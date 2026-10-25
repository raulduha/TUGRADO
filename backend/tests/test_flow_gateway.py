"""Cliente de Flow: firma de los parámetros, flujo cliente → tarjeta → suscripción, y cómo
cada estado de Flow se traduce en acceso. Sin red: las respuestas de Flow se simulan."""

import hashlib
import hmac
from urllib.parse import parse_qsl

import httpx
import pytest

from app.billing.flow import CUSTOMER_REF, FlowClient, FlowGateway, sign
from app.billing.gateway import NewSubscription, ProviderError

SECRET = "secreto-de-prueba"
REQUEST = NewSubscription(
    external_reference="ref-local",
    payer_email="estudiante@ejemplo.cl",
    reason="Suscripción",
    amount_clp=9990,
    first_charge_at=None,
    back_url="https://apruebatuexamen.cl/suscripcion/retorno",
)


class FakeFlow:
    """Responde como Flow y guarda lo que recibe, para verificar firmas y parámetros."""

    def __init__(self, responses: dict[str, dict], status: int = 200) -> None:
        self.responses = responses
        self.status = status
        self.calls: list[tuple[str, dict]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        service = request.url.path.removeprefix("/api/")
        if request.method == "GET":
            params = dict(request.url.params)
        else:
            params = dict(parse_qsl(request.content.decode()))
        self.calls.append((service, params))
        return httpx.Response(self.status, json=self.responses.get(service, {}))


def gateway(flow: FakeFlow, trial_days: int = 7) -> FlowGateway:
    client = FlowClient(
        "https://sandbox.flow.cl/api",
        "api-key",
        SECRET,
        httpx.Client(transport=httpx.MockTransport(flow)),
    )
    return FlowGateway(client, plan_id="plan-mensual", trial_days=trial_days)


def subscription(status: int, morose: int = 0) -> dict:
    return {
        "subscriptionId": "sus_123",
        "status": status,
        "morose": morose,
        "next_invoice_date": "2026-11-01",
    }


def test_la_firma_es_hmac_sha256_de_los_parametros_ordenados_por_nombre():
    params = {"customerId": "cus_1", "apiKey": "k", "amount": "9990"}
    expected = hmac.new(
        SECRET.encode(), b"amount9990apiKeykcustomerIdcus_1", hashlib.sha256
    ).hexdigest()
    assert sign(params, SECRET) == expected

    # Cada llamada real lleva apiKey y una firma válida de todo lo demás.
    flow = FakeFlow({"subscription/get": subscription(1)})
    gateway(flow).get("sus_123")
    [(_, sent)] = flow.calls
    received_signature = sent.pop("s")
    assert sent["apiKey"] == "api-key"
    assert received_signature == sign(sent, SECRET)


def test_suscribirse_crea_el_cliente_y_pide_registrar_la_tarjeta():
    flow = FakeFlow(
        {
            "customer/create": {"customerId": "cus_1"},
            "customer/register": {"url": "https://sandbox.flow.cl/app/card", "token": "tok"},
        }
    )
    created = gateway(flow).create(REQUEST)

    assert created.id == f"{CUSTOMER_REF}cus_1" and created.status == "pending"
    assert created.init_point == "https://sandbox.flow.cl/app/card?token=tok"
    customer, register = (params for _, params in flow.calls)
    assert customer["externalId"] == "ref-local" and customer["email"] == "estudiante@ejemplo.cl"
    assert register["url_return"] == REQUEST.back_url


def test_sin_tarjeta_registrada_sigue_pendiente_y_no_crea_la_suscripcion():
    flow = FakeFlow({"customer/get": {"customerId": "cus_1", "last4CardDigits": ""}})
    remote = gateway(flow).get(f"{CUSTOMER_REF}cus_1")
    assert remote.status == "pending"
    assert [service for service, _ in flow.calls] == ["customer/get"]


def test_con_tarjeta_registrada_crea_la_suscripcion_al_plan_con_la_prueba_gratis():
    flow = FakeFlow(
        {
            "customer/get": {"customerId": "cus_1", "last4CardDigits": "4242"},
            "subscription/create": subscription(status=2),  # en período de prueba
        }
    )
    remote = gateway(flow, trial_days=7).get(f"{CUSTOMER_REF}cus_1")

    assert remote.id == "sus_123" and remote.status == "authorized"
    assert remote.next_payment_date is not None and remote.next_payment_date.day == 1
    _, created = flow.calls[1]
    assert created["planId"] == "plan-mensual" and created["trial_period_days"] == "7"


@pytest.mark.parametrize(
    ("flow_status", "morose", "expected"),
    [
        (1, 0, "authorized"),  # activa y al día
        (2, 0, "authorized"),  # en prueba
        (1, 1, "paused"),  # cobro vencido: sin acceso hasta pagar
        (1, 2, "authorized"),  # cobro pendiente, aún no vencido
        (4, 0, "cancelled"),
        (0, 0, "pending"),  # no iniciada
    ],
)
def test_cada_estado_de_flow_se_traduce_en_acceso(flow_status, morose, expected):
    flow = FakeFlow({"subscription/get": subscription(flow_status, morose)})
    assert gateway(flow).get("sus_123").status == expected


def test_cancelar_es_inmediato_y_sin_suscripcion_no_llama_a_flow():
    flow = FakeFlow({"subscription/cancel": subscription(status=4)})
    assert gateway(flow).cancel("sus_123").status == "cancelled"
    [(service, params)] = flow.calls
    assert service == "subscription/cancel" and params["at_period_end"] == "0"

    idle = FakeFlow({})
    assert gateway(idle).cancel(f"{CUSTOMER_REF}cus_1").status == "cancelled"
    assert idle.calls == []


def test_un_error_de_flow_se_informa_sin_datos_sensibles():
    flow = FakeFlow({"customer/create": {"code": 1620, "message": "apiKey not found"}}, 401)
    with pytest.raises(ProviderError, match="apiKey not found"):
        gateway(flow).create(REQUEST)

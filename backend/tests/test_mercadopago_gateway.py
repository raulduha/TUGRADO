"""Cliente de Mercado Pago: cuerpo de la suscripción y motivo de los rechazos."""

import json
import logging
from datetime import UTC, datetime

import httpx
import pytest

from app.billing.gateway import MERCADOPAGO_API, MercadoPagoGateway, NewSubscription, ProviderError


def _gateway(status: int, body: dict) -> MercadoPagoGateway:
    transport = httpx.MockTransport(lambda request: httpx.Response(status, json=body))
    return MercadoPagoGateway(
        "TEST-token", httpx.Client(base_url=MERCADOPAGO_API, transport=transport)
    )


def test_un_rechazo_registra_el_motivo_de_mercado_pago(caplog):
    gateway = _gateway(
        400, {"message": "Both payer and collector must be real or test users", "status": 400}
    )
    request = NewSubscription(
        external_reference="ref",
        payer_email="estudiante@ejemplo.cl",
        reason="Suscripción",
        amount_clp=9990,
        first_charge_at=None,
        back_url="https://apruebatuexamen.cl/suscripcion/retorno",
    )
    # Las migraciones de las pruebas (fileConfig de Alembic) desactivan los loggers existentes;
    # en producción corren en otro proceso. Se reactiva y se escucha directo.
    billing_logger = logging.getLogger("tugrado.billing")
    was_disabled = billing_logger.disabled
    billing_logger.disabled = False
    billing_logger.addHandler(caplog.handler)
    try:
        with pytest.raises(ProviderError, match="must be real or test users"):
            gateway.create(request)
    finally:
        billing_logger.removeHandler(caplog.handler)
        billing_logger.disabled = was_disabled
    assert "must be real or test users" in caplog.text
    assert "estudiante@ejemplo.cl" not in caplog.text


def test_la_prueba_gratis_fija_el_primer_cobro_con_start_date():
    sent = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(json.loads(request.content))
        return httpx.Response(201, json={"id": "pre-1", "status": "pending", "init_point": "x"})

    client = httpx.Client(base_url=MERCADOPAGO_API, transport=httpx.MockTransport(handler))
    MercadoPagoGateway("TEST-token", client).create(
        NewSubscription(
            external_reference="ref",
            payer_email="estudiante@ejemplo.cl",
            reason="Suscripción",
            amount_clp=9990,
            first_charge_at=datetime(2026, 10, 30, 17, 5, 9, 123456, tzinfo=UTC),
            back_url="https://apruebatuexamen.cl/suscripcion/retorno",
        )
    )
    recurring = sent[0]["auto_recurring"]
    # Sin plan asociado, `free_trial` no evita el cobro al autorizar: se usa la fecha de inicio.
    assert "free_trial" not in recurring
    assert recurring["start_date"] == "2026-10-30T17:05:09.123Z"

"""Suscripciones con Flow (flow.cl), detrás de la misma interfaz que Mercado Pago.

Flujo:
1. `create`: crea el cliente en Flow y pide el registro de su tarjeta. La suscripción local
   queda `pending` y su referencia es la del cliente (`flow-customer:<customerId>`).
2. El estudiante registra la tarjeta en la página de Flow y vuelve a la app.
3. `get`: si el cliente ya tiene tarjeta, crea la suscripción al plan (con los días de prueba)
   y desde ahí la referencia es el `subscriptionId`. Flow cobra solo cada mes.

Acceso: la suscripción da acceso mientras está activa o en prueba y no tiene cobros vencidos.
Con un cobro vencido (`morose = 1`) queda `paused` hasta que se pague.

Autenticación de Flow: todos los parámetros (menos `s`) se ordenan por nombre, se concatenan
como nombre+valor y se firman con HMAC-SHA256 usando la secretKey; la firma va en `s`.

Por validar en el sandbox de Flow (pendiente del README): que `customer/get` informe la tarjeta
registrada en `last4CardDigits` y el contenido exacto del aviso al `urlCallback` del plan.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
from datetime import UTC, datetime

import httpx

from app.billing.gateway import NewSubscription, ProviderError, ProviderSubscription

logger = logging.getLogger("tugrado.billing")

SANDBOX_API = "https://sandbox.flow.cl/api"
PRODUCTION_API = "https://www.flow.cl/api"
CUSTOMER_REF = "flow-customer:"

# Estados de una suscripción en Flow.
INACTIVE, ACTIVE, TRIAL, CANCELLED = 0, 1, 2, 4
OVERDUE = 1  # morose: 1 = uno o más cobros vencidos


def sign(params: dict[str, str], secret_key: str) -> str:
    message = "".join(f"{name}{params[name]}" for name in sorted(params))
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()


class FlowClient:
    def __init__(
        self, api_url: str, api_key: str, secret_key: str, client: httpx.Client | None = None
    ) -> None:
        self._url = api_url.rstrip("/")
        self._api_key = api_key
        self._secret = secret_key
        self._client = client or httpx.Client(timeout=15)

    def call(self, method: str, service: str, **params: object) -> dict:
        data = {k: str(v) for k, v in params.items() if v is not None}
        data["apiKey"] = self._api_key
        data["s"] = sign(data, self._secret)
        url = f"{self._url}/{service}"
        try:
            if method == "GET":
                response = self._client.get(url, params=data)
            else:
                response = self._client.post(url, data=data)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Flow no respondió: {type(exc).__name__}") from exc
        if response.status_code >= 400:
            detail = _error_detail(response)
            logger.warning("Flow respondió %s en %s: %s", response.status_code, service, detail)
            raise ProviderError(f"Flow respondió {response.status_code} en {service}: {detail}")
        return response.json()


class FlowGateway:
    """Proveedor de suscripciones con Flow. `plan_id` es el plan creado en Flow con el precio
    mensual; `trial_days` son los días de prueba de cada suscripción nueva."""

    def __init__(self, client: FlowClient, plan_id: str, trial_days: int) -> None:
        self._flow = client
        self._plan = plan_id
        self._trial = trial_days

    def create(self, request: NewSubscription) -> ProviderSubscription:
        customer = self._flow.call(
            "POST",
            "customer/create",
            name=request.payer_email,
            email=request.payer_email,
            externalId=request.external_reference,
        )
        customer_id = str(customer["customerId"])
        register = self._flow.call(
            "POST", "customer/register", customerId=customer_id, url_return=request.back_url
        )
        return ProviderSubscription(
            id=f"{CUSTOMER_REF}{customer_id}",
            status="pending",
            init_point=f"{register['url']}?token={register['token']}",
            next_payment_date=None,
            external_reference=request.external_reference,
        )

    def get(self, provider_id: str) -> ProviderSubscription:
        if not provider_id.startswith(CUSTOMER_REF):
            data = self._flow.call("GET", "subscription/get", subscriptionId=provider_id)
            return _from_subscription(data)
        customer_id = provider_id.removeprefix(CUSTOMER_REF)
        customer = self._flow.call("GET", "customer/get", customerId=customer_id)
        if not customer.get("last4CardDigits"):
            # Todavía no registra la tarjeta: sigue pendiente.
            return ProviderSubscription(provider_id, "pending", None, None, None)
        data = self._flow.call(
            "POST",
            "subscription/create",
            planId=self._plan,
            customerId=customer_id,
            trial_period_days=self._trial or None,
        )
        return _from_subscription(data)

    def cancel(self, provider_id: str) -> ProviderSubscription:
        if provider_id.startswith(CUSTOMER_REF):
            # Sin suscripción creada en Flow: no hay nada que cancelar allá.
            return ProviderSubscription(provider_id, "cancelled", None, None, None)
        # Inmediata: mientras no se decida el acceso tras cancelar (pendiente 5 del README).
        data = self._flow.call(
            "POST", "subscription/cancel", subscriptionId=provider_id, at_period_end=0
        )
        return _from_subscription(data)


def _from_subscription(data: dict) -> ProviderSubscription:
    status = int(data.get("status", INACTIVE))
    if status == CANCELLED:
        local = "cancelled"
    elif status in (ACTIVE, TRIAL):
        local = "paused" if int(data.get("morose") or 0) == OVERDUE else "authorized"
    else:
        local = "pending"
    return ProviderSubscription(
        id=str(data["subscriptionId"]),
        status=local,
        init_point=None,
        next_payment_date=_parse_date(data.get("next_invoice_date")),
        external_reference=None,
    )


def _parse_date(value: object) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(str(value))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _error_detail(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return response.text[:200]
    if isinstance(data, dict):
        return f"{data.get('code', '-')}: {str(data.get('message'))[:200]}"
    return str(data)[:200]

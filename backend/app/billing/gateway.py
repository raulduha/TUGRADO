"""Proveedor de suscripciones detrás de una interfaz (Mercado Pago real o simulador local).

La app nunca recibe datos de tarjeta: crea la suscripción con estado `pending` y el
estudiante la autoriza en la página de Mercado Pago (`init_point`).
"""

from __future__ import annotations

import logging
import threading
import uuid
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import Protocol

import httpx

MERCADOPAGO_API = "https://api.mercadopago.com"

logger = logging.getLogger("tugrado.billing")


class ProviderError(Exception):
    """El proveedor no respondió como se esperaba. El mensaje no incluye credenciales."""


@dataclass(frozen=True)
class ProviderSubscription:
    id: str
    status: str  # pending | authorized | paused | cancelled (estados de Mercado Pago)
    init_point: str | None
    next_payment_date: datetime | None
    external_reference: str | None


@dataclass(frozen=True)
class NewSubscription:
    external_reference: str
    payer_email: str
    reason: str
    amount_clp: int
    trial_days: int
    back_url: str


class SubscriptionGateway(Protocol):
    def create(self, request: NewSubscription) -> ProviderSubscription: ...
    def get(self, provider_id: str) -> ProviderSubscription: ...
    def cancel(self, provider_id: str) -> ProviderSubscription: ...


def _parse_datetime(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _from_payload(data: dict) -> ProviderSubscription:
    return ProviderSubscription(
        id=str(data["id"]),
        status=str(data["status"]),
        init_point=data.get("init_point"),
        next_payment_date=_parse_datetime(data.get("next_payment_date")),
        external_reference=(
            str(data["external_reference"]) if data.get("external_reference") else None
        ),
    )


def _error_detail(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return response.text[:200]
    if not isinstance(data, dict):
        return str(data)[:200]
    return f"{data.get('code') or data.get('error') or '-'}: {str(data.get('message'))[:200]}"


class MercadoPagoGateway:
    """API de suscripciones sin plan asociado (`/preapproval`)."""

    def __init__(self, access_token: str, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(base_url=MERCADOPAGO_API, timeout=15)
        self._headers = {"Authorization": f"Bearer {access_token}"}

    def _request(self, method: str, path: str, **kwargs) -> dict:
        try:
            response = self._client.request(
                method, path, headers={**self._headers, **kwargs.pop("headers", {})}, **kwargs
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Mercado Pago no respondió: {type(exc).__name__}") from exc
        if response.status_code >= 400:
            # El motivo que da Mercado Pago (p. ej. pagador y vendedor de entornos distintos) se
            # registra para diagnosticar; no incluye datos de tarjeta.
            detail = _error_detail(response)
            logger.warning(
                "Mercado Pago respondió %s en %s %s: %s",
                response.status_code,
                method,
                path.split("/")[1],
                detail,
            )
            raise ProviderError(
                f"Mercado Pago respondió {response.status_code} en {path}: {detail}"
            )
        return response.json()

    def create(self, request: NewSubscription) -> ProviderSubscription:
        auto_recurring: dict = {
            "frequency": 1,
            "frequency_type": "months",
            "transaction_amount": request.amount_clp,
            "currency_id": "CLP",
        }
        if request.trial_days > 0:
            auto_recurring["free_trial"] = {
                "frequency": request.trial_days,
                "frequency_type": "days",
            }
        body = {
            "reason": request.reason,
            "external_reference": request.external_reference,
            "payer_email": request.payer_email,
            "auto_recurring": auto_recurring,
            "back_url": request.back_url,
            "status": "pending",
        }
        # La referencia local sirve de clave de idempotencia: un reintento no duplica.
        headers = {"X-Idempotency-Key": request.external_reference}
        return _from_payload(self._request("POST", "/preapproval", json=body, headers=headers))

    def get(self, provider_id: str) -> ProviderSubscription:
        return _from_payload(self._request("GET", f"/preapproval/{provider_id}"))

    def cancel(self, provider_id: str) -> ProviderSubscription:
        payload = self._request("PUT", f"/preapproval/{provider_id}", json={"status": "cancelled"})
        return _from_payload(payload)


class FakeGateway:
    """Simulador local para desarrollo y pruebas: no cobra ni contacta a Mercado Pago.

    El enlace de pago apunta a una página del frontend que permite aprobar el pago. Está
    prohibido en producción (validado en `Settings`).
    """

    def __init__(self, frontend_base_url: str) -> None:
        self._frontend = frontend_base_url.rstrip("/")
        self._items: dict[str, ProviderSubscription] = {}
        self._trial: dict[str, int] = {}
        self._lock = threading.Lock()

    def create(self, request: NewSubscription) -> ProviderSubscription:
        provider_id = f"fake-{uuid.uuid4().hex}"
        item = ProviderSubscription(
            id=provider_id,
            status="pending",
            init_point=f"{self._frontend}/suscripcion/simulador?id={provider_id}",
            next_payment_date=None,
            external_reference=request.external_reference,
        )
        with self._lock:
            self._items[provider_id] = item
            self._trial[provider_id] = request.trial_days
        return item

    def get(self, provider_id: str) -> ProviderSubscription:
        with self._lock:
            if provider_id not in self._items:
                raise ProviderError("suscripción simulada inexistente")
            return self._items[provider_id]

    def cancel(self, provider_id: str) -> ProviderSubscription:
        return self._set(provider_id, status="cancelled", next_payment_date=None)

    def approve(self, provider_id: str, now: datetime) -> ProviderSubscription:
        """Simula que el estudiante autorizó el pago en Mercado Pago."""
        trial = self._trial.get(provider_id, 0)
        return self._set(
            provider_id, status="authorized", next_payment_date=now + timedelta(days=trial)
        )

    def _set(self, provider_id: str, **changes) -> ProviderSubscription:
        with self._lock:
            item = self._items.get(provider_id)
            if item is None:
                raise ProviderError("suscripción simulada inexistente")
            self._items[provider_id] = replace(item, **changes)
            return self._items[provider_id]

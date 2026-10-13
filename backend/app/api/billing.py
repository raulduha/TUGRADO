"""Suscripción y webhooks de Mercado Pago (FR-029 a FR-031, AC-038, AC-039)."""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from pydantic import BaseModel

from app.api.deps import (
    CurrentUser,
    get_billing_service,
    get_clock,
    get_subscription_gateway,
)
from app.billing.gateway import FakeGateway, SubscriptionGateway
from app.billing.service import BillingError, BillingService
from app.billing.signature import InvalidSignature, verify
from app.config import Settings, get_settings
from app.persistence.billing_models import SubscriptionStatus

logger = logging.getLogger("tugrado.billing")

router = APIRouter(prefix="/billing", tags=["billing"])

Billing = Annotated[BillingService, Depends(get_billing_service)]
AppSettings = Annotated[Settings, Depends(get_settings)]


class SubscriptionOut(BaseModel):
    status: SubscriptionStatus | None
    has_access: bool
    amount_clp: int
    trial_days: int
    next_payment_date: datetime | None
    checkout_url: str | None


class CheckoutOut(BaseModel):
    checkout_url: str


def _view(billing: BillingService, user: CurrentUser) -> SubscriptionOut:
    view = billing.view(user.id, user.roles)
    return SubscriptionOut(**view.__dict__)


@router.get("/subscription")
def get_subscription(user: CurrentUser, billing: Billing) -> SubscriptionOut:
    return _view(billing, user)


@router.post("/subscription", status_code=status.HTTP_201_CREATED)
def start_subscription(user: CurrentUser, billing: Billing) -> CheckoutOut:
    return CheckoutOut(checkout_url=billing.start(user.id))


@router.post("/subscription/sync")
def sync_subscription(user: CurrentUser, billing: Billing) -> SubscriptionOut:
    """Al volver de Mercado Pago: se consulta el estado real; los parámetros de la URL de
    retorno no se usan."""
    billing.sync_user(user.id, source="return")
    return _view(billing, user)


@router.post("/subscription/cancel")
def cancel_subscription(user: CurrentUser, billing: Billing) -> SubscriptionOut:
    billing.cancel(user.id)
    return _view(billing, user)


@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(
    request: Request,
    billing: Billing,
    settings: AppSettings,
    data_id: Annotated[str | None, Query(alias="data.id")] = None,
    topic: Annotated[str | None, Query(alias="type")] = None,
    x_signature: Annotated[str | None, Header()] = None,
    x_request_id: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    secret = settings.mercadopago_webhook_secret
    if secret is None or not secret.get_secret_value():
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    try:
        verify(x_signature, x_request_id, data_id, secret.get_secret_value())
    except InvalidSignature as exc:
        # Sin datos sensibles en el log: solo el motivo y el id de la solicitud.
        logger.warning("Webhook rechazado (%s), request_id=%s", exc, x_request_id)
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail={"code": "invalid_signature", "message": "Firma inválida"},
        ) from exc

    if topic is None:
        body = await request.json()
        topic = body.get("type") if isinstance(body, dict) else None
    if topic != "subscription_preapproval" or not data_id:
        return {"status": "ignored"}
    try:
        billing.sync_provider_subscription(data_id, source="webhook")
    except BillingError as exc:
        # 5xx: Mercado Pago reintenta la notificación más tarde.
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE) from exc
    return {"status": "ok"}


# ------------------------------------------------- simulador (solo BILLING_PROVIDER=fake)

fake_router = APIRouter(prefix="/billing/fake", tags=["billing"])


@fake_router.post("/approve")
def approve_fake_subscription(
    user: CurrentUser,
    billing: Billing,
    gateway: Annotated[SubscriptionGateway, Depends(get_subscription_gateway)],
    clock: Annotated[Callable[[], datetime], Depends(get_clock)],
) -> SubscriptionOut:
    """Simula que el estudiante autorizó el pago en Mercado Pago. Solo en desarrollo."""
    if not isinstance(gateway, FakeGateway):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    view = billing.view(user.id, user.roles)
    if view.status != SubscriptionStatus.PENDING:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail={"code": "nothing_to_approve", "message": "No hay un pago pendiente"},
        )
    row = billing.open_subscription(user.id)
    assert row is not None and row.provider_subscription_id is not None
    gateway.approve(row.provider_subscription_id, clock())
    billing.sync_user(user.id, source="return")
    return _view(billing, user)

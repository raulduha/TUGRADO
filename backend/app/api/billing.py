"""Suscripción y avisos de los proveedores de pago: Mercado Pago o Flow (FR-029 a FR-031,
AC-038, AC-039)."""

import logging
import secrets
from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from pydantic import BaseModel, EmailStr

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
    payer_email: str | None
    provider: str  # mercadopago | flow | fake: el frontend ajusta sus textos
    # Mercado Pago exige el correo de la cuenta que paga; Flow y el simulador, no.
    asks_payer_email: bool


class StartIn(BaseModel):
    # Correo de la cuenta de Mercado Pago con la que se pagará; por omisión, el de la app.
    payer_email: EmailStr | None = None


class CheckoutOut(BaseModel):
    checkout_url: str


def _view(billing: BillingService, user: CurrentUser) -> SubscriptionOut:
    view = billing.view(user.id, user.roles)
    return SubscriptionOut(
        **view.__dict__,
        provider=billing.provider_name,
        asks_payer_email=billing.provider_name == "mercadopago",
    )


@router.get("/subscription")
def get_subscription(user: CurrentUser, billing: Billing) -> SubscriptionOut:
    return _view(billing, user)


@router.post("/subscription", status_code=status.HTTP_201_CREATED)
def start_subscription(
    user: CurrentUser, billing: Billing, body: StartIn | None = None
) -> CheckoutOut:
    payer = str(body.payer_email) if body and body.payer_email else None
    return CheckoutOut(checkout_url=billing.start(user.id, payer))


@router.post("/subscription/sync")
def sync_subscription(user: CurrentUser, billing: Billing) -> SubscriptionOut:
    """Al volver de la página de pago: se consulta el estado real al proveedor; los parámetros
    de la URL de retorno no se usan."""
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
        # Sin la clave en el log: el motivo y los datos firmados (públicos) para diagnosticar
        # una clave equivocada.
        logger.warning(
            "Webhook rechazado (%s), request_id=%s data_id=%s x_signature=%s",
            exc,
            x_request_id,
            data_id,
            x_signature,
        )
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


@router.post("/webhooks/flow")
def flow_webhook(billing: Billing, settings: AppSettings) -> dict[str, int]:
    """Aviso de Flow (urlCallback del plan) tras un cobro de la suscripción. El contenido no se
    usa como dato: se consulta a Flow el estado de las suscripciones abiertas."""
    if settings.billing_provider != "flow":
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    synced, failed = billing.sync_open(source="webhook")
    if failed:
        # 5xx: que Flow reintente el aviso.
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
    return {"synced": synced}


@router.get("/sync/run")
def run_sync(
    billing: Billing,
    settings: AppSettings,
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, int]:
    """Tarea diaria (Vercel Cron, `Authorization: Bearer <CRON_SECRET>`): consulta al proveedor
    todas las suscripciones abiertas, por si se perdió algún aviso (por ejemplo, un cobro
    rechazado que deja la suscripción con pagos vencidos)."""
    secret = settings.cron_secret.get_secret_value() if settings.cron_secret else ""
    if not secret or settings.billing_provider == "fake":
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not secrets.compare_digest(authorization or "", f"Bearer {secret}"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    synced, failed = billing.sync_open(source="sync")
    return {"synced": synced, "failed": failed}


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

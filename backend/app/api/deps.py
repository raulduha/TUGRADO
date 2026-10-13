"""Dependencias compartidas por los endpoints. Las pruebas las reemplazan con
`app.dependency_overrides` (reloj, envío de correo, base de datos)."""

from collections.abc import Callable
from datetime import datetime
from functools import lru_cache
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.email import ConsoleEmailSender, EmailSender, ResendEmailSender
from app.auth.google import GoogleOAuth, GoogleProvider
from app.auth.service import AuthenticatedUser, AuthService
from app.billing.gateway import FakeGateway, MercadoPagoGateway, SubscriptionGateway
from app.billing.service import BillingPlan, BillingService
from app.clock import utc_now
from app.config import Settings, get_settings
from app.db import get_db
from app.persistence.auth_models import Role

SESSION_COOKIE = "tugrado_session"


def get_clock() -> Callable[[], datetime]:
    return utc_now


@lru_cache
def _email_sender_for(provider: str, api_key: str | None, from_address: str) -> EmailSender:
    if provider == "resend":
        assert api_key is not None
        return ResendEmailSender(api_key, from_address)
    return ConsoleEmailSender()


def get_email_sender(settings: Annotated[Settings, Depends(get_settings)]) -> EmailSender:
    key = settings.resend_api_key
    return _email_sender_for(
        settings.email_provider, key.get_secret_value() if key else None, settings.email_from
    )


def get_auth_service(
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    clock: Annotated[Callable[[], datetime], Depends(get_clock)],
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
) -> AuthService:
    return AuthService(
        db=db,
        policy=settings.auth_policy(),
        clock=clock,
        email_sender=email_sender,
        frontend_base_url=settings.frontend_base_url,
    )


def current_user(
    service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[str | None, Cookie(alias=SESSION_COOKIE)] = None,
) -> AuthenticatedUser:
    user = service.authenticate(token) if token else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail={"code": "not_authenticated", "message": "Debes iniciar sesión"},
        )
    return user


def require_role(role: Role) -> Callable[[AuthenticatedUser], AuthenticatedUser]:
    def dependency(
        user: Annotated[AuthenticatedUser, Depends(current_user)],
    ) -> AuthenticatedUser:
        if role not in user.roles:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                detail={"code": "forbidden", "message": "No tienes permiso para esta operación"},
            )
        return user

    return dependency


CurrentUser = Annotated[AuthenticatedUser, Depends(current_user)]
AdminUser = Annotated[AuthenticatedUser, Depends(require_role(Role.ADMINISTRATOR))]


# ------------------------------------------------------------------ suscripción


@lru_cache
def _gateway_for(provider: str, access_token: str | None, frontend: str) -> SubscriptionGateway:
    if provider == "mercadopago":
        assert access_token is not None
        return MercadoPagoGateway(access_token)
    return FakeGateway(frontend)


def get_subscription_gateway(
    settings: Annotated[Settings, Depends(get_settings)],
) -> SubscriptionGateway:
    token = settings.mercadopago_access_token
    return _gateway_for(
        settings.billing_provider,
        token.get_secret_value() if token else None,
        settings.frontend_base_url,
    )


def get_billing_service(
    db: Annotated[Session, Depends(get_db)],
    settings: Annotated[Settings, Depends(get_settings)],
    clock: Annotated[Callable[[], datetime], Depends(get_clock)],
    gateway: Annotated[SubscriptionGateway, Depends(get_subscription_gateway)],
) -> BillingService:
    return BillingService(
        db=db,
        gateway=gateway,
        plan=BillingPlan(
            amount_clp=settings.billing_monthly_price_clp, trial_days=settings.billing_trial_days
        ),
        clock=clock,
        provider_name=settings.billing_provider,
        frontend_base_url=settings.frontend_base_url,
    )


def subscribed_user(
    user: Annotated[AuthenticatedUser, Depends(current_user)],
    billing: Annotated[BillingService, Depends(get_billing_service)],
) -> AuthenticatedUser:
    """Usuario con acceso al estudio: suscripción activa, o administrador (FR-030)."""
    if not billing.has_access(user.id, user.roles):
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "code": "subscription_required",
                "message": "Necesitas una suscripción activa para usar esta función",
            },
        )
    return user


SubscribedUser = Annotated[AuthenticatedUser, Depends(subscribed_user)]


# --------------------------------------------------------------- ingreso con Google


@lru_cache
def _google_for(client_id: str, client_secret: str) -> GoogleProvider:
    return GoogleOAuth(client_id, client_secret)


def get_google_provider(
    settings: Annotated[Settings, Depends(get_settings)],
) -> GoogleProvider | None:
    if not settings.google_enabled or settings.google_client_secret is None:
        return None
    assert settings.google_client_id is not None
    return _google_for(settings.google_client_id, settings.google_client_secret.get_secret_value())

"""Endpoints de cuentas y sesión (FR-001, FR-001b, AC-032, AC-036, AC-040)."""

import hmac
import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, EmailStr

from app.api.deps import (
    SESSION_COOKIE,
    AppSettings,
    Clock,
    CurrentUser,
    get_auth_service,
    get_google_provider,
)
from app.auth.google import GoogleAuthError, GoogleProvider, new_pkce_pair
from app.auth.service import AuthError, AuthService
from app.auth.signed import InvalidSignedValue, sign, unsign
from app.auth.tokens import new_token
from app.config import Settings
from app.persistence.auth_models import Role

logger = logging.getLogger("tugrado.auth")

router = APIRouter(prefix="/auth", tags=["auth"])

Service = Annotated[AuthService, Depends(get_auth_service)]

# Respuesta idéntica exista o no el correo: no se revela qué cuentas están registradas.
ACCEPTED = {"detail": "Si el correo es válido, te enviamos un mensaje con los pasos a seguir."}


class Credentials(BaseModel):
    email: EmailStr
    password: str


class EmailOnly(BaseModel):
    email: EmailStr


class TokenOnly(BaseModel):
    token: str


class PasswordReset(BaseModel):
    token: str
    password: str


class Me(BaseModel):
    id: str
    email: str
    roles: list[Role]


@router.post("/register", status_code=status.HTTP_202_ACCEPTED)
def register(body: Credentials, service: Service) -> dict[str, str]:
    service.register(body.email, body.password)
    return ACCEPTED


@router.post("/verify-email", status_code=status.HTTP_204_NO_CONTENT)
def verify_email(body: TokenOnly, service: Service) -> None:
    service.verify_email(body.token)


@router.post("/resend-verification", status_code=status.HTTP_202_ACCEPTED)
def resend_verification(body: EmailOnly, service: Service) -> dict[str, str]:
    service.resend_verification(body.email)
    return ACCEPTED


def _set_session_cookie(response: Response, token: str, settings: Settings) -> None:
    """La cookie de sesión, con los mismos atributos al ingresar con contraseña o con Google."""
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=settings.auth_session_max_age_seconds,
        httponly=True,
        secure=settings.auth_cookie_secure,
        samesite="lax",
        path="/",
    )


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(body: Credentials, response: Response, service: Service, settings: AppSettings) -> None:
    token = service.login(body.email, body.password)
    _set_session_cookie(response, token, settings)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    service: Service,
    settings: AppSettings,
    token: Annotated[str | None, Cookie(alias=SESSION_COOKIE)] = None,
) -> None:
    if token:
        service.logout(token)
    response.delete_cookie(
        SESSION_COOKIE, path="/", secure=settings.auth_cookie_secure, httponly=True, samesite="lax"
    )


@router.get("/me")
def me(user: CurrentUser) -> Me:
    return Me(id=str(user.id), email=user.email, roles=sorted(user.roles))


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
def request_password_reset(body: EmailOnly, service: Service) -> dict[str, str]:
    service.request_password_reset(body.email)
    return ACCEPTED


@router.post("/password-reset/confirm", status_code=status.HTTP_204_NO_CONTENT)
def confirm_password_reset(body: PasswordReset, service: Service) -> None:
    service.reset_password(body.token, body.password)


# --------------------------------------------------------------- ingreso con Google

GOOGLE_COOKIE = "tugrado_google"
GOOGLE_COOKIE_TTL = timedelta(minutes=10)
Google = Annotated[GoogleProvider | None, Depends(get_google_provider)]


# Google vuelve al frontend, que reenvía /api al backend: así la cookie de sesión es de primera
# parte en apruebatuexamen.cl.
GOOGLE_CALLBACK_PATH = "/api/auth/google/callback"


def _frontend(settings: Settings, path: str) -> str:
    return f"{settings.frontend_base_url.rstrip('/')}{path}"


@router.get("/providers")
def providers(settings: AppSettings) -> dict[str, bool]:
    return {"google": settings.google_enabled}


@router.get("/google/start")
def google_start(
    google: Google, settings: AppSettings, clock: Clock, next: str = "/panel"
) -> RedirectResponse:
    if google is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    assert settings.oauth_state_secret is not None
    state, nonce = new_token(), new_token()
    verifier, challenge = new_pkce_pair()
    safe_next = next if next.startswith("/") and not next.startswith("//") else "/panel"
    cookie = sign(
        {"state": state, "nonce": nonce, "verifier": verifier, "next": safe_next},
        settings.oauth_state_secret.get_secret_value(),
        clock() + GOOGLE_COOKIE_TTL,
    )
    response = RedirectResponse(
        google.authorize_url(state, nonce, challenge, _frontend(settings, GOOGLE_CALLBACK_PATH)),
        status_code=302,
    )
    response.set_cookie(
        GOOGLE_COOKIE,
        cookie,
        max_age=int(GOOGLE_COOKIE_TTL.total_seconds()),
        httponly=True,
        secure=settings.auth_cookie_secure,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/google/callback")
def google_callback(
    google: Google,
    settings: AppSettings,
    service: Service,
    clock: Clock,
    code: str | None = None,
    state: str | None = None,
    stored: Annotated[str | None, Cookie(alias=GOOGLE_COOKIE)] = None,
) -> RedirectResponse:
    if google is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    assert settings.oauth_state_secret is not None
    failure = RedirectResponse(_frontend(settings, "/iniciar-sesion?error=google"), 302)
    failure.delete_cookie(GOOGLE_COOKIE, path="/")
    try:
        saved = unsign(stored, settings.oauth_state_secret.get_secret_value(), clock())
    except InvalidSignedValue:
        return failure
    if not code or not state or not hmac.compare_digest(state, str(saved.get("state", ""))):
        return failure
    try:
        identity = google.identify(
            code, saved["verifier"], _frontend(settings, GOOGLE_CALLBACK_PATH), saved["nonce"]
        )
        token = service.login_with_google(identity)
    except (GoogleAuthError, AuthError) as exc:
        logger.warning("Ingreso con Google rechazado: %s", exc)
        return failure
    response = RedirectResponse(_frontend(settings, saved.get("next", "/panel")), 302)
    response.delete_cookie(GOOGLE_COOKIE, path="/")
    _set_session_cookie(response, token, settings)
    return response

"""Endpoints de cuentas y sesión (FR-001, AC-032, AC-036)."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr

from app.api.deps import SESSION_COOKIE, CurrentUser, get_auth_service
from app.auth.passwords import PasswordPolicyError
from app.auth.service import AuthError, AuthService
from app.config import Settings, get_settings
from app.persistence.auth_models import Role

router = APIRouter(prefix="/auth", tags=["auth"])

Service = Annotated[AuthService, Depends(get_auth_service)]
AppSettings = Annotated[Settings, Depends(get_settings)]

# Respuesta idéntica exista o no el correo: no se revela qué cuentas están registradas.
ACCEPTED = {"detail": "Si el correo es válido, te enviamos un mensaje con los pasos a seguir."}

_STATUS_BY_CODE = {
    "invalid_credentials": status.HTTP_401_UNAUTHORIZED,
    "email_not_verified": status.HTTP_403_FORBIDDEN,
    "account_locked": status.HTTP_429_TOO_MANY_REQUESTS,
    "invalid_token": status.HTTP_400_BAD_REQUEST,
}


def _http_error(exc: AuthError | PasswordPolicyError) -> HTTPException:
    if isinstance(exc, PasswordPolicyError):
        code = status.HTTP_422_UNPROCESSABLE_CONTENT
    else:
        code = _STATUS_BY_CODE.get(exc.code, status.HTTP_400_BAD_REQUEST)
    return HTTPException(code, detail={"code": exc.code, "message": str(exc)})


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
    try:
        service.register(body.email, body.password)
    except PasswordPolicyError as exc:
        raise _http_error(exc) from exc
    return ACCEPTED


@router.post("/verify-email", status_code=status.HTTP_204_NO_CONTENT)
def verify_email(body: TokenOnly, service: Service) -> None:
    try:
        service.verify_email(body.token)
    except AuthError as exc:
        raise _http_error(exc) from exc


@router.post("/resend-verification", status_code=status.HTTP_202_ACCEPTED)
def resend_verification(body: EmailOnly, service: Service) -> dict[str, str]:
    service.resend_verification(body.email)
    return ACCEPTED


@router.post("/login", status_code=status.HTTP_204_NO_CONTENT)
def login(body: Credentials, response: Response, service: Service, settings: AppSettings) -> None:
    try:
        token = service.login(body.email, body.password)
    except AuthError as exc:
        raise _http_error(exc) from exc
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=settings.auth_session_max_age_seconds,
        httponly=True,
        secure=settings.auth_cookie_secure,
        samesite="lax",
        path="/",
    )


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
    try:
        service.reset_password(body.token, body.password)
    except (AuthError, PasswordPolicyError) as exc:
        raise _http_error(exc) from exc

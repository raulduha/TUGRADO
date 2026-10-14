"""Traducción de errores de negocio a respuestas HTTP `{"detail": {"code", "message"}}`."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.auth.passwords import PasswordPolicyError
from app.errors import AppError

# Código de error → estado HTTP. Lo que no esté aquí responde 400.
STATUS_BY_CODE = {
    "invalid_credentials": status.HTTP_401_UNAUTHORIZED,
    "email_not_verified": status.HTTP_403_FORBIDDEN,
    "account_locked": status.HTTP_429_TOO_MANY_REQUESTS,
    "invalid_token": status.HTTP_400_BAD_REQUEST,
    "already_subscribed": status.HTTP_409_CONFLICT,
    "no_subscription": status.HTTP_404_NOT_FOUND,
    "billing_unavailable": status.HTTP_503_SERVICE_UNAVAILABLE,
    "question_not_found": status.HTTP_404_NOT_FOUND,
    "invalid_transition": status.HTTP_409_CONFLICT,
    "author_cannot_review": status.HTTP_403_FORBIDDEN,
    "file_too_large": status.HTTP_413_CONTENT_TOO_LARGE,
}


def http_status_for(exc: AppError) -> int:
    if isinstance(exc, PasswordPolicyError):
        return status.HTTP_422_UNPROCESSABLE_CONTENT
    return STATUS_BY_CODE.get(exc.code, status.HTTP_400_BAD_REQUEST)


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=http_status_for(exc),
            content={"detail": {"code": exc.code, "message": str(exc)}},
        )

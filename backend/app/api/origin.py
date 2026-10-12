"""Protección CSRF para la sesión en cookie: las operaciones que modifican datos solo se
aceptan desde el origen del frontend. Complementa SameSite=Lax."""

from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

Middleware = Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]


def origin_guard(allowed_origin: str) -> Middleware:
    async def middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        origin = request.headers.get("origin")
        # Sin encabezado Origin no es un navegador en otro sitio (los navegadores lo envían en
        # solicitudes que modifican datos); se acepta, por ejemplo, desde curl.
        if request.method not in SAFE_METHODS and origin is not None and origin != allowed_origin:
            return JSONResponse(
                status_code=403,
                content={
                    "detail": {"code": "origin_not_allowed", "message": "Origen no permitido"}
                },
            )
        return await call_next(request)

    return middleware

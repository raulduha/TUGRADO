from fastapi import FastAPI

from app.api import auth, health
from app.api.origin import origin_guard
from app.config import get_settings


def create_app() -> FastAPI:
    # Valida la configuración al arrancar: falla de inmediato si falta un valor obligatorio.
    settings = get_settings()
    app = FastAPI(title="TUGRADO API", version="0.1.0")
    app.middleware("http")(origin_guard(settings.frontend_origin))
    app.include_router(health.router)
    app.include_router(auth.router)
    return app


app = create_app()

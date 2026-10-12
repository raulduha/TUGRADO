from fastapi import FastAPI

from app.api import health
from app.config import get_settings


def create_app() -> FastAPI:
    # Valida la configuración al arrancar: falla de inmediato si falta un valor obligatorio.
    get_settings()
    app = FastAPI(title="TUGRADO API", version="0.1.0")
    app.include_router(health.router)
    return app


app = create_app()

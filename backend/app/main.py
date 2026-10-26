from fastapi import FastAPI

from app.api import auth, billing, drills, engagement, feedback, health, practice, questions, study
from app.api.errors import register_error_handlers
from app.api.origin import origin_guard
from app.config import get_settings


def create_app() -> FastAPI:
    # Valida la configuración al arrancar: falla de inmediato si falta un valor obligatorio.
    settings = get_settings()
    app = FastAPI(title="Aprueba tu examen API", version="0.1.0")
    app.middleware("http")(origin_guard(settings.frontend_origin))
    register_error_handlers(app)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(feedback.router)
    app.include_router(billing.router)
    app.include_router(engagement.router)
    app.include_router(questions.router)
    app.include_router(practice.router)
    app.include_router(drills.router)
    app.include_router(study.router)
    if settings.billing_provider == "fake":
        # Simulador de pagos: solo existe en desarrollo (Settings lo prohíbe en producción).
        app.include_router(billing.fake_router)
    return app


app = create_app()

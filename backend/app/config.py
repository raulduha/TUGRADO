from datetime import timedelta
from functools import lru_cache
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.auth.policy import AuthPolicy
from app.domain.simulation.policy import SessionPolicy


class Settings(BaseSettings):
    """Configuración del backend.

    Los campos sin valor por defecto son obligatorios: el arranque falla si faltan.
    Los valores confirmados en el README se cargan desde el entorno, no se codifican aquí.
    """

    model_config = SettingsConfigDict(
        # El .env de la raíz del repo (al ejecutar desde backend/) y uno local opcional.
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Entorno de ejecución: en producción se prohíben atajos de desarrollo.
    app_env: Literal["development", "test", "production"]

    database_url: str

    # Reglas de tiempo de la simulación (FR-010 a FR-012b).
    session_extension_seconds: int = Field(gt=0)
    session_max_extensions_per_question: int = Field(ge=0)
    session_extension_offer_window_seconds: int = Field(gt=0)
    # Lo usa el cliente; el backend lo expone y valida que sea menor que el timeout.
    session_heartbeat_interval_seconds: int = Field(gt=0)
    session_heartbeat_timeout_seconds: int = Field(gt=0)
    session_recovery_window_seconds: int = Field(gt=0)
    session_voluntary_pause_max_seconds: int = Field(gt=0)
    session_voluntary_pauses_per_session: int = Field(ge=0)

    # Autenticación (FR-001, AC-032, AC-036).
    auth_password_min_length: int = Field(gt=0)
    auth_password_max_length: int = Field(gt=0)
    auth_session_idle_timeout_seconds: int = Field(gt=0)
    auth_session_max_age_seconds: int = Field(gt=0)
    auth_email_verification_ttl_seconds: int = Field(gt=0)
    auth_password_reset_ttl_seconds: int = Field(gt=0)
    auth_login_max_failures: int = Field(gt=0)
    auth_login_failure_window_seconds: int = Field(gt=0)
    auth_login_lockout_seconds: int = Field(gt=0)
    auth_cookie_secure: bool
    # Origen del frontend: base de los enlaces de correo y origen aceptado (validación de Origin).
    frontend_base_url: str

    # Correo (verificación y recuperación). console = solo log, prohibido en producción.
    email_provider: Literal["console", "resend"]
    email_from: str
    resend_api_key: SecretStr | None = None

    # Ingreso con Google (FR-001b). Sin GOOGLE_CLIENT_ID queda desactivado.
    google_client_id: str | None = None
    google_client_secret: SecretStr | None = None
    # Firma la cookie temporal del ingreso con Google (state, nonce, PKCE).
    oauth_state_secret: SecretStr | None = None

    @property
    def google_enabled(self) -> bool:
        return bool(self.google_client_id)

    # Suscripción (FR-029 a FR-031). Precio en pesos chilenos, sin decimales.
    billing_provider: Literal["mercadopago", "fake"]
    billing_monthly_price_clp: int = Field(gt=0)
    billing_trial_days: int = Field(ge=0)
    # Solo con billing_provider=mercadopago (pendiente 6 del README).
    mercadopago_access_token: SecretStr | None = None
    mercadopago_webhook_secret: SecretStr | None = None

    @model_validator(mode="after")
    def _check_environment(self) -> Self:
        if self.billing_provider == "mercadopago" and not (
            _filled(self.mercadopago_access_token) and _filled(self.mercadopago_webhook_secret)
        ):
            raise ValueError(
                "billing_provider=mercadopago requiere MERCADOPAGO_ACCESS_TOKEN y "
                "MERCADOPAGO_WEBHOOK_SECRET"
            )
        if self.google_enabled and not (
            _filled(self.google_client_secret) and _filled(self.oauth_state_secret)
        ):
            raise ValueError("GOOGLE_CLIENT_ID requiere GOOGLE_CLIENT_SECRET y OAUTH_STATE_SECRET")
        if self.email_provider == "resend" and not _filled(self.resend_api_key):
            raise ValueError("email_provider=resend requiere RESEND_API_KEY")
        if self.app_env == "production":
            if self.email_provider == "console":
                raise ValueError("En producción los correos deben enviarse (EMAIL_PROVIDER=resend)")
            if self.billing_provider == "fake":
                raise ValueError("El simulador de pagos no puede usarse en producción")
            if not self.auth_cookie_secure:
                raise ValueError("En producción AUTH_COOKIE_SECURE debe ser true")
        return self

    def auth_policy(self) -> AuthPolicy:
        return AuthPolicy(
            password_min_length=self.auth_password_min_length,
            password_max_length=self.auth_password_max_length,
            session_idle_timeout=timedelta(seconds=self.auth_session_idle_timeout_seconds),
            session_max_age=timedelta(seconds=self.auth_session_max_age_seconds),
            email_verification_ttl=timedelta(seconds=self.auth_email_verification_ttl_seconds),
            password_reset_ttl=timedelta(seconds=self.auth_password_reset_ttl_seconds),
            login_max_failures=self.auth_login_max_failures,
            login_failure_window=timedelta(seconds=self.auth_login_failure_window_seconds),
            login_lockout=timedelta(seconds=self.auth_login_lockout_seconds),
        )

    @property
    def frontend_origin(self) -> str:
        parts = urlsplit(self.frontend_base_url)
        return f"{parts.scheme}://{parts.netloc}"

    def session_policy(self) -> SessionPolicy:
        return SessionPolicy(
            extension=timedelta(seconds=self.session_extension_seconds),
            max_extensions_per_question=self.session_max_extensions_per_question,
            extension_offer_window=timedelta(seconds=self.session_extension_offer_window_seconds),
            heartbeat_interval=timedelta(seconds=self.session_heartbeat_interval_seconds),
            heartbeat_timeout=timedelta(seconds=self.session_heartbeat_timeout_seconds),
            recovery_window=timedelta(seconds=self.session_recovery_window_seconds),
            voluntary_pause_max=timedelta(seconds=self.session_voluntary_pause_max_seconds),
            voluntary_pauses_per_session=self.session_voluntary_pauses_per_session,
        )


def _filled(secret: SecretStr | None) -> bool:
    # Una variable vacía en .env llega como SecretStr(""): no cuenta como configurada.
    return secret is not None and bool(secret.get_secret_value().strip())


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # Valida también las reglas cruzadas de la política al arrancar.
    settings.session_policy()
    settings.auth_policy()
    return settings

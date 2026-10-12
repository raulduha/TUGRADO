from datetime import timedelta
from functools import lru_cache
from urllib.parse import urlsplit

from pydantic import Field
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


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # Valida también las reglas cruzadas de la política al arrancar.
    settings.session_policy()
    settings.auth_policy()
    return settings

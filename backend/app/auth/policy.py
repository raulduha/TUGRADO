from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class AuthPolicy:
    """Reglas de cuentas y sesiones (FR-001, AC-032, AC-036). Valores desde la configuración."""

    password_min_length: int
    password_max_length: int
    session_idle_timeout: timedelta
    session_max_age: timedelta
    email_verification_ttl: timedelta
    password_reset_ttl: timedelta
    login_max_failures: int
    login_failure_window: timedelta
    login_lockout: timedelta

    def __post_init__(self) -> None:
        if not 1 <= self.password_min_length <= self.password_max_length:
            raise ValueError("password_min_length debe estar entre 1 y password_max_length")
        if self.session_idle_timeout > self.session_max_age:
            raise ValueError("session_idle_timeout no puede superar session_max_age")
        if self.login_max_failures < 1:
            raise ValueError("login_max_failures debe ser al menos 1")

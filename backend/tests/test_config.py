from datetime import timedelta

import pytest
from pydantic import ValidationError

from app.config import Settings

REQUIRED = {
    "DATABASE_URL": "postgresql+psycopg://u:p@127.0.0.1:5432/x",
    "SESSION_EXTENSION_SECONDS": "60",
    "SESSION_MAX_EXTENSIONS_PER_QUESTION": "1",
    "SESSION_EXTENSION_OFFER_WINDOW_SECONDS": "15",
    "SESSION_HEARTBEAT_INTERVAL_SECONDS": "10",
    "SESSION_HEARTBEAT_TIMEOUT_SECONDS": "30",
    "SESSION_RECOVERY_WINDOW_SECONDS": "1800",
    "SESSION_VOLUNTARY_PAUSE_MAX_SECONDS": "30",
    "SESSION_VOLUNTARY_PAUSES_PER_SESSION": "1",
    "AUTH_PASSWORD_MIN_LENGTH": "12",
    "AUTH_PASSWORD_MAX_LENGTH": "128",
    "AUTH_SESSION_IDLE_TIMEOUT_SECONDS": "604800",
    "AUTH_SESSION_MAX_AGE_SECONDS": "2592000",
    "AUTH_EMAIL_VERIFICATION_TTL_SECONDS": "86400",
    "AUTH_PASSWORD_RESET_TTL_SECONDS": "1800",
    "AUTH_LOGIN_MAX_FAILURES": "10",
    "AUTH_LOGIN_FAILURE_WINDOW_SECONDS": "900",
    "AUTH_LOGIN_LOCKOUT_SECONDS": "900",
    "AUTH_COOKIE_SECURE": "false",
    "FRONTEND_BASE_URL": "http://localhost:3000",
}


@pytest.fixture
def env(monkeypatch):
    for name, value in REQUIRED.items():
        monkeypatch.setenv(name, value)
    return monkeypatch


@pytest.mark.parametrize("missing", sorted(REQUIRED))
def test_falla_si_falta_un_parametro_obligatorio(env, missing):
    env.delenv(missing)
    with pytest.raises(ValidationError, match=missing.lower()):
        Settings(_env_file=None)


def test_construye_la_politica_de_sesion_desde_el_entorno(env):
    policy = Settings(_env_file=None).session_policy()
    assert policy.extension == timedelta(seconds=60)
    assert policy.max_extensions_per_question == 1
    assert policy.extension_offer_window == timedelta(seconds=15)
    assert policy.heartbeat_timeout == timedelta(seconds=30)
    assert policy.recovery_window == timedelta(minutes=30)
    assert policy.voluntary_pause_max == timedelta(seconds=30)
    assert policy.voluntary_pauses_per_session == 1


def test_rechaza_valores_no_positivos(env):
    env.setenv("SESSION_EXTENSION_SECONDS", "0")
    with pytest.raises(ValidationError, match="session_extension_seconds"):
        Settings(_env_file=None)


def test_rechaza_latido_mayor_o_igual_que_el_timeout(env):
    env.setenv("SESSION_HEARTBEAT_INTERVAL_SECONDS", "30")
    with pytest.raises(ValueError, match="heartbeat_interval"):
        Settings(_env_file=None).session_policy()


def test_construye_la_politica_de_autenticacion_desde_el_entorno(env):
    settings = Settings(_env_file=None)
    policy = settings.auth_policy()
    assert policy.password_min_length == 12
    assert policy.session_idle_timeout == timedelta(days=7)
    assert policy.session_max_age == timedelta(days=30)
    assert policy.email_verification_ttl == timedelta(hours=24)
    assert policy.password_reset_ttl == timedelta(minutes=30)
    assert policy.login_max_failures == 10
    assert policy.login_failure_window == timedelta(minutes=15)
    assert policy.login_lockout == timedelta(minutes=15)
    assert settings.frontend_origin == "http://localhost:3000"


def test_rechaza_inactividad_mayor_que_la_duracion_maxima(env):
    env.setenv("AUTH_SESSION_IDLE_TIMEOUT_SECONDS", "2592001")
    with pytest.raises(ValueError, match="session_idle_timeout"):
        Settings(_env_file=None).auth_policy()

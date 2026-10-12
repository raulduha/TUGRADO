from datetime import timedelta

import pytest

from app.auth.passwords import (
    PasswordPolicyError,
    hash_password,
    validate_password,
    verify_password,
)
from app.auth.policy import AuthPolicy

POLICY = AuthPolicy(
    password_min_length=12,
    password_max_length=128,
    session_idle_timeout=timedelta(days=7),
    session_max_age=timedelta(days=30),
    email_verification_ttl=timedelta(hours=24),
    password_reset_ttl=timedelta(minutes=30),
    login_max_failures=10,
    login_failure_window=timedelta(minutes=15),
    login_lockout=timedelta(minutes=15),
)


def code(password: str) -> str | None:
    try:
        validate_password(password, POLICY)
    except PasswordPolicyError as exc:
        return exc.code
    return None


def test_11_caracteres_se_rechaza_y_12_se_acepta():
    assert code("tribunal-ab") == "password_too_short"
    assert code("tribunal-abc") is None


def test_sin_reglas_de_composicion():
    assert code("solo minusculas y espacios") is None


def test_largo_maximo():
    assert code("x" * 128 + "tribunal") == "password_too_long"


@pytest.mark.parametrize("password", ["1q2w3e4r5t6y", "1Q2W3E4R5T6Y", "qwertyuiop123"])
def test_contrasenas_comunes_se_rechazan_sin_importar_mayusculas(password):
    assert code(password) == "password_too_common"


def test_hash_argon2id_y_verificacion():
    stored = hash_password("contraseña larga y segura")
    assert stored.startswith("$argon2id$")
    assert verify_password(stored, "contraseña larga y segura")
    assert not verify_password(stored, "otra contraseña cualquiera")
    assert not verify_password(None, "contraseña larga y segura")

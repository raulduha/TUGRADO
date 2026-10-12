"""Política y hash de contraseñas: Argon2id, sin reglas de composición, sin comunes."""

from functools import lru_cache
from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from app.auth.policy import AuthPolicy

_COMMON_PASSWORDS_FILE = Path(__file__).parent / "data" / "common_passwords.txt"
# Parámetros por defecto de argon2-cffi (perfil RFC 9106 de bajo consumo de memoria).
_hasher = PasswordHasher()
# Hash de referencia para igualar el tiempo de respuesta cuando el correo no existe.
_DUMMY_HASH = _hasher.hash("contraseña-de-relleno-para-igualar-tiempos")


class PasswordPolicyError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@lru_cache
def _common_passwords() -> frozenset[str]:
    return frozenset(_COMMON_PASSWORDS_FILE.read_text(encoding="utf-8").split("\n")) - {""}


def validate_password(password: str, policy: AuthPolicy) -> None:
    if len(password) < policy.password_min_length:
        raise PasswordPolicyError(
            "password_too_short",
            f"La contraseña debe tener al menos {policy.password_min_length} caracteres",
        )
    if len(password) > policy.password_max_length:
        raise PasswordPolicyError(
            "password_too_long",
            f"La contraseña no puede superar {policy.password_max_length} caracteres",
        )
    if password.lower() in _common_passwords():
        raise PasswordPolicyError(
            "password_too_common", "Esa contraseña es demasiado común; elige otra"
        )


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str | None, password: str) -> bool:
    """Verifica la contraseña. Con `password_hash=None` gasta el mismo tiempo y devuelve False."""
    try:
        return _hasher.verify(password_hash or _DUMMY_HASH, password) and password_hash is not None
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def needs_rehash(password_hash: str) -> bool:
    return _hasher.check_needs_rehash(password_hash)

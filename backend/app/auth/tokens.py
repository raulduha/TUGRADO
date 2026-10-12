import hashlib
import secrets


def new_token() -> str:
    """Token aleatorio para cookies y enlaces de un solo uso (256 bits)."""
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    # En la base de datos solo se guarda el hash: una filtración no permite usar los tokens.
    return hashlib.sha256(token.encode()).hexdigest()

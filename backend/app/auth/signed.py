"""Valores firmados con HMAC para cookies de corta duración (estado del ingreso con Google)."""

import base64
import hashlib
import hmac
import json
from datetime import datetime


class InvalidSignedValue(Exception):
    pass


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def sign(payload: dict, secret: str, expires_at: datetime) -> str:
    body = _b64(json.dumps({**payload, "exp": int(expires_at.timestamp())}).encode())
    mac = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{mac}"


def unsign(value: str | None, secret: str, now: datetime) -> dict:
    if not value or "." not in value:
        raise InvalidSignedValue("vacío o malformado")
    body, mac = value.rsplit(".", 1)
    expected = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, mac):
        raise InvalidSignedValue("firma inválida")
    try:
        payload = json.loads(_unb64(body))
    except (ValueError, json.JSONDecodeError) as exc:
        raise InvalidSignedValue("contenido inválido") from exc
    if int(payload.get("exp", 0)) <= int(now.timestamp()):
        raise InvalidSignedValue("vencido")
    return payload

"""Verificación de la firma de los webhooks de Mercado Pago (Gate 11b, AC-039).

Replica `mercadopago.webhook.WebhookSignatureValidator` del SDK oficial de Python (MIT):
HMAC-SHA256 del manifiesto `id:{data.id};request-id:{x-request-id};ts:{ts};` con la clave
secreta de la aplicación, comparado en tiempo constante con `v1` del encabezado
`x-signature` (`ts=<ts>,v1=<hex>`). Los pares vacíos se omiten del manifiesto.
"""

import hashlib
import hmac
import re

_VERSION_KEY = re.compile(r"^v\d+$")


class InvalidSignature(Exception):
    pass


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text or None


def _parse(header: str) -> tuple[str | None, dict[str, str]]:
    ts, hashes = None, {}
    for part in header.split(","):
        if "=" not in part:
            continue
        key, value = (piece.strip() for piece in part.split("=", 1))
        key = key.lower()
        if not key or not value:
            continue
        if key == "ts":
            ts = value
        elif _VERSION_KEY.match(key):
            hashes[key] = value
    return ts, hashes


def build_manifest(data_id: str | None, request_id: str | None, ts: str) -> str:
    parts = []
    if data_id:
        parts.append(f"id:{data_id}")
    if request_id:
        parts.append(f"request-id:{request_id}")
    parts.append(f"ts:{ts}")
    return ";".join(parts) + ";"


def sign(secret: str, data_id: str | None, request_id: str | None, ts: str) -> str:
    manifest = build_manifest(data_id, request_id, ts)
    return hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()


def verify(
    x_signature: str | None, x_request_id: str | None, data_id: str | None, secret: str
) -> None:
    """Lanza InvalidSignature si la notificación no fue firmada con `secret`."""
    header = _normalize(x_signature)
    if header is None:
        raise InvalidSignature("falta x-signature")
    ts, hashes = _parse(header)
    if ts is None or not ts.isdigit():
        raise InvalidSignature("x-signature sin ts válido")
    received = hashes.get("v1")
    if received is None:
        raise InvalidSignature("x-signature sin v1")
    expected = sign(secret, _normalize(data_id), _normalize(x_request_id), ts)
    if not hmac.compare_digest(expected, received):
        raise InvalidSignature("firma no coincide")

"""Envío de correos detrás de una interfaz. El proveedor de producción está pendiente (README)."""

import logging
from dataclasses import dataclass
from typing import Protocol

import httpx

logger = logging.getLogger("tugrado.email")


@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    body: str
    # Versión HTML opcional; `body` es siempre la versión de texto plano.
    html: str | None = None


class EmailSender(Protocol):
    def send(self, message: EmailMessage) -> None: ...


class ConsoleEmailSender:
    """Solo para desarrollo: escribe el correo en el log en lugar de enviarlo."""

    def send(self, message: EmailMessage) -> None:
        logger.warning(
            "Correo de desarrollo\nPara: %s\nAsunto: %s\n\n%s",
            message.to,
            message.subject,
            message.body,
        )


class EmailDeliveryError(Exception):
    """El proveedor no aceptó el correo. El mensaje no incluye la clave ni el destinatario."""


class ResendEmailSender:
    """Envío real con la API de Resend (`POST /emails`)."""

    API = "https://api.resend.com"

    def __init__(self, api_key: str, from_address: str, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(base_url=self.API, timeout=10)
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._from = from_address

    def send(self, message: EmailMessage) -> None:
        body = {
            "from": self._from,
            "to": [message.to],
            "subject": message.subject,
            "text": message.body,
        }
        if message.html:
            body["html"] = message.html
        try:
            response = self._client.post("/emails", json=body, headers=self._headers)
        except httpx.HTTPError as exc:
            raise EmailDeliveryError(f"Resend no respondió: {type(exc).__name__}") from exc
        if response.status_code >= 400:
            raise EmailDeliveryError(f"Resend respondió {response.status_code}")

"""Envío de correos detrás de una interfaz. El proveedor de producción está pendiente (README)."""

import logging
from dataclasses import dataclass
from typing import Protocol

logger = logging.getLogger("tugrado.email")


@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    body: str


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

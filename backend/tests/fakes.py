"""Dobles de prueba compartidos."""

import re
import threading
from datetime import datetime, timedelta

from app.auth.email import EmailMessage
from tests.domain.conftest import T0


class FakeClock:
    """Hora controlada por la prueba, en segundos desde T0. Segura entre hilos."""

    def __init__(self, seconds: float = 0) -> None:
        self.now = T0 + timedelta(seconds=seconds)
        self._lock = threading.Lock()

    def set(self, seconds: float) -> None:
        with self._lock:
            self.now = T0 + timedelta(seconds=seconds)

    def advance(self, seconds: float) -> None:
        with self._lock:
            self.now += timedelta(seconds=seconds)

    def __call__(self) -> datetime:
        with self._lock:
            return self.now


class Outbox:
    """Guarda los correos en memoria en lugar de enviarlos."""

    def __init__(self) -> None:
        self.messages: list[EmailMessage] = []

    def send(self, message: EmailMessage) -> None:
        self.messages.append(message)

    def to(self, address: str) -> list[EmailMessage]:
        return [m for m in self.messages if m.to == address]

    def last_token(self, address: str) -> str:
        match = re.search(r"token=([\w-]+)", self.to(address)[-1].body)
        assert match, "el último correo no tiene enlace con token"
        return match.group(1)

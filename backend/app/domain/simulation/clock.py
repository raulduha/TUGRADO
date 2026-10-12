from datetime import datetime, timedelta


class Stopwatch:
    """Cronómetro acumulativo: suma el tiempo de los tramos en que estuvo corriendo."""

    def __init__(self) -> None:
        self._used = timedelta(0)
        self._running_since: datetime | None = None

    @classmethod
    def restored(cls, accumulated: timedelta, running_since: datetime | None) -> "Stopwatch":
        clock = cls()
        clock._used = accumulated
        clock._running_since = running_since
        return clock

    @property
    def accumulated(self) -> timedelta:
        """Tiempo acumulado en tramos ya cerrados (sin el tramo en curso)."""
        return self._used

    @property
    def running(self) -> bool:
        return self._running_since is not None

    @property
    def running_since(self) -> datetime | None:
        return self._running_since

    def used(self, at: datetime) -> timedelta:
        if self._running_since is None:
            return self._used
        return self._used + max(timedelta(0), at - self._running_since)

    def start(self, at: datetime) -> None:
        if self._running_since is None:
            self._running_since = at

    def stop(self, at: datetime) -> None:
        # Una parada retroactiva anterior al arranque no descuenta tiempo negativo.
        if self._running_since is not None:
            self._used += max(timedelta(0), at - self._running_since)
            self._running_since = None

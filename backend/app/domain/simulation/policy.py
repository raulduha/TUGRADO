from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class SessionPolicy:
    """Reglas de tiempo de la simulación. Los valores vienen de la configuración (README).

    Se copia en cada sesión al crearla: cambiarla después no altera sesiones existentes.
    """

    extension: timedelta
    max_extensions_per_question: int
    extension_offer_window: timedelta
    heartbeat_interval: timedelta
    heartbeat_timeout: timedelta
    recovery_window: timedelta
    voluntary_pause_max: timedelta
    voluntary_pauses_per_session: int

    def __post_init__(self) -> None:
        for name in (
            "extension",
            "extension_offer_window",
            "heartbeat_interval",
            "heartbeat_timeout",
            "recovery_window",
            "voluntary_pause_max",
        ):
            if getattr(self, name) <= timedelta(0):
                raise ValueError(f"{name} debe ser positivo")
        if self.max_extensions_per_question < 0 or self.voluntary_pauses_per_session < 0:
            raise ValueError("los máximos no pueden ser negativos")
        if self.heartbeat_interval >= self.heartbeat_timeout:
            raise ValueError("heartbeat_interval debe ser menor que heartbeat_timeout")


@dataclass(frozen=True)
class SimulationTimeConfig:
    """Parte temporal de la configuración congelada de una simulación (AC-005)."""

    total_limit: timedelta
    question_limit: timedelta
    question_count: int

    def __post_init__(self) -> None:
        if self.total_limit <= timedelta(0) or self.question_limit <= timedelta(0):
            raise ValueError("los límites de tiempo deben ser positivos")
        if self.question_count < 1:
            raise ValueError("la simulación debe tener al menos una pregunta")

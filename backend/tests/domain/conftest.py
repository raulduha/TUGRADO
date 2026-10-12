from datetime import UTC, datetime, timedelta

import pytest

from app.domain.simulation.policy import SessionPolicy, SimulationTimeConfig
from app.domain.simulation.session import (
    TERMINAL_SESSION_STATES,
    SessionRuleError,
    SimulationSession,
)

T0 = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def at(seconds: float) -> datetime:
    """Instante T0 + `seconds`."""
    return T0 + timedelta(seconds=seconds)


def secs(value: float) -> timedelta:
    return timedelta(seconds=value)


def make_policy(**overrides) -> SessionPolicy:
    # Valores confirmados en el README, inyectados explícitamente (Gate 3).
    values = dict(
        extension=secs(60),
        max_extensions_per_question=1,
        extension_offer_window=secs(15),
        heartbeat_interval=secs(10),
        heartbeat_timeout=secs(30),
        recovery_window=timedelta(minutes=30),
        voluntary_pause_max=secs(30),
        voluntary_pauses_per_session=1,
    )
    values.update(overrides)
    return SessionPolicy(**values)


def make_session(total=600, question=120, count=3, **policy_overrides) -> SimulationSession:
    config = SimulationTimeConfig(
        total_limit=secs(total), question_limit=secs(question), question_count=count
    )
    session = SimulationSession(config, make_policy(**policy_overrides))
    session.start(at(0))
    return session


def keep_alive(session: SimulationSession, until: float, step: float = 10) -> None:
    """Latidos cada `step` segundos desde el último contacto hasta `until` (inclusive).

    Se detiene sin error si la sesión se cierra por tiempo en el camino.
    """
    t = (session.last_seen - T0).total_seconds()
    while session.state not in TERMINAL_SESSION_STATES:
        t = min(t + step, until)
        try:
            session.heartbeat(at(t))
        except SessionRuleError as exc:
            # El latido consolida el cierre por tiempo y luego se rechaza: es lo esperado.
            assert exc.code == "session_closed"
        if t >= until:
            break


@pytest.fixture
def session() -> SimulationSession:
    return make_session()

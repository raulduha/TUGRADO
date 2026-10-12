"""Persistencia de la simulación con bloqueo por sesión.

Cada operación se ejecuta en una transacción que bloquea la fila de la sesión
(`SELECT ... FOR UPDATE`). Así, dos solicitudes concurrentes sobre la misma sesión se
serializan y la segunda ve el estado que dejó la primera (Gate 3, AC-011).
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from app.domain.simulation.clock import Stopwatch
from app.domain.simulation.policy import SessionPolicy, SimulationTimeConfig
from app.domain.simulation.session import (
    QuestionAttempt,
    SessionEvent,
    SessionRuleError,
    SimulationSession,
)
from app.persistence.simulation_models import (
    QuestionAttemptRow,
    SessionEventRow,
    SessionRequestRow,
    SimulationSessionRow,
)


class SessionNotFound(Exception):
    pass


# ------------------------------------------------- resultados de request_id en JSON


def _encode_result(value: Any) -> dict[str, Any]:
    if value is None:
        return {"type": "none"}
    if isinstance(value, bool):
        raise TypeError("tipo de resultado no soportado: bool")
    if isinstance(value, int):
        return {"type": "int", "value": value}
    if isinstance(value, timedelta):
        return {"type": "timedelta", "value": value.total_seconds()}
    if isinstance(value, datetime):
        return {"type": "datetime", "value": value.isoformat()}
    raise TypeError(f"tipo de resultado no soportado: {type(value).__name__}")


def _decode_result(data: dict[str, Any]) -> Any:
    kind = data["type"]
    if kind == "none":
        return None
    if kind == "int":
        return data["value"]
    if kind == "timedelta":
        return timedelta(seconds=data["value"])
    if kind == "datetime":
        return datetime.fromisoformat(data["value"])
    raise ValueError(f"tipo de resultado desconocido: {kind}")


# --------------------------------------------------------------------- mapeo


def _to_domain(
    row: SimulationSessionRow, events: list[SessionEventRow], requests: list[SessionRequestRow]
) -> SimulationSession:
    config = SimulationTimeConfig(
        total_limit=row.total_limit,
        question_limit=row.question_limit,
        question_count=row.question_count,
    )
    policy = SessionPolicy(
        extension=row.policy_extension,
        max_extensions_per_question=row.policy_max_extensions_per_question,
        extension_offer_window=row.policy_extension_offer_window,
        heartbeat_interval=row.policy_heartbeat_interval,
        heartbeat_timeout=row.policy_heartbeat_timeout,
        recovery_window=row.policy_recovery_window,
        voluntary_pause_max=row.policy_voluntary_pause_max,
        voluntary_pauses_per_session=row.policy_voluntary_pauses_per_session,
    )
    session = SimulationSession(config, policy)
    session.state = row.state
    session.resume_state = row.resume_state
    session.total_clock = Stopwatch.restored(row.total_accumulated, row.total_running_since)
    session.last_seen = row.last_seen
    session.paused_at = row.paused_at
    session.voluntary_pause_started_at = row.voluntary_pause_started_at
    session.voluntary_pauses_used = row.voluntary_pauses_used
    session.committed_at = row.committed_at
    session.last_operation_at = row.last_operation_at
    session.attempts = [
        QuestionAttempt(
            order=a.order,
            started_at=a.started_at,
            limit=a.limit,
            state=a.state,
            clock=Stopwatch.restored(a.clock_accumulated, a.clock_running_since),
            extensions_granted=a.extensions_granted,
            answer_received_at=a.answer_received_at,
        )
        for a in row.attempts
    ]
    session.events = [SessionEvent(type=e.type, at=e.at, data=e.data) for e in events]
    session.request_results = {r.request_id: _decode_result(r.result) for r in requests}
    return session


def _write_session_fields(row: SimulationSessionRow, session: SimulationSession) -> None:
    row.state = session.state
    row.resume_state = session.resume_state
    row.total_accumulated = session.total_clock.accumulated
    row.total_running_since = session.total_clock.running_since
    row.last_seen = session.last_seen
    row.paused_at = session.paused_at
    row.voluntary_pause_started_at = session.voluntary_pause_started_at
    row.voluntary_pauses_used = session.voluntary_pauses_used
    row.committed_at = session.committed_at
    row.last_operation_at = session.last_operation_at


def _write_attempt_fields(row: QuestionAttemptRow, attempt: QuestionAttempt) -> None:
    row.state = attempt.state
    row.started_at = attempt.started_at
    row.limit = attempt.limit
    row.clock_accumulated = attempt.clock.accumulated
    row.clock_running_since = attempt.clock.running_since
    row.extensions_granted = attempt.extensions_granted
    row.answer_received_at = attempt.answer_received_at


# ---------------------------------------------------------------- repositorio


@dataclass
class _Loaded:
    row: SimulationSessionRow
    domain: SimulationSession
    persisted_events: int
    persisted_requests: set[str]


class SimulationSessionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, session_id: uuid.UUID, student_id: uuid.UUID, session: SimulationSession) -> None:
        policy = session.policy
        row = SimulationSessionRow(
            id=session_id,
            student_id=student_id,
            total_limit=session.config.total_limit,
            question_limit=session.config.question_limit,
            question_count=session.config.question_count,
            policy_extension=policy.extension,
            policy_max_extensions_per_question=policy.max_extensions_per_question,
            policy_extension_offer_window=policy.extension_offer_window,
            policy_heartbeat_interval=policy.heartbeat_interval,
            policy_heartbeat_timeout=policy.heartbeat_timeout,
            policy_recovery_window=policy.recovery_window,
            policy_voluntary_pause_max=policy.voluntary_pause_max,
            policy_voluntary_pauses_per_session=policy.voluntary_pauses_per_session,
        )
        _write_session_fields(row, session)
        self.db.add(row)
        self.db.flush()
        self.save(_Loaded(row=row, domain=session, persisted_events=0, persisted_requests=set()))

    def lock(self, session_id: uuid.UUID) -> _Loaded:
        """Carga la sesión bloqueando su fila hasta el fin de la transacción."""
        row = self.db.scalars(
            select(SimulationSessionRow)
            .where(SimulationSessionRow.id == session_id)
            .with_for_update()
        ).one_or_none()
        if row is None:
            raise SessionNotFound(str(session_id))
        events = list(
            self.db.scalars(
                select(SessionEventRow)
                .where(SessionEventRow.session_id == session_id)
                .order_by(SessionEventRow.seq)
            )
        )
        requests = list(
            self.db.scalars(
                select(SessionRequestRow).where(SessionRequestRow.session_id == session_id)
            )
        )
        return _Loaded(
            row=row,
            domain=_to_domain(row, events, requests),
            persisted_events=len(events),
            persisted_requests={r.request_id for r in requests},
        )

    def save(self, loaded: _Loaded) -> None:
        session, row = loaded.domain, loaded.row
        _write_session_fields(row, session)

        existing = {a.order: a for a in row.attempts}
        for attempt in session.attempts:
            attempt_row = existing.get(attempt.order)
            if attempt_row is None:
                attempt_row = QuestionAttemptRow(session_id=row.id, order=attempt.order)
                row.attempts.append(attempt_row)
            _write_attempt_fields(attempt_row, attempt)

        # Los eventos son de solo adición: se insertan los nuevos, nunca se reescriben.
        for seq, event in enumerate(
            session.events[loaded.persisted_events :], start=loaded.persisted_events
        ):
            self.db.add(
                SessionEventRow(
                    session_id=row.id, seq=seq, type=event.type, at=event.at, data=event.data
                )
            )
        loaded.persisted_events = len(session.events)

        for request_id, result in session.request_results.items():
            if request_id not in loaded.persisted_requests:
                self.db.add(
                    SessionRequestRow(
                        session_id=row.id, request_id=request_id, result=_encode_result(result)
                    )
                )
                loaded.persisted_requests.add(request_id)
        self.db.flush()


def run_locked[T](
    engine: Engine,
    session_id: uuid.UUID,
    operation: Callable[[SimulationSession, datetime], T],
    clock: Callable[[], datetime],
) -> T:
    """Ejecuta `operation` sobre la sesión bloqueada y guarda el resultado.

    La hora se toma después de obtener el bloqueo, para que las operaciones de una sesión
    lleguen al dominio en orden temporal. Si el dominio rechaza la operación
    (`SessionRuleError`), igual se guardan las transiciones que aplicó antes de rechazarla
    (por ejemplo, una pausa por desconexión detectada) y luego se propaga el error.
    """
    # Cualquier otra excepción sale sin commit: al cerrar la sesión se hace rollback.
    with Session(engine) as db:
        repo = SimulationSessionRepository(db)
        loaded = repo.lock(session_id)
        try:
            result = operation(loaded.domain, clock())
        except SessionRuleError:
            repo.save(loaded)
            db.commit()
            raise
        repo.save(loaded)
        db.commit()
        return result


def create_session(
    engine: Engine, session_id: uuid.UUID, student_id: uuid.UUID, session: SimulationSession
) -> None:
    with Session(engine) as db:
        SimulationSessionRepository(db).add(session_id, student_id, session)
        db.commit()

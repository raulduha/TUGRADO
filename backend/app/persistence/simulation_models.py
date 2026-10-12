"""Tablas de la simulación. El mapeo con el dominio está en `simulation_repository.py`."""

import uuid
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Interval,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.simulation.session import AttemptState, SessionState
from app.persistence.base import Base


def _enum(enum_cls: type) -> Enum:
    # Se guarda el valor (`in_progress`), no el nombre del miembro. La restricción CHECK se
    # declara aparte con `_enum_check` para que Alembic no la duplique.
    return Enum(
        enum_cls,
        native_enum=False,
        create_constraint=False,
        length=40,
        values_callable=lambda e: [m.value for m in e],
    )


def _enum_check(column: str, enum_cls: type, name: str) -> CheckConstraint:
    values = ", ".join(f"'{m.value}'" for m in enum_cls)
    return CheckConstraint(f"{column} IN ({values})", name=name)


class SimulationSessionRow(Base):
    __tablename__ = "simulation_session"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    # TODO(FK): referenciará a la tabla de usuarios cuando exista.
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True)
    state: Mapped[SessionState] = mapped_column(_enum(SessionState))
    resume_state: Mapped[SessionState | None] = mapped_column(_enum(SessionState))

    # Configuración temporal congelada (AC-005).
    total_limit: Mapped[timedelta] = mapped_column(Interval)
    question_limit: Mapped[timedelta] = mapped_column(Interval)
    question_count: Mapped[int] = mapped_column(Integer)

    # Política congelada al crear la sesión.
    policy_extension: Mapped[timedelta] = mapped_column(Interval)
    policy_max_extensions_per_question: Mapped[int] = mapped_column(Integer)
    policy_extension_offer_window: Mapped[timedelta] = mapped_column(Interval)
    policy_heartbeat_interval: Mapped[timedelta] = mapped_column(Interval)
    policy_heartbeat_timeout: Mapped[timedelta] = mapped_column(Interval)
    policy_recovery_window: Mapped[timedelta] = mapped_column(Interval)
    policy_voluntary_pause_max: Mapped[timedelta] = mapped_column(Interval)
    policy_voluntary_pauses_per_session: Mapped[int] = mapped_column(Integer)

    # Estado de los relojes y del ciclo de vida.
    total_accumulated: Mapped[timedelta] = mapped_column(Interval)
    total_running_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    paused_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    voluntary_pause_started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    voluntary_pauses_used: Mapped[int] = mapped_column(Integer)
    committed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_operation_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    attempts: Mapped[list["QuestionAttemptRow"]] = relationship(
        order_by="QuestionAttemptRow.order", cascade="all, delete-orphan"
    )

    __table_args__ = (
        _enum_check("state", SessionState, "state_valid"),
        _enum_check("resume_state", SessionState, "resume_state_valid"),
        CheckConstraint("question_count >= 1", name="question_count_positive"),
        CheckConstraint("voluntary_pauses_used >= 0", name="voluntary_pauses_used_non_negative"),
    )


class QuestionAttemptRow(Base):
    __tablename__ = "question_attempt"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("simulation_session.id", ondelete="CASCADE"), primary_key=True
    )
    order: Mapped[int] = mapped_column(Integer, primary_key=True)
    # TODO(FK): versión de pregunta presentada, cuando exista el contenido versionado.
    state: Mapped[AttemptState] = mapped_column(_enum(AttemptState))
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    limit: Mapped[timedelta] = mapped_column(Interval)
    clock_accumulated: Mapped[timedelta] = mapped_column(Interval)
    clock_running_since: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    extensions_granted: Mapped[int] = mapped_column(Integer)
    answer_received_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        _enum_check("state", AttemptState, "state_valid"),
        CheckConstraint('"order" >= 1', name="order_positive"),
        CheckConstraint("extensions_granted >= 0", name="extensions_granted_non_negative"),
    )


class SessionEventRow(Base):
    """Registro auditable de solo adición."""

    __tablename__ = "session_event"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("simulation_session.id", ondelete="CASCADE"), index=True
    )
    # Posición en la secuencia de la sesión; la unicidad impide escrituras concurrentes perdidas.
    seq: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(60))
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    data: Mapped[dict[str, Any]] = mapped_column(JSONB)

    __table_args__ = (UniqueConstraint("session_id", "seq", name="uq_session_event_session_seq"),)


class SessionRequestRow(Base):
    """Resultado de cada request_id aceptado, para responder igual a los duplicados."""

    __tablename__ = "session_request"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("simulation_session.id", ondelete="CASCADE"), primary_key=True
    )
    request_id: Mapped[str] = mapped_column(String(100), primary_key=True)
    result: Mapped[dict[str, Any]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

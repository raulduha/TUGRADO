"""Hábito de estudio: días con actividad (rachas, FR-033), recordatorios por correo (FR-034) y
plan diario: fecha del examen y meta de preguntas (FR-035)."""

import uuid
from datetime import date, datetime

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base


class ActivityDayRow(Base):
    """Un registro por estudiante y día (hora de Chile) en que entró a la app."""

    __tablename__ = "activity_day"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)


class ReminderStateRow(Base):
    """Recordatorios de cada estudiante: último envío y baja.

    `unsubscribe_token` se guarda en claro a propósito: solo permite darse de baja de estos
    recordatorios y así el enlace de cualquier correo anterior sigue sirviendo."""

    __tablename__ = "reminder_state"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    unsubscribe_token: Mapped[str] = mapped_column(String(64), unique=True)
    last_sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    opted_out_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class StudyProfileRow(Base):
    """Plan diario del estudiante: la fecha de su examen y cuántas preguntas quiere responder al
    día. Ambos son opcionales hasta que el estudiante los configura."""

    __tablename__ = "study_profile"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    exam_date: Mapped[date | None] = mapped_column(Date)
    daily_goal: Mapped[int | None] = mapped_column(Integer)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "daily_goal IS NULL OR daily_goal BETWEEN 1 AND 200", name="daily_goal_range"
        ),
    )


class RankingProfileRow(Base):
    """Participación voluntaria en el ranking mensual (FR-039): quien no tiene fila no aparece.
    En el ranking se muestra solo el apodo, nunca el correo ni el nombre."""

    __tablename__ = "ranking_profile"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    alias: Mapped[str] = mapped_column(String(24))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (Index("uq_ranking_profile_alias", text("lower(alias)"), unique=True),)

"""Días con actividad (rachas, FR-033) y estado de los recordatorios por correo (FR-034)."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
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

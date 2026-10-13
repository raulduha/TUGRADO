"""Días con actividad de cada estudiante, para las rachas (FR-033)."""

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base


class ActivityDayRow(Base):
    """Un registro por estudiante y día (hora de Chile) en que entró a la app."""

    __tablename__ = "activity_day"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    day: Mapped[date] = mapped_column(Date, primary_key=True)

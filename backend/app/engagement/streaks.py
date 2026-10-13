"""Rachas de días seguidos (FR-033). El cálculo es puro; el registro es idempotente."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.persistence.engagement_models import ActivityDayRow


@dataclass(frozen=True)
class Streak:
    current: int
    best: int
    # True solo en la primera visita del día: el frontend celebra una vez.
    new_today: bool
    # Últimos 7 días, del más antiguo a hoy: si hubo actividad.
    week: list[bool]


def compute(days: set[date], today: date) -> tuple[int, int]:
    """Racha actual (días seguidos que terminan hoy) y mejor racha histórica."""
    current = 0
    cursor = today
    while cursor in days:
        current += 1
        cursor -= timedelta(days=1)
    best = 0
    for day in days:
        if day - timedelta(days=1) in days:
            continue  # no es el inicio de una racha
        length = 0
        while day + timedelta(days=length) in days:
            length += 1
        best = max(best, length)
    return current, best


def check_in(db: Session, user_id: uuid.UUID, today: date) -> Streak:
    """Registra la actividad de hoy (una sola vez) y devuelve la racha."""
    inserted = db.execute(
        insert(ActivityDayRow)
        .values(user_id=user_id, day=today)
        .on_conflict_do_nothing()
        .returning(ActivityDayRow.day)
    ).first()
    db.commit()
    days = set(db.scalars(select(ActivityDayRow.day).where(ActivityDayRow.user_id == user_id)))
    current, best = compute(days, today)
    week = [today - timedelta(days=offset) in days for offset in range(6, -1, -1)]
    return Streak(current=current, best=best, new_today=inserted is not None, week=week)

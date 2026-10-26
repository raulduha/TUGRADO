"""Ranking mensual voluntario (FR-039, AC-051).

Solo aparece quien se inscribe con un apodo, y el ranking muestra únicamente ese apodo. Ordena
por la experiencia del mes en curso (hora de Chile): 10 XP por respuesta correcta, la misma
regla de la ruta. Mide constancia de práctica, no promete aprobar el examen.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.clock import CHILE
from app.content.path import XP_PER_CORRECT
from app.errors import AppError
from app.persistence.content_models import PracticeAttemptRow
from app.persistence.engagement_models import RankingProfileRow

TOP = 20
ALIAS = re.compile(r"^[\wÁÉÍÓÚÜÑáéíóúüñ][\wÁÉÍÓÚÜÑáéíóúüñ .-]{1,22}[\wÁÉÍÓÚÜÑáéíóúüñ]$")


@dataclass(frozen=True)
class Entry:
    position: int
    alias: str
    xp: int
    me: bool


@dataclass(frozen=True)
class Ranking:
    entries: list[Entry]
    me: Entry | None  # None si no participa
    alias: str | None


def join(db: Session, user_id: uuid.UUID, alias: str, now: datetime) -> None:
    alias = " ".join(alias.split())
    if not ALIAS.match(alias) or "@" in alias:
        raise AppError(
            "invalid_alias", "El apodo debe tener entre 3 y 24 letras, números, espacios o . -"
        )
    row = db.get(RankingProfileRow, user_id) or RankingProfileRow(user_id=user_id, joined_at=now)
    row.alias = alias
    db.add(row)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise AppError("alias_taken", "Ese apodo ya lo usa otra persona") from error


def leave(db: Session, user_id: uuid.UUID) -> None:
    row = db.get(RankingProfileRow, user_id)
    if row is not None:
        db.delete(row)
        db.commit()


def monthly(db: Session, user_id: uuid.UUID, now: datetime) -> Ranking:
    local = now.astimezone(CHILE)
    month_start = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    correct = (
        select(PracticeAttemptRow.user_id, func.count().label("correct"))
        .where(PracticeAttemptRow.correct.is_(True), PracticeAttemptRow.answered_at >= month_start)
        .group_by(PracticeAttemptRow.user_id)
        .subquery()
    )
    rows = db.execute(
        select(RankingProfileRow.user_id, RankingProfileRow.alias, correct.c.correct)
        .outerjoin(correct, correct.c.user_id == RankingProfileRow.user_id)
        .order_by(correct.c.correct.desc().nulls_last(), RankingProfileRow.joined_at)
    ).all()
    entries = [
        Entry(i, alias, (count or 0) * XP_PER_CORRECT, uid == user_id)
        for i, (uid, alias, count) in enumerate(rows, start=1)
    ]
    me = next((e for e in entries if e.me), None)
    return Ranking(entries=entries[:TOP], me=me, alias=me.alias if me else None)

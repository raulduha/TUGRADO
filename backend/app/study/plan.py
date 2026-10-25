"""Plan diario del estudiante (FR-035): fecha del examen, meta de preguntas y avance del día.

La meta sugerida reparte las preguntas que aún no domina entre los días que faltan para el
examen. «Domina» significa que su último intento fue correcto, la misma regla que usan las
estrellas de la ruta y la preparación por cédula.
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.clock import CHILE, chile_date
from app.content.path import latest_outcomes
from app.errors import AppError
from app.persistence.content_models import PracticeAttemptRow, QuestionVersionRow, VersionStatus
from app.persistence.engagement_models import StudyProfileRow
from app.study.review import due_today

# Hasta cuándo puede estar el examen: más allá es casi seguro un error al escribir la fecha.
MAX_HORIZON = timedelta(days=3 * 365)

# La sugerencia nunca baja de este mínimo: menos no alcanza a formar el hábito.
MIN_SUGGESTED_GOAL = 5


@dataclass(frozen=True)
class Today:
    exam_date: date | None
    days_left: int | None  # None sin fecha; 0 el mismo día o si ya pasó
    daily_goal: int | None
    suggested_goal: int | None  # None sin fecha de examen
    answered_today: int
    review_due: int
    remaining: int  # preguntas publicadas que aún no domina


def suggested_goal(remaining: int, days_left: int | None) -> int | None:
    if days_left is None:
        return None
    return max(MIN_SUGGESTED_GOAL, math.ceil(remaining / max(days_left, 1)))


def save_profile(
    db: Session,
    user_id: uuid.UUID,
    exam_date: date | None,
    daily_goal: int | None,
    now: datetime,
) -> None:
    today = chile_date(now)
    if exam_date is not None and not today <= exam_date <= today + MAX_HORIZON:
        raise AppError("invalid_exam_date", "La fecha del examen debe estar entre hoy y 3 años más")
    row = db.get(StudyProfileRow, user_id) or StudyProfileRow(user_id=user_id)
    row.exam_date = exam_date
    row.daily_goal = daily_goal
    row.updated_at = now
    db.add(row)
    db.commit()


def today_summary(db: Session, user_id: uuid.UUID, now: datetime) -> Today:
    today = chile_date(now)
    row = db.get(StudyProfileRow, user_id)
    exam_date = row.exam_date if row else None
    days_left = max((exam_date - today).days, 0) if exam_date else None
    published = _published_questions(db)
    mastered = {q for q, correct in latest_outcomes(db, user_id).items() if correct}
    remaining = len(published - mastered)
    return Today(
        exam_date=exam_date,
        days_left=days_left,
        daily_goal=row.daily_goal if row else None,
        suggested_goal=suggested_goal(remaining, days_left),
        answered_today=_answered_on(db, user_id, today),
        review_due=sum(q in published for q in due_today(db, user_id, now)),
        remaining=remaining,
    )


def _answered_on(db: Session, user_id: uuid.UUID, day: date) -> int:
    local_day = func.date(func.timezone(str(CHILE), PracticeAttemptRow.answered_at))
    return (
        db.scalar(
            select(func.count())
            .select_from(PracticeAttemptRow)
            .where(PracticeAttemptRow.user_id == user_id, local_day == day)
        )
        or 0
    )


def _published_questions(db: Session) -> set[uuid.UUID]:
    return set(
        db.scalars(
            select(QuestionVersionRow.question_id).where(
                QuestionVersionRow.status == VersionStatus.PUBLISHED
            )
        )
    )

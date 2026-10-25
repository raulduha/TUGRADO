"""Repaso espaciado de los errores (FR-035).

Una pregunta entra al repaso cuando el estudiante la falla. Vuelve al día siguiente; cada vez que
la acierta en el repaso, el siguiente espera más (3, 7 y 14 días), y tras acertarla cuatro veces
seguidas sale del repaso. Si la vuelve a fallar, empieza de nuevo. Todo se calcula a partir de
las respuestas registradas (practice_attempt), en días de Chile.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.clock import chile_date
from app.persistence.content_models import PracticeAttemptRow, QuestionVersionRow

# Días de espera según cuántas veces seguidas se acertó desde el último error.
INTERVALS = (1, 3, 7, 14)


@dataclass(frozen=True)
class Attempt:
    question_id: uuid.UUID
    day: date
    correct: bool


def due_questions(attempts: list[Attempt], today: date) -> list[uuid.UUID]:
    """Preguntas que toca repasar hoy, las más atrasadas primero. `attempts` en orden
    cronológico."""
    history: dict[uuid.UUID, list[Attempt]] = {}
    for attempt in attempts:
        history.setdefault(attempt.question_id, []).append(attempt)

    due: list[tuple[date, uuid.UUID]] = []
    for question_id, answers in history.items():
        failures = [i for i, a in enumerate(answers) if not a.correct]
        if not failures:
            continue  # nunca la falló: no entra al repaso
        streak = len(answers) - 1 - failures[-1]  # aciertos seguidos desde el último error
        if streak >= len(INTERVALS):
            continue  # ya la domina
        due_on = answers[-1].day + timedelta(days=INTERVALS[streak])
        if due_on <= today:
            due.append((due_on, question_id))
    return [question_id for _, question_id in sorted(due)]


def user_attempts(db: Session, user_id: uuid.UUID) -> list[Attempt]:
    rows = db.execute(
        select(
            QuestionVersionRow.question_id,
            PracticeAttemptRow.answered_at,
            PracticeAttemptRow.correct,
        )
        .join(QuestionVersionRow, QuestionVersionRow.id == PracticeAttemptRow.version_id)
        .where(PracticeAttemptRow.user_id == user_id)
        .order_by(PracticeAttemptRow.answered_at)
    ).all()
    return [Attempt(question_id, chile_date(at), correct) for question_id, at, correct in rows]


def due_today(db: Session, user_id: uuid.UUID, now: datetime) -> list[uuid.UUID]:
    return due_questions(user_attempts(db, user_id), chile_date(now))

"""Prueba cronometrada y flashcards sobre el banco publicado (FR-037, AC-049).

La prueba entrega las preguntas sin respuesta y corrige todo al final: recién al entregar se
registran las respuestas (cuentan para la ruta, las estrellas y el repaso) y se revelan la
correcta, la explicación y la fuente. El tiempo lo lleva la pantalla y es solo orientativo: la
prueba no tiene consecuencias más allá de la práctica, así que el backend no lo controla.

Las flashcards muestran la respuesta a propósito (son para repasar), y no registran nada.
"""

import random
import uuid
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import SubscribedUser, get_clock
from app.api.practice import PracticeQuestion, question_out
from app.content import queries
from app.content.path import latest_outcomes
from app.db import get_db
from app.persistence.content_models import PracticeAttemptRow
from app.study.review import due_today

router = APIRouter(prefix="/practice", tags=["practice"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]
Subject = Annotated[str | None, Query(max_length=200)]

EXAM_SIZES = (10, 20, 40)


# ------------------------------------------------------------------------- prueba


class ExamAnswer(BaseModel):
    version_id: uuid.UUID
    position: int | None = Field(default=None, ge=0)  # None: la dejó sin responder


class ExamIn(BaseModel):
    answers: list[ExamAnswer] = Field(min_length=1, max_length=max(EXAM_SIZES))


class ExamItem(BaseModel):
    id: str
    chosen: int | None
    correct: bool
    correct_position: int
    explanation: str
    source: str


class SubtopicScore(BaseModel):
    subject: str
    subtopic: str | None
    correct: int
    total: int


class ExamResult(BaseModel):
    correct: int
    total: int
    items: list[ExamItem]
    by_subtopic: list[SubtopicScore]


@router.get("/exam")
def exam_questions(
    _: SubscribedUser,
    db: Db,
    subject: Subject = None,
    size: Annotated[int, Query(ge=1, le=max(EXAM_SIZES))] = 20,
) -> list[PracticeQuestion]:
    """Preguntas publicadas al azar para una prueba, de una materia o de todas."""
    return [question_out(db, view) for view in queries.random_published(db, size, subject)]


@router.post("/exam/grade")
def grade_exam(body: ExamIn, user: SubscribedUser, db: Db, clock: Clock) -> ExamResult:
    """Corrige la prueba completa y registra las respuestas dadas. Las preguntas que dejaron de
    estar publicadas durante la prueba se omiten; las no respondidas cuentan como incorrectas
    pero no se registran como intento."""
    answers = {a.version_id: a.position for a in body.answers}  # sin duplicados
    views = queries.published_by_ids(db, list(answers))
    now = clock()
    items: list[ExamItem] = []
    scores: dict[tuple[str, str | None], SubtopicScore] = {}
    for i, view in enumerate(views):
        version = view.version
        chosen = answers[version.id]
        if chosen is not None and chosen >= len(queries.options(db, version.id)):
            chosen = None  # una alternativa que no existe vale como no respondida
        correct = chosen == version.correct_position
        if chosen is not None:
            db.add(
                PracticeAttemptRow(
                    user_id=user.id,
                    version_id=version.id,
                    chosen_position=chosen,
                    correct=correct,
                    # Horas correlativas: el orden de la prueba es el orden de los intentos.
                    answered_at=now + timedelta(microseconds=i),
                )
            )
        items.append(
            ExamItem(
                id=str(version.id),
                chosen=chosen,
                correct=correct,
                correct_position=version.correct_position,
                explanation=version.explanation,
                source=version.source,
            )
        )
        key = (view.subject, view.subtopic)
        score = scores.setdefault(
            key, SubtopicScore(subject=view.subject, subtopic=view.subtopic, correct=0, total=0)
        )
        score.total += 1
        score.correct += correct
    db.commit()
    return ExamResult(
        correct=sum(item.correct for item in items),
        total=len(items),
        items=items,
        by_subtopic=sorted(scores.values(), key=lambda s: s.correct / s.total),
    )


# ---------------------------------------------------------------------- flashcards


class Flashcard(BaseModel):
    id: str
    subject: str
    subtopic: str | None
    prompt: str
    options: list[str]
    correct_position: int  # la explicación cita las alternativas por letra
    explanation: str
    source: str
    status: Literal["review", "pending", "mastered"]


@router.get("/flashcards")
def flashcards(
    user: SubscribedUser,
    db: Db,
    clock: Clock,
    subject: Subject = None,
    limit: Annotated[int, Query(ge=1, le=50)] = 20,
) -> list[Flashcard]:
    """Tarjetas para repasar: primero los errores que toca repasar hoy, luego las preguntas que
    aún no domina y al final las que ya domina; al azar dentro de cada grupo."""
    views = queries.published_views(db, subject)
    due = set(due_today(db, user.id, clock()))
    outcome = latest_outcomes(db, user.id)

    def status(question_id: uuid.UUID) -> Literal["review", "pending", "mastered"]:
        if question_id in due:
            return "review"
        return "mastered" if outcome.get(question_id) else "pending"

    random.shuffle(views)
    order = {"review": 0, "pending": 1, "mastered": 2}
    views.sort(key=lambda view: order[status(view.version.question_id)])
    cards = []
    for view in views[:limit]:
        version = view.version
        cards.append(
            Flashcard(
                id=str(version.id),
                subject=view.subject,
                subtopic=view.subtopic,
                prompt=version.prompt,
                options=queries.options(db, version.id),
                correct_position=version.correct_position,
                explanation=version.explanation,
                source=version.source,
                status=status(version.question_id),
            )
        )
    return cards

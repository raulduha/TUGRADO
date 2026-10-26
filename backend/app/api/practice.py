"""Práctica de alternativas, ruta de estudio y repaso (FR-006, FR-035, AC-044, AC-045, AC-047).

Solo se usan versiones publicadas, y la respuesta correcta se entrega recién al responder.
"""

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import SubscribedUser, get_clock
from app.content import queries
from app.content.path import Lesson, build_path, find_lesson, total_xp
from app.content.question import ContentError
from app.db import get_db
from app.persistence.content_models import PracticeAttemptRow, QuestionVersionRow, VersionStatus
from app.study.review import due_today

router = APIRouter(prefix="/practice", tags=["practice"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]


class PracticeQuestion(BaseModel):
    id: str
    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    options: list[str]  # sin la respuesta correcta: se revela al responder


class LessonOut(BaseModel):
    id: str
    title: str
    subtopics: list[str]
    total: int
    answered: int
    correct: int
    completed: bool
    stars: int


class LessonDetail(LessonOut):
    subject: str
    questions: list[PracticeQuestion]


class UnitOut(BaseModel):
    subject: str
    lessons: list[LessonOut]
    total: int
    mastered: int  # último intento correcto: la preparación por cédula


class PathOut(BaseModel):
    units: list[UnitOut]
    xp: int


class AnswerIn(BaseModel):
    version_id: uuid.UUID
    position: int = Field(ge=0)


class AnswerOut(BaseModel):
    correct: bool
    correct_position: int
    explanation: str
    source: str


def question_out(db: Session, view: queries.VersionView) -> PracticeQuestion:
    v = view.version
    return PracticeQuestion(
        id=str(v.id),
        subject=view.subject,
        subtopic=view.subtopic,
        difficulty=v.difficulty,
        prompt=v.prompt,
        options=queries.options(db, v.id),
    )


def _lesson(lesson: Lesson) -> LessonOut:
    return LessonOut(
        id=lesson.id,
        title=lesson.title,
        subtopics=lesson.subtopics,
        total=lesson.total,
        answered=lesson.answered,
        correct=lesson.correct,
        completed=lesson.completed,
        stars=lesson.stars,
    )


def _not_found(code: str, message: str) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, detail={"code": code, "message": message})


@router.get("/questions")
def random_questions(
    _: SubscribedUser, db: Db, limit: Annotated[int, Query(ge=1, le=30)] = 10
) -> list[PracticeQuestion]:
    """Práctica libre: preguntas publicadas al azar."""
    return [question_out(db, view) for view in queries.random_published(db, limit)]


@router.get("/path")
def study_path(user: SubscribedUser, db: Db) -> PathOut:
    """La ruta de estudio con el avance del estudiante."""
    return PathOut(
        units=[
            UnitOut(
                subject=unit.subject,
                lessons=[_lesson(lesson) for lesson in unit.lessons],
                total=unit.total,
                mastered=unit.mastered,
            )
            for unit in build_path(db, user.id)
        ],
        xp=total_xp(db, user.id),
    )


@router.get("/review")
def review_questions(
    user: SubscribedUser, db: Db, clock: Clock, limit: Annotated[int, Query(ge=1, le=30)] = 10
) -> list[PracticeQuestion]:
    """Los errores que toca repasar hoy (FR-035), los más atrasados primero."""
    due = due_today(db, user.id, clock())
    return [question_out(db, view) for view in queries.published_for_questions(db, due)[:limit]]


@router.get("/lessons/{lesson_id}")
def lesson_questions(lesson_id: str, user: SubscribedUser, db: Db) -> LessonDetail:
    found = find_lesson(build_path(db, user.id), lesson_id)
    if found is None:
        raise _not_found("lesson_not_found", "Esa lección ya no está disponible")
    unit, lesson = found
    views = queries.published_by_ids(db, lesson.version_ids)
    return LessonDetail(
        **_lesson(lesson).model_dump(),
        subject=unit.subject,
        questions=[question_out(db, view) for view in views],
    )


@router.post("/answers")
def answer(body: AnswerIn, user: SubscribedUser, db: Db, clock: Clock) -> AnswerOut:
    """Registra la respuesta y recién entonces revela la correcta, la explicación y la fuente."""
    version = db.get(QuestionVersionRow, body.version_id)
    if version is None or version.status != VersionStatus.PUBLISHED:
        raise _not_found("question_not_found", "La pregunta ya no está disponible")
    if body.position >= len(queries.options(db, version.id)):
        raise ContentError("invalid_options", "Esa alternativa no existe")
    correct = body.position == version.correct_position
    db.add(
        PracticeAttemptRow(
            user_id=user.id,
            version_id=version.id,
            chosen_position=body.position,
            correct=correct,
            answered_at=clock(),
        )
    )
    db.commit()
    return AnswerOut(
        correct=correct,
        correct_position=version.correct_position,
        explanation=version.explanation,
        source=version.source,
    )

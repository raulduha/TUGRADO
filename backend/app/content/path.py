"""Ruta de estudio tipo Duolingo (FR-006): unidades y lecciones sobre el banco publicado.

Cada materia es una unidad y sus subtemas se agrupan en lecciones cortas, en el orden en que
entraron al banco (así la ruta sigue el orden del temario con que se importó la planilla). Una
lección está completa cuando el estudiante respondió todas sus preguntas; las estrellas dependen
de cuántas acertó en su último intento. El orden y el desbloqueo son solo pedagógicos: el
backend entrega cualquier lección a quien tenga acceso al estudio.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.persistence.content_models import (
    PracticeAttemptRow,
    QuestionRow,
    QuestionVersionRow,
    SubjectRow,
    SubtopicRow,
    VersionStatus,
)

# Preguntas mínimas por lección: se juntan subtemas consecutivos hasta llegar a este número.
LESSON_SIZE = 5
GENERAL = "General"
XP_PER_CORRECT = 10


@dataclass
class Lesson:
    id: str
    title: str
    subtopics: list[str]
    version_ids: list[uuid.UUID] = field(default_factory=list)
    question_ids: list[uuid.UUID] = field(default_factory=list)
    answered: int = 0
    correct: int = 0

    @property
    def total(self) -> int:
        return len(self.version_ids)

    @property
    def completed(self) -> bool:
        return self.total > 0 and self.answered >= self.total

    @property
    def stars(self) -> int:
        if not self.completed:
            return 0
        if self.correct == self.total:
            return 3
        return 2 if self.correct * 5 >= self.total * 4 else 1  # 80 % o más


@dataclass
class Unit:
    subject: str
    lessons: list[Lesson]

    @property
    def total(self) -> int:
        return sum(lesson.total for lesson in self.lessons)

    @property
    def mastered(self) -> int:
        """Preguntas cuyo último intento fue correcto: la preparación por cédula."""
        return sum(lesson.correct for lesson in self.lessons)


def build_path(db: Session, user_id: uuid.UUID | None = None) -> list[Unit]:
    rows = db.execute(
        select(
            QuestionVersionRow.id,
            QuestionVersionRow.question_id,
            SubjectRow.id,
            SubjectRow.name,
            SubtopicRow.id,
            SubtopicRow.name,
            QuestionRow.created_at,
        )
        .join(SubjectRow, SubjectRow.id == QuestionVersionRow.subject_id)
        .outerjoin(SubtopicRow, SubtopicRow.id == QuestionVersionRow.subtopic_id)
        .join(QuestionRow, QuestionRow.id == QuestionVersionRow.question_id)
        .where(QuestionVersionRow.status == VersionStatus.PUBLISHED)
        .order_by(QuestionRow.created_at, QuestionRow.id)
    ).all()

    # materia → subtema → preguntas, en orden de llegada al banco.
    subjects: dict[uuid.UUID, tuple[str, dict[uuid.UUID, tuple[str, list]]]] = {}
    for version_id, question_id, subject_id, subject, subtopic_id, subtopic, _ in rows:
        _, topics = subjects.setdefault(subject_id, (subject, {}))
        key = subtopic_id or subject_id  # sin subtema: un grupo «General» por materia
        _, items = topics.setdefault(key, (subtopic or GENERAL, []))
        items.append((version_id, question_id))

    units = []
    for subject_id, (subject, topics) in subjects.items():
        lessons: list[Lesson] = []
        current: Lesson | None = None
        for key, (name, items) in topics.items():
            if current is None or current.total >= LESSON_SIZE:
                current = Lesson(id=f"{subject_id}.{key}", title=name, subtopics=[])
                lessons.append(current)
            current.subtopics.append(name)
            current.version_ids += [v for v, _ in items]
            current.question_ids += [q for _, q in items]
        # Una última lección muy corta se suma a la anterior.
        if len(lessons) > 1 and lessons[-1].total < LESSON_SIZE // 2 + 1:
            last = lessons.pop()
            lessons[-1].subtopics += last.subtopics
            lessons[-1].version_ids += last.version_ids
            lessons[-1].question_ids += last.question_ids
        units.append(Unit(subject=subject, lessons=lessons))

    if user_id is not None:
        _apply_progress(db, user_id, units)
    return units


def latest_outcomes(db: Session, user_id: uuid.UUID) -> dict[uuid.UUID, bool]:
    """Si acertó el último intento de cada pregunta que respondió (de cualquiera de sus
    versiones). Es la regla de «domina» que usan las estrellas y la preparación por cédula."""
    latest = (
        select(
            QuestionVersionRow.question_id,
            PracticeAttemptRow.correct,
            func.row_number()
            .over(
                partition_by=QuestionVersionRow.question_id,
                order_by=PracticeAttemptRow.answered_at.desc(),
            )
            .label("rank"),
        )
        .join(QuestionVersionRow, QuestionVersionRow.id == PracticeAttemptRow.version_id)
        .where(PracticeAttemptRow.user_id == user_id)
        .subquery()
    )
    return dict(
        db.execute(select(latest.c.question_id, latest.c.correct).where(latest.c.rank == 1)).all()
    )


def _apply_progress(db: Session, user_id: uuid.UUID, units: list[Unit]) -> None:
    outcome = latest_outcomes(db, user_id)
    for unit in units:
        for lesson in unit.lessons:
            results = [outcome[q] for q in lesson.question_ids if q in outcome]
            lesson.answered = len(results)
            lesson.correct = sum(results)


def total_xp(db: Session, user_id: uuid.UUID) -> int:
    correct = db.scalar(
        select(func.count())
        .select_from(PracticeAttemptRow)
        .where(PracticeAttemptRow.user_id == user_id, PracticeAttemptRow.correct.is_(True))
    )
    return (correct or 0) * XP_PER_CORRECT


def find_lesson(units: list[Unit], lesson_id: str) -> tuple[Unit, Lesson] | None:
    for unit in units:
        for lesson in unit.lessons:
            if lesson.id == lesson_id:
                return unit, lesson
    return None

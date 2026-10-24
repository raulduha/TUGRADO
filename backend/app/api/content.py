"""Banco de preguntas: administración (FR-013, FR-014) y práctica de alternativas (FR-006)."""

import uuid
from collections.abc import Callable
from dataclasses import asdict
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

from app.api.deps import AdminUser, SubscribedUser, get_clock
from app.content.importer import parse_workbook
from app.content.path import Lesson, build_path, find_lesson, total_xp
from app.content.service import ContentError, ContentService, QuestionContent
from app.content.workbook import ExportRow, build_workbook
from app.db import get_db
from app.persistence.auth_models import UserAccountRow
from app.persistence.content_models import (
    DIFFICULTY_MAX,
    DIFFICULTY_MIN,
    OPTIONS_MAX,
    OPTIONS_MIN,
    AnswerOptionRow,
    ContentReviewRow,
    PracticeAttemptRow,
    QuestionVersionRow,
    ReviewDecision,
    SubjectRow,
    SubtopicRow,
    VersionStatus,
)

admin_router = APIRouter(prefix="/admin/questions", tags=["content"])
practice_router = APIRouter(prefix="/practice", tags=["practice"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # documentos importables: hasta 25 MB (README)
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def service(db: Db, clock: Clock) -> ContentService:
    return ContentService(db, clock)


Service = Annotated[ContentService, Depends(service)]


# ------------------------------------------------------------------ administración


class ImportOut(BaseModel):
    created: int = 0
    updated: int = 0
    retired: int = 0
    unchanged: int = 0
    errors: list[dict]


@admin_router.post("/import")
async def import_questions(request: Request, admin: AdminUser, svc: Service) -> ImportOut:
    """Recibe el .xlsx como cuerpo binario. Todo o nada: con errores no aplica ninguna fila."""
    data = await request.body()
    if len(data) > MAX_UPLOAD_BYTES:
        raise ContentError("file_too_large", "El archivo supera los 25 MB")
    parsed, errors = parse_workbook(data)
    summary = None
    if not errors:
        summary, errors = svc.apply_workbook(parsed, admin.id)
    if errors or summary is None:
        return ImportOut(errors=[{"row": e.row, "message": e.message} for e in errors])
    return ImportOut(**asdict(summary), errors=[])


def _xlsx(data: bytes, filename: str) -> Response:
    return Response(
        content=data,
        media_type=XLSX,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@admin_router.get("/template")
def download_template(_: AdminUser) -> Response:
    """Planilla vacía, con las columnas e instrucciones."""
    return _xlsx(build_workbook([]), "plantilla-preguntas.xlsx")


@admin_router.get("/export")
def export_questions(_: AdminUser, svc: Service, clock: Clock) -> Response:
    """El banco actual (última versión de cada pregunta no retirada), para editar y resubir."""
    rows = [ExportRow(qid, content, status) for qid, content, status in svc.export_rows()]
    return _xlsx(build_workbook(rows), f"banco-preguntas-{clock():%Y-%m-%d}.xlsx")


class BulkIn(BaseModel):
    action: Literal["submit", "approve", "publish"]
    ids: list[uuid.UUID] = Field(min_length=1, max_length=2000)


class BulkOut(BaseModel):
    done: int
    skipped: list[dict]


@admin_router.post("/bulk")
def bulk_action(body: BulkIn, admin: AdminUser, svc: Service) -> BulkOut:
    """Enviar a revisión, aprobar o publicar varias versiones; las que no pueden, se saltan."""
    done, skipped = svc.bulk(body.action, body.ids, admin.id)
    return BulkOut(done=done, skipped=[{"id": str(i), "message": m} for i, m in skipped])


class VersionSummary(BaseModel):
    id: str
    question_id: str
    number: int
    status: VersionStatus
    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    author: str
    is_author: bool
    created_at: datetime


class ReviewOut(BaseModel):
    decision: ReviewDecision
    comment: str | None
    reviewer: str
    created_at: datetime


class VersionDetail(VersionSummary):
    options: list[str]
    correct_position: int
    explanation: str
    source: str
    reviews: list[ReviewOut]


def _summary_query():
    author = aliased(UserAccountRow)
    return (
        select(QuestionVersionRow, SubjectRow.name, SubtopicRow.name, author.email)
        .join(SubjectRow, SubjectRow.id == QuestionVersionRow.subject_id)
        .outerjoin(SubtopicRow, SubtopicRow.id == QuestionVersionRow.subtopic_id)
        .join(author, author.id == QuestionVersionRow.created_by)
    )


def _summary(row, subject, subtopic, author, me: uuid.UUID) -> dict:
    return {
        "id": str(row.id),
        "question_id": str(row.question_id),
        "number": row.number,
        "status": row.status,
        "subject": subject,
        "subtopic": subtopic,
        "difficulty": row.difficulty,
        "prompt": row.prompt,
        "author": author,
        "is_author": row.created_by == me,
        "created_at": row.created_at,
    }


@admin_router.get("")
def list_versions(
    admin: AdminUser,
    db: Db,
    status_filter: Annotated[VersionStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
) -> list[VersionSummary]:
    query = _summary_query().order_by(QuestionVersionRow.created_at.desc()).limit(limit)
    if status_filter is not None:
        query = query.where(QuestionVersionRow.status == status_filter)
    return [VersionSummary(**_summary(*r, admin.id)) for r in db.execute(query).all()]


@admin_router.get("/{version_id}")
def get_version(version_id: uuid.UUID, admin: AdminUser, db: Db) -> VersionDetail:
    found = db.execute(_summary_query().where(QuestionVersionRow.id == version_id)).one_or_none()
    if found is None:
        raise ContentError("question_not_found", "No existe esa versión de pregunta")
    row = found[0]
    options = db.scalars(
        select(AnswerOptionRow.text)
        .where(AnswerOptionRow.version_id == row.id)
        .order_by(AnswerOptionRow.position)
    ).all()
    reviews = db.execute(
        select(ContentReviewRow, UserAccountRow.email)
        .join(UserAccountRow, UserAccountRow.id == ContentReviewRow.reviewer_id)
        .where(ContentReviewRow.version_id == row.id)
        .order_by(ContentReviewRow.created_at)
    ).all()
    return VersionDetail(
        **_summary(*found, admin.id),
        options=list(options),
        correct_position=row.correct_position,
        explanation=row.explanation,
        source=row.source,
        reviews=[
            ReviewOut(
                decision=r.decision, comment=r.comment, reviewer=email, created_at=r.created_at
            )
            for r, email in reviews
        ],
    )


class ContentIn(BaseModel):
    subject: str = Field(min_length=1, max_length=120)
    subtopic: str | None = Field(default=None, max_length=160)
    difficulty: int = Field(ge=DIFFICULTY_MIN, le=DIFFICULTY_MAX)
    prompt: str = Field(min_length=1)
    options: list[str] = Field(min_length=OPTIONS_MIN, max_length=OPTIONS_MAX)
    correct_position: int = Field(ge=0)
    explanation: str = Field(min_length=1)
    source: str = Field(min_length=1, max_length=300)


@admin_router.post("/{version_id}/edit", status_code=status.HTTP_201_CREATED)
def edit_version(
    version_id: uuid.UUID, body: ContentIn, admin: AdminUser, svc: Service
) -> dict[str, str]:
    if body.correct_position >= len(body.options) or any(not o.strip() for o in body.options):
        raise ContentError("invalid_options", "Revisa las alternativas y la respuesta correcta")
    content = QuestionContent(**body.model_dump())
    return {"id": str(svc.edit(version_id, content, admin.id))}


class ReviewIn(BaseModel):
    decision: ReviewDecision
    comment: str | None = Field(default=None, max_length=2000)


@admin_router.post("/{version_id}/submit", status_code=status.HTTP_204_NO_CONTENT)
def submit(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    svc.submit(version_id, admin.id)


@admin_router.post("/{version_id}/review", status_code=status.HTTP_204_NO_CONTENT)
def review(version_id: uuid.UUID, body: ReviewIn, admin: AdminUser, svc: Service) -> None:
    svc.review(version_id, admin.id, body.decision, body.comment)


@admin_router.post("/{version_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
def publish(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    svc.publish(version_id, admin.id)


@admin_router.post("/{version_id}/retire", status_code=status.HTTP_204_NO_CONTENT)
def retire(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    svc.retire(version_id, admin.id)


# ---------------------------------------------------------------------- práctica


class PracticeQuestion(BaseModel):
    id: str
    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    options: list[str]  # sin la respuesta correcta: se revela al responder


@practice_router.get("/questions")
def practice_questions(
    _: SubscribedUser,
    db: Db,
    limit: Annotated[int, Query(ge=1, le=30)] = 10,
) -> list[PracticeQuestion]:
    """Preguntas publicadas al azar. Solo versiones `published` (regla de integridad 1)."""
    rows = db.execute(
        _summary_query()
        .where(QuestionVersionRow.status == VersionStatus.PUBLISHED)
        .order_by(func.random())
        .limit(limit)
    ).all()
    return [_practice_question(db, row, subject, subtopic) for row, subject, subtopic, _ in rows]


class LessonOut(BaseModel):
    id: str
    title: str
    subtopics: list[str]
    total: int
    answered: int
    correct: int
    completed: bool
    stars: int


class UnitOut(BaseModel):
    subject: str
    lessons: list[LessonOut]


class PathOut(BaseModel):
    units: list[UnitOut]
    xp: int


def _lesson_out(lesson: Lesson) -> LessonOut:
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


@practice_router.get("/path")
def study_path(user: SubscribedUser, db: Db) -> PathOut:
    """La ruta de estudio con el avance del estudiante (solo preguntas publicadas)."""
    units = build_path(db, user.id)
    return PathOut(
        units=[
            UnitOut(subject=u.subject, lessons=[_lesson_out(x) for x in u.lessons]) for u in units
        ],
        xp=total_xp(db, user.id),
    )


class LessonDetail(LessonOut):
    subject: str
    questions: list[PracticeQuestion]


@practice_router.get("/lessons/{lesson_id}")
def lesson_questions(lesson_id: str, user: SubscribedUser, db: Db) -> LessonDetail:
    found = find_lesson(build_path(db, user.id), lesson_id)
    if found is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"code": "lesson_not_found", "message": "Esa lección ya no está disponible"},
        )
    unit, lesson = found
    rows = db.execute(_summary_query().where(QuestionVersionRow.id.in_(lesson.version_ids))).all()
    by_id = {row.id: (row, subject, subtopic) for row, subject, subtopic, _ in rows}
    questions = [_practice_question(db, *by_id[vid]) for vid in lesson.version_ids if vid in by_id]
    return LessonDetail(
        **_lesson_out(lesson).model_dump(), subject=unit.subject, questions=questions
    )


def _practice_question(db: Session, row, subject: str, subtopic: str | None) -> PracticeQuestion:
    options = db.scalars(
        select(AnswerOptionRow.text)
        .where(AnswerOptionRow.version_id == row.id)
        .order_by(AnswerOptionRow.position)
    ).all()
    return PracticeQuestion(
        id=str(row.id),
        subject=subject,
        subtopic=subtopic,
        difficulty=row.difficulty,
        prompt=row.prompt,
        options=list(options),
    )


class AnswerIn(BaseModel):
    version_id: uuid.UUID
    position: int = Field(ge=0)


class AnswerOut(BaseModel):
    correct: bool
    correct_position: int
    explanation: str
    source: str


@practice_router.post("/answers")
def answer(body: AnswerIn, user: SubscribedUser, db: Db, clock: Clock) -> AnswerOut:
    version = db.get(QuestionVersionRow, body.version_id)
    if version is None or version.status != VersionStatus.PUBLISHED:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"code": "question_not_found", "message": "La pregunta ya no está disponible"},
        )
    count = db.scalar(
        select(func.count())
        .select_from(AnswerOptionRow)
        .where(AnswerOptionRow.version_id == version.id)
    )
    if body.position >= (count or 0):
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

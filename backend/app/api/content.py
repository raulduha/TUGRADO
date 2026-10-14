"""Banco de preguntas: administración (FR-013, FR-014) y práctica de alternativas (FR-006)."""

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session, aliased

from app.api.deps import AdminUser, SubscribedUser, get_clock
from app.content.importer import parse_workbook
from app.content.service import ContentError, ContentService, QuestionContent
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


def service(db: Db, clock: Clock) -> ContentService:
    return ContentService(db, clock)


Service = Annotated[ContentService, Depends(service)]


# ------------------------------------------------------------------ administración


class ImportOut(BaseModel):
    imported: int
    errors: list[dict]


@admin_router.post("/import")
async def import_questions(request: Request, admin: AdminUser, svc: Service) -> ImportOut:
    """Recibe el .xlsx como cuerpo binario. Todo o nada: con errores no importa ninguna fila."""
    data = await request.body()
    if len(data) > MAX_UPLOAD_BYTES:
        raise ContentError("file_too_large", "El archivo supera los 25 MB")
    parsed, errors = parse_workbook(data)
    if errors:
        return ImportOut(imported=0, errors=[{"row": e.row, "message": e.message} for e in errors])
    return ImportOut(imported=svc.import_questions(parsed, admin.id), errors=[])


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
    out = []
    for row, subject, subtopic, _author in rows:
        options = db.scalars(
            select(AnswerOptionRow.text)
            .where(AnswerOptionRow.version_id == row.id)
            .order_by(AnswerOptionRow.position)
        ).all()
        out.append(
            PracticeQuestion(
                id=str(row.id),
                subject=subject,
                subtopic=subtopic,
                difficulty=row.difficulty,
                prompt=row.prompt,
                options=list(options),
            )
        )
    return out


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

"""Consultas de lectura del banco para el panel de administración y la práctica."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, aliased

from app.persistence.auth_models import UserAccountRow
from app.persistence.content_models import (
    AnswerOptionRow,
    ContentReviewRow,
    QuestionRow,
    QuestionVersionRow,
    ReviewDecision,
    SubjectRow,
    SubtopicRow,
    VersionStatus,
)


@dataclass(frozen=True)
class VersionView:
    """Una versión con los nombres de su materia, subtema y autor."""

    version: QuestionVersionRow
    subject: str
    subtopic: str | None
    author: str


@dataclass(frozen=True)
class ReviewView:
    decision: ReviewDecision
    comment: str | None
    reviewer: str
    created_at: datetime


def _versions() -> Select:
    author = aliased(UserAccountRow)
    return (
        select(QuestionVersionRow, SubjectRow.name, SubtopicRow.name, author.email)
        .join(SubjectRow, SubjectRow.id == QuestionVersionRow.subject_id)
        .outerjoin(SubtopicRow, SubtopicRow.id == QuestionVersionRow.subtopic_id)
        .join(author, author.id == QuestionVersionRow.created_by)
    )


def _views(db: Session, query: Select) -> list[VersionView]:
    return [VersionView(*row) for row in db.execute(query).all()]


# --------------------------------------------------------------------------- panel


def search_versions(
    db: Session,
    *,
    status: VersionStatus | None = None,
    subject: str | None = None,
    text: str | None = None,
    limit: int = 200,
    offset: int = 0,
) -> list[VersionView]:
    """Las más nuevas primero; dentro de una misma carga, en el orden de la planilla. `text`
    busca en el enunciado y en el subtema, sin distinguir mayúsculas."""
    query = (
        _versions()
        .join(QuestionRow, QuestionRow.id == QuestionVersionRow.question_id)
        .order_by(
            QuestionVersionRow.created_at.desc(),
            QuestionRow.created_at,
            QuestionVersionRow.number.desc(),
        )
        .limit(limit)
        .offset(offset)
    )
    if status is not None:
        query = query.where(QuestionVersionRow.status == status)
    if subject:
        query = query.where(SubjectRow.name == subject)
    if text and text.strip():
        pattern = f"%{text.strip()}%"
        query = query.where(
            QuestionVersionRow.prompt.ilike(pattern) | SubtopicRow.name.ilike(pattern)
        )
    return _views(db, query)


def version_view(db: Session, version_id: uuid.UUID) -> VersionView | None:
    views = _views(db, _versions().where(QuestionVersionRow.id == version_id))
    return views[0] if views else None


def history(db: Session, question_id: uuid.UUID) -> list[VersionView]:
    """Todas las versiones de una pregunta, de la más nueva a la más antigua."""
    query = _versions().where(QuestionVersionRow.question_id == question_id)
    return _views(db, query.order_by(QuestionVersionRow.number.desc()))


def reviews(db: Session, version_id: uuid.UUID) -> list[ReviewView]:
    rows = db.execute(
        select(ContentReviewRow, UserAccountRow.email)
        .join(UserAccountRow, UserAccountRow.id == ContentReviewRow.reviewer_id)
        .where(ContentReviewRow.version_id == version_id)
        .order_by(ContentReviewRow.created_at)
    ).all()
    return [ReviewView(r.decision, r.comment, email, r.created_at) for r, email in rows]


def subjects_with_subtopics(db: Session) -> dict[str, list[str]]:
    rows = db.execute(
        select(SubjectRow.name, SubtopicRow.name)
        .outerjoin(SubtopicRow, SubtopicRow.subject_id == SubjectRow.id)
        .order_by(SubjectRow.name, SubtopicRow.name)
    ).all()
    out: dict[str, list[str]] = {}
    for subject, subtopic in rows:
        out.setdefault(subject, [])
        if subtopic:
            out[subject].append(subtopic)
    return out


# ------------------------------------------------------------------------ práctica


def options(db: Session, version_id: uuid.UUID) -> list[str]:
    return list(
        db.scalars(
            select(AnswerOptionRow.text)
            .where(AnswerOptionRow.version_id == version_id)
            .order_by(AnswerOptionRow.position)
        )
    )


def random_published(db: Session, limit: int) -> list[VersionView]:
    """Preguntas publicadas al azar (solo `published`: regla de integridad 1)."""
    query = _versions().where(QuestionVersionRow.status == VersionStatus.PUBLISHED)
    return _views(db, query.order_by(func.random()).limit(limit))


def published_by_ids(db: Session, version_ids: list[uuid.UUID]) -> list[VersionView]:
    """Las versiones publicadas pedidas, en el mismo orden de `version_ids`."""
    query = _versions().where(
        QuestionVersionRow.id.in_(version_ids),
        QuestionVersionRow.status == VersionStatus.PUBLISHED,
    )
    by_id = {view.version.id: view for view in _views(db, query)}
    return [by_id[i] for i in version_ids if i in by_id]

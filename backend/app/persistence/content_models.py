"""Banco de preguntas versionado (FR-004, FR-006, FR-013, FR-014; reglas de integridad 1–2).

Una `QuestionVersion` es inmutable en su contenido: editar crea una versión nueva. Solo una
versión `published` se usa con estudiantes. Quien crea una versión no puede aprobarla ni
publicarla; aprobar y publicar son actos distintos y quedan en `content_event`.
Jurisdicción y programa de estudio aún no se modelan (pendiente de las materias reales).
"""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base, enum_check, enum_column

DIFFICULTY_MIN, DIFFICULTY_MAX = 1, 3
OPTIONS_MIN, OPTIONS_MAX = 2, 5


class VersionStatus(StrEnum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    RETIRED = "retired"


class ReviewDecision(StrEnum):
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"


class ContentAction(StrEnum):
    IMPORTED = "imported"
    CREATED = "created"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    PUBLISHED = "published"
    RETIRED = "retired"


class SubjectRow(Base):
    __tablename__ = "subject"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True)


class SubtopicRow(Base):
    __tablename__ = "subtopic"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subject.id", ondelete="RESTRICT"), index=True
    )
    name: Mapped[str] = mapped_column(String(160))

    __table_args__ = (UniqueConstraint("subject_id", "name", name="uq_subtopic_subject_name"),)


class QuestionRow(Base):
    """Identidad estable de una pregunta; su contenido vive en las versiones."""

    __tablename__ = "question"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class QuestionVersionRow(Base):
    __tablename__ = "question_version"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question.id", ondelete="RESTRICT"), index=True
    )
    number: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(20), default="multiple_choice")
    subject_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("subject.id", ondelete="RESTRICT"))
    subtopic_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("subtopic.id", ondelete="RESTRICT")
    )
    difficulty: Mapped[int] = mapped_column(Integer)
    prompt: Mapped[str] = mapped_column(Text)
    correct_position: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(300))
    status: Mapped[VersionStatus] = mapped_column(enum_column(VersionStatus), index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="RESTRICT")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        enum_check("status", VersionStatus, "status_valid"),
        UniqueConstraint("question_id", "number", name="uq_question_version_number"),
        CheckConstraint(
            f"difficulty BETWEEN {DIFFICULTY_MIN} AND {DIFFICULTY_MAX}", name="difficulty_range"
        ),
        CheckConstraint("kind IN ('multiple_choice')", name="kind_valid"),
        # A lo más una versión publicada por pregunta.
        Index(
            "uq_question_one_published",
            "question_id",
            unique=True,
            postgresql_where=text("status = 'published'"),
        ),
    )


class AnswerOptionRow(Base):
    __tablename__ = "answer_option"

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question_version.id", ondelete="RESTRICT"), primary_key=True
    )
    position: Mapped[int] = mapped_column(Integer, primary_key=True)  # 0 = A, 1 = B…
    text: Mapped[str] = mapped_column(Text)


class ContentReviewRow(Base):
    __tablename__ = "content_review"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question_version.id", ondelete="RESTRICT"), index=True
    )
    reviewer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="RESTRICT")
    )
    decision: Mapped[ReviewDecision] = mapped_column(enum_column(ReviewDecision))
    comment: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (enum_check("decision", ReviewDecision, "decision_valid"),)


class ContentEventRow(Base):
    """Auditoría de solo adición del ciclo de vida de cada versión."""

    __tablename__ = "content_event"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question_version.id", ondelete="RESTRICT"), index=True
    )
    action: Mapped[ContentAction] = mapped_column(enum_column(ContentAction))
    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id", ondelete="RESTRICT"))
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (enum_check("action", ContentAction, "action_valid"),)


class PracticeAttemptRow(Base):
    __tablename__ = "practice_attempt"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question_version.id", ondelete="RESTRICT")
    )
    chosen_position: Mapped[int] = mapped_column(Integer)
    correct: Mapped[bool]
    answered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

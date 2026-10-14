"""Flujo editorial del banco de preguntas (FR-013, FR-014, AC-029).

borrador → en revisión → (otro admin) aprobada | vuelve a borrador con cambios pedidos
aprobada → (otro admin) publicada; la versión publicada anterior de la misma pregunta se retira.
Editar nunca modifica una versión: crea la siguiente como borrador.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.content.importer import ParsedQuestion
from app.errors import AppError
from app.persistence.content_models import (
    AnswerOptionRow,
    ContentAction,
    ContentEventRow,
    ContentReviewRow,
    QuestionRow,
    QuestionVersionRow,
    ReviewDecision,
    SubjectRow,
    SubtopicRow,
    VersionStatus,
)


class ContentError(AppError):
    pass


@dataclass(frozen=True)
class QuestionContent:
    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    options: list[str]
    correct_position: int
    explanation: str
    source: str


class ContentService:
    def __init__(self, db: Session, clock: Callable[[], datetime]) -> None:
        self.db = db
        self.clock = clock

    # ---------------------------------------------------------------- creación

    def import_questions(self, rows: list[ParsedQuestion], actor: uuid.UUID) -> int:
        for row in rows:
            content = QuestionContent(
                subject=row.subject,
                subtopic=row.subtopic,
                difficulty=row.difficulty,
                prompt=row.prompt,
                options=row.options,
                correct_position=row.correct_position,
                explanation=row.explanation,
                source=row.source,
            )
            question = QuestionRow(id=uuid.uuid4(), created_at=self.clock())
            self.db.add(question)
            self.db.flush()
            self._new_version(question.id, 1, content, actor, ContentAction.IMPORTED)
        self.db.commit()
        return len(rows)

    def edit(self, version_id: uuid.UUID, content: QuestionContent, actor: uuid.UUID) -> uuid.UUID:
        """Crea la siguiente versión como borrador; la editada no cambia."""
        base = self._version(version_id, lock=True)
        latest = self.db.scalar(
            select(func.max(QuestionVersionRow.number)).where(
                QuestionVersionRow.question_id == base.question_id
            )
        )
        version = self._new_version(
            base.question_id, (latest or 0) + 1, content, actor, ContentAction.CREATED
        )
        self.db.commit()
        return version.id

    # ------------------------------------------------------------------ flujo

    def submit(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        version = self._version(version_id, lock=True)
        self._expect(version, VersionStatus.DRAFT, "Solo un borrador puede enviarse a revisión")
        version.status = VersionStatus.IN_REVIEW
        self._event(version, ContentAction.SUBMITTED, actor)
        self.db.commit()

    def review(
        self,
        version_id: uuid.UUID,
        reviewer: uuid.UUID,
        decision: ReviewDecision,
        comment: str | None,
    ) -> None:
        version = self._version(version_id, lock=True)
        self._expect(version, VersionStatus.IN_REVIEW, "La versión no está en revisión")
        self._not_author(version, reviewer, "revisar")
        if decision == ReviewDecision.CHANGES_REQUESTED and not (comment and comment.strip()):
            raise ContentError("comment_required", "Explica qué cambios se necesitan")
        self.db.add(
            ContentReviewRow(
                version_id=version.id,
                reviewer_id=reviewer,
                decision=decision,
                comment=comment.strip() if comment else None,
                created_at=self.clock(),
            )
        )
        if decision == ReviewDecision.APPROVED:
            version.status = VersionStatus.APPROVED
            self._event(version, ContentAction.APPROVED, reviewer)
        else:
            version.status = VersionStatus.DRAFT
            self._event(version, ContentAction.CHANGES_REQUESTED, reviewer)
        self.db.commit()

    def publish(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        version = self._version(version_id, lock=True)
        self._expect(version, VersionStatus.APPROVED, "Solo una versión aprobada puede publicarse")
        self._not_author(version, actor, "publicar")
        current = self.db.scalars(
            select(QuestionVersionRow)
            .where(QuestionVersionRow.question_id == version.question_id)
            .where(QuestionVersionRow.status == VersionStatus.PUBLISHED)
            .with_for_update()
        ).one_or_none()
        if current is not None:
            current.status = VersionStatus.RETIRED
            self._event(current, ContentAction.RETIRED, actor)
            self.db.flush()  # libera el índice único antes de publicar la nueva
        version.status = VersionStatus.PUBLISHED
        self._event(version, ContentAction.PUBLISHED, actor)
        self.db.commit()

    def retire(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        version = self._version(version_id, lock=True)
        self._expect(version, VersionStatus.PUBLISHED, "Solo una versión publicada puede retirarse")
        version.status = VersionStatus.RETIRED
        self._event(version, ContentAction.RETIRED, actor)
        self.db.commit()

    # --------------------------------------------------------------- internos

    def _new_version(
        self,
        question_id: uuid.UUID,
        number: int,
        content: QuestionContent,
        actor: uuid.UUID,
        action: ContentAction,
    ) -> QuestionVersionRow:
        subject = self._subject(content.subject)
        subtopic = self._subtopic(subject, content.subtopic) if content.subtopic else None
        version = QuestionVersionRow(
            id=uuid.uuid4(),
            question_id=question_id,
            number=number,
            kind="multiple_choice",
            subject_id=subject.id,
            subtopic_id=subtopic.id if subtopic else None,
            difficulty=content.difficulty,
            prompt=content.prompt,
            correct_position=content.correct_position,
            explanation=content.explanation,
            source=content.source,
            status=VersionStatus.DRAFT,
            created_by=actor,
            created_at=self.clock(),
        )
        self.db.add(version)
        self.db.flush()
        for position, option in enumerate(content.options):
            self.db.add(AnswerOptionRow(version_id=version.id, position=position, text=option))
        self._event(version, action, actor)
        return version

    def _subject(self, name: str) -> SubjectRow:
        row = self.db.scalars(select(SubjectRow).where(SubjectRow.name == name)).one_or_none()
        if row is None:
            row = SubjectRow(id=uuid.uuid4(), name=name)
            self.db.add(row)
            self.db.flush()
        return row

    def _subtopic(self, subject: SubjectRow, name: str) -> SubtopicRow:
        row = self.db.scalars(
            select(SubtopicRow).where(
                SubtopicRow.subject_id == subject.id, SubtopicRow.name == name
            )
        ).one_or_none()
        if row is None:
            row = SubtopicRow(id=uuid.uuid4(), subject_id=subject.id, name=name)
            self.db.add(row)
            self.db.flush()
        return row

    def _version(self, version_id: uuid.UUID, lock: bool = False) -> QuestionVersionRow:
        query = select(QuestionVersionRow).where(QuestionVersionRow.id == version_id)
        row = self.db.scalars(query.with_for_update() if lock else query).one_or_none()
        if row is None:
            raise ContentError("question_not_found", "No existe esa versión de pregunta")
        return row

    @staticmethod
    def _expect(version: QuestionVersionRow, status: VersionStatus, message: str) -> None:
        if version.status != status:
            raise ContentError("invalid_transition", message)

    @staticmethod
    def _not_author(version: QuestionVersionRow, actor: uuid.UUID, verb: str) -> None:
        if version.created_by == actor:
            raise ContentError(
                "author_cannot_review",
                f"Quien creó o modificó esta versión no puede {verb}la: "
                "debe hacerlo otro administrador",
            )

    def _event(self, version: QuestionVersionRow, action: ContentAction, actor: uuid.UUID) -> None:
        self.db.add(
            ContentEventRow(version_id=version.id, action=action, actor_id=actor, at=self.clock())
        )

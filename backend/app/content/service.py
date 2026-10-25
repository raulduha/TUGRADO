"""Flujo editorial del banco de preguntas (FR-013, FR-014, AC-029, AC-046).

Cada pregunta tiene versiones numeradas e inmutables. Una versión avanza así:

    borrador → en revisión → aprobada → publicada
                   ↘ (cambios pedidos) vuelve a borrador

- Editar nunca modifica una versión: crea la siguiente como borrador.
- Quien crea una versión no puede aprobarla ni publicarla: lo hace otro administrador.
- Publicar una versión retira la publicada anterior de la misma pregunta.
- Retirar no borra nada: la versión (o la pregunta completa) queda en el historial.

Los métodos no confirman la transacción: lo hace quien los llama (la API o app/content/sync.py),
para que, por ejemplo, una planilla se aplique completa o no se aplique. La excepción es `bulk`,
que confirma cada versión por separado.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.content.question import ContentError, QuestionContent
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


class ContentService:
    def __init__(self, db: Session, clock: Callable[[], datetime]) -> None:
        self.db = db
        self.clock = clock

    # ------------------------------------------------------------- crear y editar

    def create(
        self,
        content: QuestionContent,
        actor: uuid.UUID,
        *,
        action: ContentAction = ContentAction.CREATED,
        created_at: datetime | None = None,
    ) -> QuestionVersionRow:
        """Pregunta nueva: su versión 1 queda en borrador."""
        question = QuestionRow(id=uuid.uuid4(), created_at=created_at or self.clock())
        self.db.add(question)
        self.db.flush()
        return self.add_version(question.id, content, actor, action=action)

    def add_version(
        self,
        question_id: uuid.UUID,
        content: QuestionContent,
        actor: uuid.UUID,
        *,
        action: ContentAction = ContentAction.CREATED,
    ) -> QuestionVersionRow:
        """La versión siguiente de una pregunta, en borrador. Las anteriores no cambian."""
        latest = self.latest_version(question_id, lock=True)
        version = QuestionVersionRow(
            id=uuid.uuid4(),
            question_id=question_id,
            number=(latest.number if latest else 0) + 1,
            kind="multiple_choice",
            subject_id=self._subject(content.subject).id,
            subtopic_id=self._subtopic(content.subject, content.subtopic),
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
        for position, text in enumerate(content.options):
            self.db.add(AnswerOptionRow(version_id=version.id, position=position, text=text))
        self._log(version, action, actor)
        return version

    def edit(self, version_id: uuid.UUID, content: QuestionContent, actor: uuid.UUID) -> uuid.UUID:
        """Edita a partir de una versión: guarda la siguiente como borrador."""
        base = self._version(version_id)
        return self.add_version(base.question_id, content, actor).id

    # ------------------------------------------------------------- revisar y publicar

    def submit(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        version = self._version(version_id, lock=True)
        self._require(version, VersionStatus.DRAFT, "Solo un borrador puede enviarse a revisión")
        version.status = VersionStatus.IN_REVIEW
        self._log(version, ContentAction.SUBMITTED, actor)

    def review(
        self,
        version_id: uuid.UUID,
        reviewer: uuid.UUID,
        decision: ReviewDecision,
        comment: str | None = None,
    ) -> None:
        version = self._version(version_id, lock=True)
        self._require(version, VersionStatus.IN_REVIEW, "La versión no está en revisión")
        self._require_other_admin(version, reviewer, "revisar")
        comment = (comment or "").strip() or None
        if decision == ReviewDecision.CHANGES_REQUESTED and comment is None:
            raise ContentError("comment_required", "Explica qué cambios se necesitan")
        self.db.add(
            ContentReviewRow(
                version_id=version.id,
                reviewer_id=reviewer,
                decision=decision,
                comment=comment,
                created_at=self.clock(),
            )
        )
        if decision == ReviewDecision.APPROVED:
            version.status = VersionStatus.APPROVED
            self._log(version, ContentAction.APPROVED, reviewer)
        else:
            version.status = VersionStatus.DRAFT
            self._log(version, ContentAction.CHANGES_REQUESTED, reviewer)

    def publish(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        version = self._version(version_id, lock=True)
        self._require(version, VersionStatus.APPROVED, "Solo una versión aprobada puede publicarse")
        self._require_other_admin(version, actor, "publicar")
        previous = self.db.scalars(
            select(QuestionVersionRow)
            .where(QuestionVersionRow.question_id == version.question_id)
            .where(QuestionVersionRow.status == VersionStatus.PUBLISHED)
            .with_for_update()
        ).one_or_none()
        if previous is not None:
            self._set_retired(previous, actor)
            self.db.flush()  # libera el índice «una publicada por pregunta» antes de publicar
        version.status = VersionStatus.PUBLISHED
        self._log(version, ContentAction.PUBLISHED, actor)

    # -------------------------------------------------------------------- retirar

    def retire(self, version_id: uuid.UUID, actor: uuid.UUID) -> None:
        """Retira una versión: la publicada sale de la práctica; un borrador queda descartado."""
        version = self._version(version_id, lock=True)
        if version.status == VersionStatus.RETIRED:
            raise ContentError("invalid_transition", "Esta versión ya está retirada")
        self._set_retired(version, actor)

    def retire_question(self, question_id: uuid.UUID, actor: uuid.UUID) -> bool:
        """Retira todas las versiones vigentes de la pregunta. False si ya no quedaba ninguna."""
        active = self.db.scalars(
            select(QuestionVersionRow)
            .where(QuestionVersionRow.question_id == question_id)
            .where(QuestionVersionRow.status != VersionStatus.RETIRED)
            .with_for_update()
        ).all()
        for version in active:
            self._set_retired(version, actor)
        return bool(active)

    # ------------------------------------------------------------------- en bloque

    def bulk(
        self, action: str, version_ids: list[uuid.UUID], actor: uuid.UUID
    ) -> tuple[int, list[tuple[uuid.UUID, str]]]:
        """Misma acción para varias versiones, cada una con sus reglas. No es todo o nada:
        las que no pueden avanzar se saltan con su motivo. Confirma cada una por separado."""
        steps: dict[str, Callable[[uuid.UUID], None]] = {
            "submit": lambda vid: self.submit(vid, actor),
            "approve": lambda vid: self.review(vid, actor, ReviewDecision.APPROVED),
            "publish": lambda vid: self.publish(vid, actor),
        }
        if action not in steps:
            raise ContentError("invalid_action", "Acción desconocida")
        done, skipped = 0, []
        for version_id in dict.fromkeys(version_ids):
            try:
                steps[action](version_id)
                self.db.commit()
                done += 1
            except ContentError as error:
                self.db.rollback()
                skipped.append((version_id, str(error)))
        return done, skipped

    # ---------------------------------------------------------------------- lectura

    def latest_version(
        self, question_id: uuid.UUID, lock: bool = False
    ) -> QuestionVersionRow | None:
        query = (
            select(QuestionVersionRow)
            .where(QuestionVersionRow.question_id == question_id)
            .order_by(QuestionVersionRow.number.desc())
            .limit(1)
        )
        return self.db.scalars(query.with_for_update() if lock else query).one_or_none()

    def content_of(self, version: QuestionVersionRow) -> QuestionContent:
        subject = self.db.get(SubjectRow, version.subject_id)
        subtopic = self.db.get(SubtopicRow, version.subtopic_id) if version.subtopic_id else None
        options = self.db.scalars(
            select(AnswerOptionRow.text)
            .where(AnswerOptionRow.version_id == version.id)
            .order_by(AnswerOptionRow.position)
        ).all()
        assert subject is not None
        return QuestionContent(
            subject=subject.name,
            subtopic=subtopic.name if subtopic else None,
            difficulty=version.difficulty,
            prompt=version.prompt,
            options=list(options),
            correct_position=version.correct_position,
            explanation=version.explanation,
            source=version.source,
        )

    def version(self, version_id: uuid.UUID) -> QuestionVersionRow:
        return self._version(version_id)

    # --------------------------------------------------------------------- internos

    def _version(self, version_id: uuid.UUID, lock: bool = False) -> QuestionVersionRow:
        query = select(QuestionVersionRow).where(QuestionVersionRow.id == version_id)
        row = self.db.scalars(query.with_for_update() if lock else query).one_or_none()
        if row is None:
            raise ContentError("question_not_found", "No existe esa versión de pregunta")
        return row

    def _subject(self, name: str) -> SubjectRow:
        row = self.db.scalars(select(SubjectRow).where(SubjectRow.name == name)).one_or_none()
        if row is None:
            row = SubjectRow(id=uuid.uuid4(), name=name)
            self.db.add(row)
            self.db.flush()
        return row

    def _subtopic(self, subject_name: str, name: str | None) -> uuid.UUID | None:
        if not name:
            return None
        subject = self._subject(subject_name)
        row = self.db.scalars(
            select(SubtopicRow).where(
                SubtopicRow.subject_id == subject.id, SubtopicRow.name == name
            )
        ).one_or_none()
        if row is None:
            row = SubtopicRow(id=uuid.uuid4(), subject_id=subject.id, name=name)
            self.db.add(row)
            self.db.flush()
        return row.id

    def _set_retired(self, version: QuestionVersionRow, actor: uuid.UUID) -> None:
        version.status = VersionStatus.RETIRED
        self._log(version, ContentAction.RETIRED, actor)

    @staticmethod
    def _require(version: QuestionVersionRow, status: VersionStatus, message: str) -> None:
        if version.status != status:
            raise ContentError("invalid_transition", message)

    @staticmethod
    def _require_other_admin(version: QuestionVersionRow, actor: uuid.UUID, verb: str) -> None:
        if version.created_by == actor:
            raise ContentError(
                "author_cannot_review",
                f"Quien creó o modificó esta versión no puede {verb}la: "
                "debe hacerlo otro administrador",
            )

    def _log(self, version: QuestionVersionRow, action: ContentAction, actor: uuid.UUID) -> None:
        """Auditoría de solo adición (content_event)."""
        self.db.add(
            ContentEventRow(version_id=version.id, action=action, actor_id=actor, at=self.clock())
        )

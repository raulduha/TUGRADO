"""Glosario jurídico para el rosco legal (FR-038).

Cada término pasa por borrador → aprobado → publicado, y solo los publicados llegan a los
estudiantes. Igual que en el banco de preguntas, quien carga un término no puede aprobarlo ni
publicarlo (AC-029); aprobar y publicar quedan registrados con responsable y fecha.
"""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base, enum_check, enum_column


class TermStatus(StrEnum):
    DRAFT = "draft"
    APPROVED = "approved"
    PUBLISHED = "published"
    RETIRED = "retired"


class GlossaryTermRow(Base):
    __tablename__ = "glossary_term"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subject.id", ondelete="CASCADE"), index=True
    )
    term: Mapped[str] = mapped_column(String(120))
    definition: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(300))
    status: Mapped[TermStatus] = mapped_column(enum_column(TermStatus), index=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("user_account.id"))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    published_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("user_account.id"))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        enum_check("status", TermStatus, "status_valid"),
        # Un término vigente por materia (sin distinguir mayúsculas); los retirados no cuentan.
        Index(
            "uq_glossary_term_active",
            "subject_id",
            text("lower(term)"),
            unique=True,
            postgresql_where=text("status <> 'retired'"),
        ),
    )

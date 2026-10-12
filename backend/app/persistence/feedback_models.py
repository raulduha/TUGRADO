"""Comentarios de usuarios sobre la aplicación (FR-028, AC-037)."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base, enum_check, enum_column

FEEDBACK_MAX_LENGTH = 2000


class FeedbackCategory(StrEnum):
    SUGGESTION = "suggestion"
    PROBLEM = "problem"
    OTHER = "other"


class UserFeedbackRow(Base):
    __tablename__ = "user_feedback"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[FeedbackCategory] = mapped_column(enum_column(FeedbackCategory))
    message: Mapped[str] = mapped_column(Text)
    # Ruta de la app desde la que se envió (por ejemplo, /panel); nunca una URL externa.
    page: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    __table_args__ = (
        enum_check("category", FeedbackCategory, "category_valid"),
        CheckConstraint(
            f"char_length(message) BETWEEN 1 AND {FEEDBACK_MAX_LENGTH}", name="message_length"
        ),
    )

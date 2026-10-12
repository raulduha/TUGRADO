"""Comentarios de usuarios (FR-028, AC-037)."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import AdminUser, CurrentUser, get_clock
from app.db import get_db
from app.persistence.auth_models import UserAccountRow
from app.persistence.feedback_models import (
    FEEDBACK_MAX_LENGTH,
    FeedbackCategory,
    UserFeedbackRow,
)

router = APIRouter(prefix="/feedback", tags=["feedback"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]


class FeedbackIn(BaseModel):
    category: FeedbackCategory
    message: str = Field(max_length=FEEDBACK_MAX_LENGTH)
    page: str | None = Field(default=None, max_length=200)

    @field_validator("message")
    @classmethod
    def not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El comentario no puede estar vacío")
        return value

    @field_validator("page")
    @classmethod
    def internal_path(cls, value: str | None) -> str | None:
        # Solo rutas internas de la app; cualquier otra cosa se descarta.
        if value is None or not value.startswith("/") or value.startswith("//"):
            return None
        return value


class FeedbackOut(BaseModel):
    id: str
    category: FeedbackCategory
    message: str
    page: str | None
    created_at: datetime
    user_email: str


@router.post("", status_code=status.HTTP_201_CREATED)
def send_feedback(body: FeedbackIn, user: CurrentUser, db: Db, clock: Clock) -> dict[str, str]:
    row = UserFeedbackRow(
        user_id=user.id,
        category=body.category,
        message=body.message,
        page=body.page,
        created_at=clock(),
    )
    db.add(row)
    db.commit()
    return {"id": str(row.id)}


@router.get("")
def list_feedback(
    _: AdminUser, db: Db, limit: Annotated[int, Query(ge=1, le=200)] = 50
) -> list[FeedbackOut]:
    rows = db.execute(
        select(UserFeedbackRow, UserAccountRow.email)
        .join(UserAccountRow, UserAccountRow.id == UserFeedbackRow.user_id)
        .order_by(UserFeedbackRow.created_at.desc())
        .limit(limit)
    ).all()
    return [
        FeedbackOut(
            id=str(row.id),
            category=row.category,
            message=row.message,
            page=row.page,
            created_at=row.created_at,
            user_email=email,
        )
        for row, email in rows
    ]

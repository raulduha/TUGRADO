"""Plan diario del estudiante (FR-035, AC-047): fecha del examen, meta diaria y repaso."""

from collections.abc import Callable
from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import SubscribedUser, get_clock
from app.db import get_db
from app.study import plan

router = APIRouter(prefix="/study", tags=["study"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]


class TodayOut(BaseModel):
    exam_date: date | None
    days_left: int | None
    daily_goal: int | None
    suggested_goal: int | None
    answered_today: int
    review_due: int
    remaining: int


class ProfileIn(BaseModel):
    exam_date: date | None = None
    daily_goal: int | None = Field(default=None, ge=1, le=200)


@router.get("/today")
def today(user: SubscribedUser, db: Db, clock: Clock) -> TodayOut:
    """Lo que el estudiante tiene para hoy: cuenta regresiva, meta, avance y repaso."""
    return TodayOut(**plan.today_summary(db, user.id, clock()).__dict__)


@router.put("/profile", status_code=status.HTTP_204_NO_CONTENT)
def save_profile(body: ProfileIn, user: SubscribedUser, db: Db, clock: Clock) -> None:
    plan.save_profile(db, user.id, body.exam_date, body.daily_goal, clock())

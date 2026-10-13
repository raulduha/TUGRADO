"""Rachas de días seguidos (FR-033, AC-042)."""

from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_clock
from app.clock import chile_date
from app.db import get_db
from app.engagement.streaks import check_in

router = APIRouter(prefix="/engagement", tags=["engagement"])


class StreakOut(BaseModel):
    current: int
    best: int
    new_today: bool
    week: list[bool]


@router.post("/checkin")
def checkin(
    user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    clock: Annotated[Callable[[], datetime], Depends(get_clock)],
) -> StreakOut:
    """Marca el día de hoy (hora de Chile) como activo y devuelve la racha."""
    streak = check_in(db, user.id, chile_date(clock()))
    return StreakOut(**streak.__dict__)

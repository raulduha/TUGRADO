"""Rachas (FR-033, AC-042), recordatorios por correo (FR-034, AC-043) y ranking voluntario
(FR-039, AC-051)."""

import secrets
from collections.abc import Callable
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, SubscribedUser, get_clock, get_email_sender
from app.auth.email import EmailSender
from app.clock import chile_date
from app.config import Settings, get_settings
from app.db import get_db
from app.engagement import ranking
from app.engagement.reminders import send_due_reminders, unsubscribe
from app.engagement.streaks import check_in

router = APIRouter(prefix="/engagement", tags=["engagement"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]


class StreakOut(BaseModel):
    current: int
    best: int
    new_today: bool
    week: list[bool]


@router.post("/checkin")
def checkin(
    user: CurrentUser,
    db: Db,
    clock: Clock,
) -> StreakOut:
    """Marca el día de hoy (hora de Chile) como activo y devuelve la racha."""
    streak = check_in(db, user.id, chile_date(clock()))
    return StreakOut(**streak.__dict__)


@router.get("/reminders/run")
def run_reminders(
    db: Db,
    clock: Clock,
    settings: Annotated[Settings, Depends(get_settings)],
    sender: Annotated[EmailSender, Depends(get_email_sender)],
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, int]:
    """Lo llama Vercel Cron una vez al día con `Authorization: Bearer <CRON_SECRET>`."""
    secret = settings.cron_secret.get_secret_value() if settings.cron_secret else ""
    if not secret:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    if not secrets.compare_digest(authorization or "", f"Bearer {secret}"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return {"sent": send_due_reminders(db, sender, clock(), settings.frontend_base_url)}


class UnsubscribeIn(BaseModel):
    token: str = Field(min_length=1, max_length=64)


@router.post("/reminders/unsubscribe", status_code=status.HTTP_204_NO_CONTENT)
def unsubscribe_reminders(body: UnsubscribeIn, db: Db, clock: Clock) -> None:
    """Baja de los recordatorios desde el enlace del correo (sin iniciar sesión)."""
    if not unsubscribe(db, body.token, clock()):
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail={"code": "invalid_token", "message": "El enlace no es válido"},
        )


class RankingEntryOut(BaseModel):
    position: int
    alias: str
    xp: int
    me: bool


class RankingOut(BaseModel):
    entries: list[RankingEntryOut]
    me: RankingEntryOut | None
    alias: str | None


class AliasIn(BaseModel):
    alias: str = Field(min_length=1, max_length=40)


@router.get("/ranking")
def get_ranking(user: SubscribedUser, db: Db, clock: Clock) -> RankingOut:
    """Ranking del mes en curso, solo con quienes se inscribieron (FR-039)."""
    result = ranking.monthly(db, user.id, clock())
    return RankingOut(
        entries=[RankingEntryOut(**e.__dict__) for e in result.entries],
        me=RankingEntryOut(**result.me.__dict__) if result.me else None,
        alias=result.alias,
    )


@router.put("/ranking/profile", status_code=status.HTTP_204_NO_CONTENT)
def join_ranking(body: AliasIn, user: SubscribedUser, db: Db, clock: Clock) -> None:
    ranking.join(db, user.id, body.alias, clock())


@router.delete("/ranking/profile", status_code=status.HTTP_204_NO_CONTENT)
def leave_ranking(user: SubscribedUser, db: Db) -> None:
    ranking.leave(db, user.id)

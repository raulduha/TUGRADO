"""Glosario y rosco legal (FR-038, AC-050): administración del glosario y el juego."""

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import AdminUser, SubscribedUser, get_clock
from app.content.question import ContentError
from app.db import get_db
from app.glossary import terms
from app.persistence.auth_models import UserAccountRow
from app.persistence.content_models import SubjectRow
from app.persistence.glossary_models import GlossaryTermRow, TermStatus

admin_router = APIRouter(prefix="/admin/glossary", tags=["glossary"])
router = APIRouter(prefix="/practice/rosco", tags=["practice"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


# ------------------------------------------------------------------ administración


class TermOut(BaseModel):
    id: str
    subject: str
    term: str
    definition: str
    source: str
    status: TermStatus
    author: str
    mine: bool  # quien la cargó no puede aprobarla ni publicarla


class ImportOut(BaseModel):
    created: int = 0
    errors: list[dict] = []


class BulkIn(BaseModel):
    action: Literal["approve", "publish", "retire"]
    ids: list[uuid.UUID] = Field(min_length=1, max_length=2000)


class BulkOut(BaseModel):
    done: int
    skipped: list[dict]


@admin_router.get("")
def list_terms(
    admin: AdminUser, db: Db, status: Annotated[TermStatus | None, Query()] = None
) -> list[TermOut]:
    query = (
        select(GlossaryTermRow, SubjectRow.name, UserAccountRow.email)
        .join(SubjectRow, SubjectRow.id == GlossaryTermRow.subject_id)
        .join(UserAccountRow, UserAccountRow.id == GlossaryTermRow.created_by)
        .order_by(SubjectRow.name, GlossaryTermRow.term)
    )
    if status is not None:
        query = query.where(GlossaryTermRow.status == status)
    return [
        TermOut(
            id=str(row.id),
            subject=subject,
            term=row.term,
            definition=row.definition,
            source=row.source,
            status=row.status,
            author=author,
            mine=row.created_by == admin.id,
        )
        for row, subject, author in db.execute(query).all()
    ]


@admin_router.post("/import")
async def import_glossary(request: Request, admin: AdminUser, db: Db, clock: Clock) -> ImportOut:
    """Recibe el .xlsx como cuerpo binario. Todo o nada; los términos quedan en borrador."""
    data = await request.body()
    if len(data) > MAX_UPLOAD_BYTES:
        raise ContentError("file_too_large", "El archivo supera los 25 MB")
    parsed, errors = terms.parse_glossary(data)
    if errors:
        return ImportOut(errors=[{"row": row, "message": message} for row, message in errors])
    return ImportOut(created=terms.import_terms(db, parsed, admin.id, clock()))


@admin_router.get("/template")
def download_template(_: AdminUser) -> Response:
    return Response(
        content=terms.template(),
        media_type=XLSX,
        headers={"Content-Disposition": 'attachment; filename="plantilla-glosario.xlsx"'},
    )


@admin_router.post("/bulk")
def bulk_action(body: BulkIn, admin: AdminUser, db: Db, clock: Clock) -> BulkOut:
    done, skipped = terms.bulk(db, body.action, body.ids, admin.id, clock())
    return BulkOut(done=done, skipped=[{"id": str(i), "reason": reason} for i, reason in skipped])


# ------------------------------------------------------------------------- rosco


class RoscoItemOut(BaseModel):
    id: str
    letter: str
    mode: Literal["starts", "contains"]
    definition: str
    subject: str


class CheckIn(BaseModel):
    id: uuid.UUID
    answer: str = Field(max_length=200)


class CheckOut(BaseModel):
    correct: bool
    term: str


@router.get("")
def rosco(
    _: SubscribedUser, db: Db, subject: Annotated[str | None, Query()] = None
) -> list[RoscoItemOut]:
    """Una letra por término publicado, sin revelar la respuesta."""
    return [
        RoscoItemOut(
            id=str(item.id),
            letter=item.letter,
            mode=item.mode,
            definition=item.definition,
            subject=item.subject,
        )
        for item in terms.build_rosco(db, subject)
    ]


@router.post("/check")
def check(body: CheckIn, _: SubscribedUser, db: Db) -> CheckOut:
    """Corrige una respuesta (o un «pasapalabra» al final) y revela el término."""
    correct, term = terms.check_answer(db, body.id, body.answer)
    return CheckOut(correct=correct, term=term)

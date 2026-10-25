"""Administración del banco de preguntas (FR-013, FR-014, AC-029, AC-044, AC-046).

Cada endpoint valida la entrada, llama al servicio editorial y confirma la transacción. Las
reglas (versiones inmutables, quien crea no aprueba ni publica, nada se borra) viven en
app/content/service.py.
"""

import uuid
from collections.abc import Callable
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Request, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import AdminUser, get_clock
from app.content import queries
from app.content.question import ContentError, QuestionContent, make_content
from app.content.service import ContentService
from app.content.spreadsheet import build_workbook, parse_workbook
from app.content.sync import apply_spreadsheet, export_rows
from app.db import get_db
from app.persistence.content_models import (
    DIFFICULTY_MAX,
    DIFFICULTY_MIN,
    OPTIONS_MAX,
    OPTIONS_MIN,
    ReviewDecision,
    VersionStatus,
)

router = APIRouter(prefix="/admin/questions", tags=["content"])

Db = Annotated[Session, Depends(get_db)]
Clock = Annotated[Callable[[], datetime], Depends(get_clock)]

MAX_UPLOAD_BYTES = 25 * 1024 * 1024  # documentos importables: hasta 25 MB (README)
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _service(db: Db, clock: Clock) -> ContentService:
    return ContentService(db, clock)


Service = Annotated[ContentService, Depends(_service)]


# ---------------------------------------------------------------------------- esquemas


class VersionSummary(BaseModel):
    id: str
    question_id: str
    number: int
    status: VersionStatus
    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    author: str
    is_author: bool
    created_at: datetime


class ReviewOut(BaseModel):
    decision: ReviewDecision
    comment: str | None
    reviewer: str
    created_at: datetime


class HistoryItem(BaseModel):
    id: str
    number: int
    status: VersionStatus
    author: str
    created_at: datetime


class VersionDetail(VersionSummary):
    options: list[str]
    correct_position: int
    explanation: str
    source: str
    reviews: list[ReviewOut]
    history: list[HistoryItem]  # de la versión más nueva a la más antigua


class SubjectOut(BaseModel):
    name: str
    subtopics: list[str]


class ContentIn(BaseModel):
    subject: str = Field(max_length=200)
    subtopic: str | None = Field(default=None, max_length=200)
    difficulty: int = Field(ge=DIFFICULTY_MIN, le=DIFFICULTY_MAX)
    prompt: str
    options: list[str] = Field(min_length=OPTIONS_MIN, max_length=OPTIONS_MAX)
    correct_position: int = Field(ge=0)
    explanation: str
    source: str = Field(max_length=400)

    def to_content(self) -> QuestionContent:
        return make_content(**self.model_dump())  # mismas reglas que la planilla


class ReviewIn(BaseModel):
    decision: ReviewDecision
    comment: str | None = Field(default=None, max_length=2000)


class BulkIn(BaseModel):
    action: Literal["submit", "approve", "publish"]
    ids: list[uuid.UUID] = Field(min_length=1, max_length=2000)


class BulkOut(BaseModel):
    done: int
    skipped: list[dict]


class ImportOut(BaseModel):
    created: int = 0
    updated: int = 0
    retired: int = 0
    unchanged: int = 0
    errors: list[dict] = []


def _summary(view: queries.VersionView, me: uuid.UUID) -> VersionSummary:
    v = view.version
    return VersionSummary(
        id=str(v.id),
        question_id=str(v.question_id),
        number=v.number,
        status=v.status,
        subject=view.subject,
        subtopic=view.subtopic,
        difficulty=v.difficulty,
        prompt=v.prompt,
        author=view.author,
        is_author=v.created_by == me,
        created_at=v.created_at,
    )


# ----------------------------------------------------------------------------- planilla


@router.post("/import")
async def import_spreadsheet(request: Request, admin: AdminUser, svc: Service) -> ImportOut:
    """Recibe el .xlsx como cuerpo binario. Todo o nada: con errores no aplica ninguna fila."""
    data = await request.body()
    if len(data) > MAX_UPLOAD_BYTES:
        raise ContentError("file_too_large", "El archivo supera los 25 MB")
    rows, errors = parse_workbook(data)
    summary = None
    if not errors:
        summary, errors = apply_spreadsheet(svc, rows, admin.id)
    if summary is None:
        return ImportOut(errors=[{"row": e.row, "message": e.message} for e in errors])
    return ImportOut(**summary.__dict__)


def _xlsx(data: bytes, filename: str) -> Response:
    return Response(
        content=data,
        media_type=XLSX,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/template")
def download_template(_: AdminUser) -> Response:
    return _xlsx(build_workbook([]), "plantilla-preguntas.xlsx")


@router.get("/export")
def download_bank(_: AdminUser, svc: Service, clock: Clock) -> Response:
    """El banco actual (última versión de cada pregunta no retirada), para editar y resubir."""
    return _xlsx(build_workbook(export_rows(svc)), f"banco-preguntas-{clock():%Y-%m-%d}.xlsx")


# ------------------------------------------------------------------------------ lectura


@router.get("")
def list_versions(
    admin: AdminUser,
    db: Db,
    status_filter: Annotated[VersionStatus | None, Query(alias="status")] = None,
    subject: Annotated[str | None, Query(max_length=120)] = None,
    q: Annotated[str | None, Query(max_length=200)] = None,
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[VersionSummary]:
    views = queries.search_versions(
        db, status=status_filter, subject=subject, text=q, limit=limit, offset=offset
    )
    return [_summary(view, admin.id) for view in views]


@router.get("/subjects")
def list_subjects(_: AdminUser, db: Db) -> list[SubjectOut]:
    """Materias y subtemas existentes, para filtrar y para sugerirlos al crear o editar."""
    return [SubjectOut(name=n, subtopics=t) for n, t in queries.subjects_with_subtopics(db).items()]


@router.get("/{version_id}")
def get_version(version_id: uuid.UUID, admin: AdminUser, db: Db) -> VersionDetail:
    view = queries.version_view(db, version_id)
    if view is None:
        raise ContentError("question_not_found", "No existe esa versión de pregunta")
    v = view.version
    return VersionDetail(
        **_summary(view, admin.id).model_dump(),
        options=queries.options(db, v.id),
        correct_position=v.correct_position,
        explanation=v.explanation,
        source=v.source,
        reviews=[ReviewOut(**r.__dict__) for r in queries.reviews(db, v.id)],
        history=[
            HistoryItem(
                id=str(h.version.id),
                number=h.version.number,
                status=h.version.status,
                author=h.author,
                created_at=h.version.created_at,
            )
            for h in queries.history(db, v.question_id)
        ],
    )


# ------------------------------------------------------------------------------ cambios


@router.post("", status_code=status.HTTP_201_CREATED)
def create_question(body: ContentIn, admin: AdminUser, svc: Service) -> dict[str, str]:
    """Pregunta nueva: queda como versión 1 en borrador."""
    version = svc.create(body.to_content(), admin.id)
    svc.db.commit()
    return {"id": str(version.id)}


@router.post("/{version_id}/edit", status_code=status.HTTP_201_CREATED)
def edit_question(
    version_id: uuid.UUID, body: ContentIn, admin: AdminUser, svc: Service
) -> dict[str, str]:
    """Nunca modifica la versión: guarda la siguiente como borrador."""
    new_id = svc.edit(version_id, body.to_content(), admin.id)
    svc.db.commit()
    return {"id": str(new_id)}


@router.post("/{version_id}/submit", status_code=status.HTTP_204_NO_CONTENT)
def submit(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    svc.submit(version_id, admin.id)
    svc.db.commit()


@router.post("/{version_id}/review", status_code=status.HTTP_204_NO_CONTENT)
def review(version_id: uuid.UUID, body: ReviewIn, admin: AdminUser, svc: Service) -> None:
    svc.review(version_id, admin.id, body.decision, body.comment)
    svc.db.commit()


@router.post("/{version_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
def publish(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    svc.publish(version_id, admin.id)
    svc.db.commit()


@router.post("/{version_id}/retire", status_code=status.HTTP_204_NO_CONTENT)
def retire_version(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    """Retira una versión: la publicada sale de la práctica; un borrador queda descartado."""
    svc.retire(version_id, admin.id)
    svc.db.commit()


@router.post("/{version_id}/retire-question", status_code=status.HTTP_204_NO_CONTENT)
def retire_question(version_id: uuid.UUID, admin: AdminUser, svc: Service) -> None:
    """Retira la pregunta completa: todas sus versiones vigentes."""
    if not svc.retire_question(svc.version(version_id).question_id, admin.id):
        raise ContentError("invalid_transition", "La pregunta ya está retirada")
    svc.db.commit()


@router.post("/bulk")
def bulk_action(body: BulkIn, admin: AdminUser, svc: Service) -> BulkOut:
    """Enviar a revisión, aprobar o publicar varias versiones; las que no pueden, se saltan."""
    done, skipped = svc.bulk(body.action, body.ids, admin.id)
    return BulkOut(done=done, skipped=[{"id": str(i), "message": m} for i, m in skipped])

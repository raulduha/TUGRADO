"""Sincronización entre el banco y la planilla (AC-044): aplicar una planilla subida y armar la
planilla para descargar. El formato del archivo vive en app/content/spreadsheet.py."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import select

from app.content.question import STATUS_LABELS
from app.content.service import ContentService
from app.content.spreadsheet import ExportRow, ParsedQuestion, ParsedRetirement, ParsedRow, RowError
from app.persistence.content_models import (
    ContentAction,
    QuestionRow,
    QuestionVersionRow,
    VersionStatus,
)


@dataclass(frozen=True)
class SyncSummary:
    created: int = 0
    updated: int = 0
    retired: int = 0
    unchanged: int = 0


def apply_spreadsheet(
    service: ContentService, rows: list[ParsedRow], actor: uuid.UUID
) -> tuple[SyncSummary | None, list[RowError]]:
    """Aplica las filas en una sola transacción. Si alguna no puede aplicarse (por ahora, un id
    que no existe en el banco), no cambia nada y devuelve los errores por fila."""
    errors = _unknown_ids(service, rows)
    if errors:
        return None, errors

    created = updated = retired = unchanged = 0
    # Las preguntas nuevas reciben horas de creación correlativas: así conservan el orden de la
    # planilla, que es el orden que sigue la ruta de estudio (app/content/path.py).
    started = service.clock()
    for row in rows:
        if isinstance(row, ParsedRetirement):
            if service.retire_question(row.question_id, actor):
                retired += 1
            else:
                unchanged += 1
        elif row.question_id is None:
            service.create(
                row.content,
                actor,
                action=ContentAction.IMPORTED,
                created_at=started + timedelta(microseconds=created),
            )
            created += 1
        elif _changed(service, row):
            service.add_version(row.question_id, row.content, actor, action=ContentAction.IMPORTED)
            updated += 1
        else:
            unchanged += 1
    service.db.commit()
    return SyncSummary(created, updated, retired, unchanged), []


def export_rows(service: ContentService) -> list[ExportRow]:
    """La última versión de cada pregunta no retirada, con un estado legible para el Excel."""
    versions = service.db.scalars(
        select(QuestionVersionRow).order_by(
            QuestionVersionRow.question_id, QuestionVersionRow.number
        )
    ).all()
    history: dict[uuid.UUID, list[QuestionVersionRow]] = {}
    for version in versions:
        history.setdefault(version.question_id, []).append(version)

    rows = []
    for question_id, question_versions in history.items():
        latest = question_versions[-1]
        if latest.status == VersionStatus.RETIRED:
            continue
        status = f"v{latest.number} {STATUS_LABELS[latest.status]}"
        published = [
            v for v in question_versions if v.status == VersionStatus.PUBLISHED and v is not latest
        ]
        if published:
            status += f" · v{published[0].number} publicada"
        rows.append(ExportRow(question_id, service.content_of(latest), status))
    rows.sort(key=lambda r: (r.content.subject, r.content.subtopic or "", r.content.prompt))
    return rows


def _unknown_ids(service: ContentService, rows: list[ParsedRow]) -> list[RowError]:
    ids = {r.question_id for r in rows if r.question_id is not None}
    if not ids:
        return []
    existing = set(service.db.scalars(select(QuestionRow.id).where(QuestionRow.id.in_(ids))))
    return [
        RowError(r.row, "No existe una pregunta con ese id en el banco.")
        for r in rows
        if r.question_id is not None and r.question_id not in existing
    ]


def _changed(service: ContentService, row: ParsedQuestion) -> bool:
    assert row.question_id is not None
    latest = service.latest_version(row.question_id)
    return latest is None or service.content_of(latest) != row.content

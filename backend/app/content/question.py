"""Tipos y reglas del contenido de una pregunta, comunes a la planilla y al panel.

Las mismas reglas valen para una pregunta escrita en el formulario del panel y para una fila de
la planilla: así ambos caminos aceptan y rechazan exactamente lo mismo.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.errors import AppError
from app.persistence.content_models import (
    DIFFICULTY_MAX,
    DIFFICULTY_MIN,
    OPTIONS_MAX,
    OPTIONS_MIN,
    VersionStatus,
)

MAX_SUBJECT, MAX_SUBTOPIC, MAX_SOURCE = 120, 160, 300

STATUS_LABELS = {
    VersionStatus.DRAFT: "borrador",
    VersionStatus.IN_REVIEW: "en revisión",
    VersionStatus.APPROVED: "aprobada",
    VersionStatus.PUBLISHED: "publicada",
    VersionStatus.RETIRED: "retirada",
}


class ContentError(AppError):
    """Error de negocio del banco de preguntas (se traduce a HTTP en app/api/errors.py)."""


@dataclass(frozen=True)
class QuestionContent:
    """Lo que un administrador escribe en una versión de pregunta de alternativas."""

    subject: str
    subtopic: str | None
    difficulty: int
    prompt: str
    options: list[str]
    correct_position: int  # 0 = A, 1 = B…
    explanation: str
    source: str


def make_content(
    *,
    subject: str,
    subtopic: str | None,
    difficulty: int,
    prompt: str,
    options: list[str],
    correct_position: int,
    explanation: str,
    source: str,
) -> QuestionContent:
    """Valida y normaliza (quita espacios sobrantes). Lanza ContentError con el motivo."""
    subject, prompt = subject.strip(), prompt.strip()
    explanation, source = explanation.strip(), source.strip()
    subtopic = (subtopic or "").strip() or None
    options = [o.strip() for o in options]

    for label, value in (
        ("materia", subject),
        ("enunciado", prompt),
        ("explicacion", explanation),
        ("fuente", source),
    ):
        if not value:
            raise ContentError("invalid_content", f"Falta «{label}».")
    if len(subject) > MAX_SUBJECT or len(subtopic or "") > MAX_SUBTOPIC or len(source) > MAX_SOURCE:
        raise ContentError(
            "invalid_content",
            f"Materia ({MAX_SUBJECT}), subtema ({MAX_SUBTOPIC}) o fuente ({MAX_SOURCE}) supera "
            "el largo máximo.",
        )
    if not DIFFICULTY_MIN <= difficulty <= DIFFICULTY_MAX:
        raise ContentError(
            "invalid_content", f"La dificultad va de {DIFFICULTY_MIN} a {DIFFICULTY_MAX}."
        )
    if not OPTIONS_MIN <= len(options) <= OPTIONS_MAX:
        raise ContentError(
            "invalid_options", f"Debe tener entre {OPTIONS_MIN} y {OPTIONS_MAX} alternativas."
        )
    if any(not o for o in options):
        raise ContentError("invalid_options", "Hay alternativas vacías.")
    if len({o.casefold() for o in options}) != len(options):
        raise ContentError("invalid_options", "Hay alternativas repetidas.")
    if not 0 <= correct_position < len(options):
        raise ContentError(
            "invalid_options", "La respuesta correcta no es una de las alternativas."
        )

    return QuestionContent(
        subject=subject,
        subtopic=subtopic,
        difficulty=difficulty,
        prompt=prompt,
        options=options,
        correct_position=correct_position,
        explanation=explanation,
        source=source,
    )

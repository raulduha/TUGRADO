"""Ayudas para armar planillas de preguntas en las pruebas."""

from io import BytesIO

from openpyxl import Workbook

from app.content.spreadsheet import COLUMNS, SHEET

ROW = {
    "materia": "Derecho Civil",
    "subtema": "Personas",
    "dificultad": 1,
    "enunciado": "¿Cuándo principia la existencia legal de una persona?",
    "alternativa_a": "Desde la concepción",
    "alternativa_b": "Al nacer",
    "alternativa_c": "",
    "alternativa_d": "",
    "alternativa_e": "",
    "correcta": "B",
    "explicacion": "Principia al nacer, al separarse completamente de la madre.",
    "fuente": "Código Civil, art. 74",
}


def row(header: list[str] = COLUMNS, **overrides) -> list:
    """Una fila con las columnas de `header` (las que no están en ROW quedan vacías)."""
    values = ROW | overrides
    return [values.get(column) for column in header]


def xlsx(rows: list[list], header: list[str] = COLUMNS, sheet: str = SHEET) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(header)
    for values in rows:
        ws.append(values)
    out = BytesIO()
    wb.save(out)
    return out.getvalue()

"""Lectura de la planilla de preguntas (todo o nada, errores por fila)."""

from io import BytesIO

from openpyxl import Workbook

from app.content.importer import COLUMNS, parse_workbook


def xlsx(rows: list[list], header: list[str] | None = None, sheet: str = "Preguntas") -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet
    ws.append(header or COLUMNS)
    for values in rows:
        ws.append(values)
    out = BytesIO()
    wb.save(out)
    return out.getvalue()


def row(**overrides) -> list:
    values = {
        "materia": "Derecho Civil",
        "subtema": "Personas",
        "dificultad": 1,
        "enunciado": "¿Cuándo principia la existencia legal?",
        "alternativa_a": "Desde la concepción",
        "alternativa_b": "Al nacer",
        "alternativa_c": "",
        "alternativa_d": "",
        "alternativa_e": "",
        "correcta": "B",
        "explicacion": "Principia al nacer.",
        "fuente": "Código Civil, art. 74",
    } | overrides
    return [values[c] for c in COLUMNS]


def test_lee_una_fila_valida():
    parsed, errors = parse_workbook(xlsx([row()]))
    assert errors == []
    [q] = parsed
    assert q.options == ["Desde la concepción", "Al nacer"]
    assert q.correct_position == 1 and q.difficulty == 1 and q.subtopic == "Personas"


def test_ignora_filas_vacias():
    parsed, errors = parse_workbook(xlsx([row(), [None] * len(COLUMNS)]))
    assert len(parsed) == 1 and errors == []


def test_informa_cada_fila_con_error():
    bad = [
        row(dificultad=4),
        row(correcta="C"),  # apunta a una alternativa vacía
        row(alternativa_b="", alternativa_c="Al nacer"),  # hueco entre alternativas
        row(enunciado=""),
        row(alternativa_b="desde la concepción"),  # repetida
    ]
    parsed, errors = parse_workbook(xlsx(bad))
    assert parsed == []
    assert [e.row for e in errors] == [2, 3, 4, 5, 6]
    assert "1 a 3" in errors[0].message


def test_rechaza_archivos_que_no_son_la_plantilla():
    assert parse_workbook(b"no es un excel")[1][0].row == 0
    assert "Falta la hoja" in parse_workbook(xlsx([row()], sheet="Hoja1"))[1][0].message
    assert "Faltan columnas" in parse_workbook(xlsx([row()], header=["materia"]))[1][0].message


def test_la_plantilla_oficial_se_lee_sin_errores():
    from pathlib import Path

    data = (Path(__file__).parents[2] / "docs/plantillas/preguntas-alternativas.xlsx").read_bytes()
    parsed, errors = parse_workbook(data)
    assert errors == [] and len(parsed) == 2

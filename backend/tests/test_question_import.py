"""Lectura de la planilla de preguntas (todo o nada, errores por fila)."""

import uuid
from io import BytesIO

from openpyxl import Workbook

from app.content.importer import COLUMNS, ParsedRetirement, parse_workbook
from app.content.service import QuestionContent
from app.content.workbook import HEADER, ExportRow, build_workbook


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


QID = uuid.UUID("3f2d7c1e-5b0a-4c8e-9d61-2a7b9c0e4f13")


def with_id(qid="", retirar="", **overrides) -> list:
    return [qid, *row(**overrides), "v1 publicada", retirar]


def test_las_columnas_id_retirar_y_estado_son_opcionales_e_informativas():
    parsed, errors = parse_workbook(xlsx([with_id(str(QID)), with_id()], header=HEADER))
    assert errors == []
    assert parsed[0].question_id == QID and parsed[1].question_id is None


def test_retirar_solo_exige_el_id():
    rows = [with_id(str(QID), retirar="Sí", enunciado="", correcta="Z")]
    parsed, errors = parse_workbook(xlsx(rows, header=HEADER))
    assert errors == [] and parsed == [ParsedRetirement(row=2, question_id=QID)]


def test_errores_de_id_y_retirar():
    rows = [
        with_id("no-es-un-id"),
        with_id(retirar="sí"),  # sin id
        with_id(str(QID), retirar="tal vez"),
        with_id(str(QID)),
        with_id(str(QID)),  # repetido
    ]
    parsed, errors = parse_workbook(xlsx(rows, header=HEADER))
    assert [e.row for e in errors] == [2, 3, 4, 6]
    assert "fila 5" in errors[-1].message


def test_la_planilla_descargada_se_vuelve_a_leer_igual():
    content = QuestionContent(
        subject="Derecho Civil",
        subtopic=None,
        difficulty=3,
        prompt="¿Pregunta?",
        options=["Uno", "Dos", "Tres", "Cuatro", "Cinco"],
        correct_position=4,
        explanation="Porque sí.",
        source="Código Civil, art. 1",
    )
    parsed, errors = parse_workbook(build_workbook([ExportRow(QID, content, "v1 borrador")]))
    assert errors == []
    [q] = parsed
    assert q.question_id == QID and q.options == content.options and q.correct_position == 4
    assert parse_workbook(build_workbook([]))[1][0].message == "La planilla no tiene preguntas."

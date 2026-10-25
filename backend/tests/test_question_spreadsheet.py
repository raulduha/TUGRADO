"""Formato de la planilla de preguntas: qué se acepta, cómo se informan los errores y que lo
que se descarga se pueda volver a subir (AC-044). Sin base de datos."""

import uuid
from pathlib import Path

from app.content.question import QuestionContent
from app.content.spreadsheet import (
    HEADER,
    ExportRow,
    ParsedQuestion,
    ParsedRetirement,
    build_workbook,
    parse_workbook,
)
from tests.spreadsheet import row, xlsx

QID = uuid.UUID("3f2d7c1e-5b0a-4c8e-9d61-2a7b9c0e4f13")


def test_una_fila_valida_se_convierte_en_contenido_normalizado():
    rows = [
        row(enunciado="  ¿Cuándo principia la existencia legal?  ", subtema="", correcta="b"),
        [None] * len(row()),  # las filas vacías se ignoran
    ]
    parsed, errors = parse_workbook(xlsx(rows))
    assert errors == []
    [q] = parsed
    assert q.question_id is None  # sin id: pregunta nueva
    assert q.content.prompt == "¿Cuándo principia la existencia legal?"
    assert q.content.subtopic is None
    assert q.content.options == ["Desde la concepción", "Al nacer"]  # hasta la última escrita
    assert q.content.correct_position == 1


def test_cada_fila_invalida_se_informa_con_su_numero_y_ninguna_se_acepta():
    rows = [
        row(),  # fila 2: válida, pero no basta para aceptar la planilla
        row(dificultad=4),
        row(correcta="C"),  # apunta a una alternativa vacía
        row(alternativa_b="", alternativa_c="Al nacer"),  # hueco entre alternativas
        row(enunciado=""),
        row(alternativa_b="desde la concepción"),  # repetida (sin distinguir mayúsculas)
    ]
    parsed, errors = parse_workbook(xlsx(rows))
    messages = {e.row: e.message for e in errors}
    assert list(messages) == [3, 4, 5, 6, 7]
    assert "1 a 3" in messages[3]
    assert "entre A y B" in messages[4]
    assert "seguidas" in messages[5]
    assert "enunciado" in messages[6]
    assert "repetidas" in messages[7]
    assert (
        len(parsed) == 1
    )  # la API no aplica nada si hay errores (ver test_question_spreadsheet_sync)


def test_el_archivo_debe_ser_la_plantilla():
    assert parse_workbook(b"no es un excel")[1][0].message.startswith("El archivo no es")
    assert "Falta la hoja" in parse_workbook(xlsx([row()], sheet="Hoja1"))[1][0].message
    assert "Faltan columnas" in parse_workbook(xlsx([["x"]], header=["materia"]))[1][0].message


def test_id_y_retirar_deciden_la_operacion_de_cada_fila():
    rows = [
        row(HEADER, id=str(QID)),  # existente: puede traer cambios
        row(HEADER, id=str(uuid.uuid4()), retirar="Sí", enunciado="", correcta="Z"),  # retirar
        row(HEADER),  # nueva
    ]
    parsed, errors = parse_workbook(xlsx(rows, header=HEADER))
    assert errors == []
    existing, retirement, new = parsed
    assert isinstance(existing, ParsedQuestion) and existing.question_id == QID
    # Para retirar basta el id: el resto de la fila no se valida.
    assert isinstance(retirement, ParsedRetirement)
    assert isinstance(new, ParsedQuestion) and new.question_id is None


def test_errores_de_id_y_de_retirar():
    rows = [
        row(HEADER, id="no-es-un-id"),
        row(HEADER, retirar="sí"),  # retirar sin id
        row(HEADER, id=str(QID), retirar="tal vez"),
        row(HEADER, id=str(QID)),
        row(HEADER, id=str(QID)),  # el mismo id dos veces
    ]
    _, errors = parse_workbook(xlsx(rows, header=HEADER))
    assert [e.row for e in errors] == [2, 3, 4, 6]
    assert "fila 5" in errors[-1].message


def test_la_planilla_generada_se_vuelve_a_leer_igual():
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
    assert errors == [] and parsed == [ParsedQuestion(row=2, content=content, question_id=QID)]
    # La plantilla vacía también es una planilla válida, solo que sin preguntas.
    assert parse_workbook(build_workbook([]))[1][0].message == "La planilla no tiene preguntas."


def test_la_plantilla_oficial_de_docs_sigue_siendo_valida():
    data = (Path(__file__).parents[2] / "docs/plantillas/preguntas-alternativas.xlsx").read_bytes()
    parsed, errors = parse_workbook(data)
    assert errors == [] and len(parsed) == 2

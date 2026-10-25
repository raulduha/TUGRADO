"""Práctica y ruta de estudio del estudiante (FR-006, AC-044, AC-045): solo preguntas
publicadas, la respuesta se revela al responder y el avance sale de las respuestas registradas."""

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.content_models import PracticeAttemptRow
from tests.api.bank import (
    AUTHOR,
    as_admin,
    create_question,
    import_rows,
    publish,
    publish_all,
    student,
)
from tests.spreadsheet import row

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]

# Cuatro subtemas de tres preguntas: la ruta los junta en dos lecciones de seis.
SUBTOPICS = ["Fuentes", "Interpretación", "Efectos en el tiempo", "Efectos en el espacio"]


def publish_lessons(api) -> None:
    as_admin(api, AUTHOR)
    rows = [row(subtema=s, enunciado=f"{s}: pregunta {n}") for s in SUBTOPICS for n in (1, 2, 3)]
    assert import_rows(api, rows)["created"] == 12
    publish_all(api)


def test_la_practica_solo_usa_publicadas_y_revela_la_respuesta_al_responder(
    api, outbox, engine, clock
):
    as_admin(api, AUTHOR)
    draft = create_question(api, prompt="Todavía en borrador")
    published = create_question(api)
    publish(api, published)

    student(api, outbox, engine, clock)
    [question] = api.get("/practice/questions").json()
    assert question["id"] == published  # el borrador no aparece
    assert "correct_position" not in question and "explanation" not in question

    wrong = api.post("/practice/answers", json={"version_id": published, "position": 1}).json()
    assert (wrong["correct"], wrong["correct_position"]) == (False, 0)
    assert wrong["source"] == "Código Orgánico de Tribunales, art. 1"
    assert (
        api.post("/practice/answers", json={"version_id": draft, "position": 0}).status_code == 404
    )
    assert (
        api.post("/practice/answers", json={"version_id": published, "position": 7}).status_code
        == 400
    )
    with Session(engine) as db:
        assert len(db.scalars(select(PracticeAttemptRow)).all()) == 1


def test_sin_suscripcion_no_hay_practica_ni_ruta(api, outbox, engine, clock):
    student(api, outbox, engine, clock, with_access=False)
    assert api.get("/practice/questions").status_code == 402
    assert api.get("/practice/path").status_code == 402


def test_la_ruta_agrupa_subtemas_consecutivos_en_lecciones(api, outbox, engine, clock):
    publish_lessons(api)
    student(api, outbox, engine, clock)

    [unit] = api.get("/practice/path").json()["units"]
    assert unit["subject"] == "Derecho Civil"
    assert [(lesson["subtopics"], lesson["total"]) for lesson in unit["lessons"]] == [
        (SUBTOPICS[:2], 6),
        (SUBTOPICS[2:], 6),
    ]
    lesson = api.get(f"/practice/lessons/{unit['lessons'][0]['id']}").json()
    assert [q["prompt"] for q in lesson["questions"]][:3] == [
        "Fuentes: pregunta 1",
        "Fuentes: pregunta 2",
        "Fuentes: pregunta 3",
    ]
    assert "correct_position" not in lesson["questions"][0]
    assert api.get("/practice/lessons/no-existe").status_code == 404


def test_estrellas_y_xp_salen_del_ultimo_intento_de_cada_pregunta(api, outbox, engine, clock):
    publish_lessons(api)
    student(api, outbox, engine, clock)
    first = api.get("/practice/path").json()["units"][0]["lessons"][0]
    questions = api.get(f"/practice/lessons/{first['id']}").json()["questions"]

    def answer(question, correct: bool):
        position = 1 if correct else 0  # en la planilla de prueba la correcta es la B
        clock.advance(5)  # cada respuesta llega en otro momento: cuenta la más reciente
        api.post("/practice/answers", json={"version_id": question["id"], "position": position})

    def first_lesson():
        path = api.get("/practice/path").json()
        return path["units"][0]["lessons"][0], path["xp"]

    for question in questions[:-1]:
        answer(question, correct=True)
    lesson, _ = first_lesson()
    assert (lesson["completed"], lesson["stars"]) == (False, 0)  # falta una

    answer(questions[-1], correct=False)
    lesson, xp = first_lesson()
    assert (lesson["completed"], lesson["correct"], lesson["stars"], xp) == (True, 5, 2, 50)

    answer(questions[-1], correct=True)  # repetirla y acertar mejora la lección
    lesson, xp = first_lesson()
    assert (lesson["stars"], xp) == (3, 60)

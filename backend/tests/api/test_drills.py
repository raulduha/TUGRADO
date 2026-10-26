"""Prueba cronometrada y flashcards (FR-037, AC-049): solo preguntas publicadas, la prueba se
corrige al entregar y registra las respuestas dadas, y las flashcards priorizan el repaso."""

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

DAY = 24 * 3600
RIGHT, WRONG = 1, 0  # en la planilla de prueba la correcta es la B


def publish_civil(api, n: int = 6) -> None:
    as_admin(api, AUTHOR)
    import_rows(api, [row(subtema="Fuentes", enunciado=f"Civil {i}") for i in range(n)])
    publish_all(api)


def attempts(engine) -> list[PracticeAttemptRow]:
    with Session(engine) as db:
        return list(db.scalars(select(PracticeAttemptRow)))


def test_la_prueba_filtra_por_materia_y_no_revela_respuestas(api, outbox, engine, clock):
    publish_civil(api, 3)
    as_admin(api, AUTHOR)
    procesal = create_question(api)  # Derecho Procesal
    publish(api, procesal)
    as_admin(api, AUTHOR)
    create_question(api, prompt="Borrador sin publicar")
    student(api, outbox, engine, clock)

    everything = api.get("/practice/exam", params={"size": 10}).json()
    assert len(everything) == 4  # el borrador no aparece
    assert all("correct_position" not in q and "explanation" not in q for q in everything)
    only_procesal = api.get(
        "/practice/exam", params={"subject": "Derecho Procesal", "size": 10}
    ).json()
    assert [q["id"] for q in only_procesal] == [procesal]


def test_al_entregar_se_corrige_todo_y_se_registran_solo_las_respondidas(
    api, outbox, engine, clock
):
    publish_civil(api, 4)
    student(api, outbox, engine, clock)
    q = [x["id"] for x in api.get("/practice/exam", params={"size": 4}).json()]

    result = api.post(
        "/practice/exam/grade",
        json={
            "answers": [
                {"version_id": q[0], "position": RIGHT},
                {"version_id": q[1], "position": WRONG},
                {"version_id": q[2], "position": None},  # sin responder
                {"version_id": q[3], "position": 9},  # alternativa inexistente
            ]
        },
    ).json()

    assert (result["correct"], result["total"]) == (1, 4)
    by_id = {item["id"]: item for item in result["items"]}
    assert by_id[q[1]]["correct_position"] == RIGHT and by_id[q[1]]["explanation"]
    assert by_id[q[2]]["chosen"] is None and by_id[q[3]]["chosen"] is None
    assert result["by_subtopic"] == [
        {"subject": "Derecho Civil", "subtopic": "Fuentes", "correct": 1, "total": 4}
    ]
    # Solo las dos respondidas cuentan como intento, y alimentan la ruta y el repaso.
    assert sorted(a.correct for a in attempts(engine)) == [False, True]
    [unit] = api.get("/practice/path").json()["units"]
    assert unit["mastered"] == 1
    clock.advance(DAY)
    assert [x["id"] for x in api.get("/practice/review").json()] == [q[1]]


def test_las_flashcards_muestran_primero_lo_que_toca_repasar(api, outbox, engine, clock):
    publish_civil(api, 5)
    student(api, outbox, engine, clock)
    q = [x["id"] for x in api.get("/practice/exam", params={"size": 5}).json()]
    api.post(
        "/practice/exam/grade",
        json={
            "answers": [
                {"version_id": q[0], "position": WRONG},
                {"version_id": q[1], "position": RIGHT},
            ]
        },
    )
    clock.advance(DAY)

    cards = api.get("/practice/flashcards", params={"limit": 5}).json()
    assert [c["status"] for c in cards] == ["review", "pending", "pending", "pending", "mastered"]
    assert (cards[0]["id"], cards[-1]["id"]) == (q[0], q[1])
    card = cards[0]
    assert card["options"][card["correct_position"]] == "Al nacer"  # muestra la correcta
    before = len(attempts(engine))
    api.get("/practice/flashcards")
    assert len(attempts(engine)) == before  # mirar tarjetas no registra respuestas


def test_sin_suscripcion_no_hay_prueba_ni_flashcards(api, outbox, engine, clock):
    student(api, outbox, engine, clock, with_access=False)
    assert api.get("/practice/exam").status_code == 402
    assert api.get("/practice/flashcards").status_code == 402

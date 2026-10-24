"""Ruta de estudio tipo Duolingo y acciones masivas del banco (FR-006, FR-014, AC-029)."""

import pytest
from sqlalchemy.orm import Session

from app.billing.grants import grant_access
from tests.api.test_auth import EMAIL, login, verified_account
from tests.api.test_content import AUTHOR, REVIEWER, admins, as_admin  # noqa: F401
from tests.test_question_import import row, xlsx

# `admins` (importado) crea a la autora y al revisor en cada prueba.
pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]

# Cuatro subtemas de tres preguntas: dos lecciones de seis (A+B y C+D).
SUBTOPICS = ["Fuentes", "Interpretación", "Efectos en el tiempo", "Efectos en el espacio"]


def publish_bank(api, clock) -> list[str]:
    rows = []
    for subtopic in SUBTOPICS:
        for n in range(3):
            rows.append(row(subtema=subtopic, enunciado=f"{subtopic}: pregunta {n + 1}"))
    as_admin(api, AUTHOR)
    assert api.post("/admin/questions/import", content=xlsx(rows)).json()["created"] == 12
    ids = [v["id"] for v in api.get("/admin/questions").json()]
    assert api.post("/admin/questions/bulk", json={"action": "submit", "ids": ids}).json() == {
        "done": 12,
        "skipped": [],
    }
    # La autora no puede aprobar lo suyo: todo se salta con el motivo.
    own = api.post("/admin/questions/bulk", json={"action": "approve", "ids": ids}).json()
    assert own["done"] == 0 and "otro administrador" in own["skipped"][0]["message"]

    as_admin(api, REVIEWER)
    for action in ("approve", "publish"):
        result = api.post("/admin/questions/bulk", json={"action": action, "ids": ids}).json()
        assert result["done"] == 12
    return ids


def student(api, outbox, engine, clock):
    verified_account(api, outbox)
    with Session(engine) as db:
        grant_access(db, EMAIL, "Pruebas", "equipo@proda.cl", clock())
    login(api)


def test_la_ruta_agrupa_subtemas_en_lecciones_y_registra_el_avance(api, outbox, engine, clock):
    publish_bank(api, clock)
    student(api, outbox, engine, clock)

    path = api.get("/practice/path").json()
    assert path["xp"] == 0
    [unit] = path["units"]
    assert unit["subject"] == "Derecho Civil"
    first, second = unit["lessons"]
    assert first["subtopics"] == SUBTOPICS[:2] and first["total"] == 6
    assert second["subtopics"] == SUBTOPICS[2:] and second["stars"] == 0

    lesson = api.get(f"/practice/lessons/{first['id']}").json()
    assert [q["prompt"] for q in lesson["questions"]][:2] == [
        "Fuentes: pregunta 1",
        "Fuentes: pregunta 2",
    ]
    assert "correct_position" not in lesson["questions"][0]

    # Acierta 5 de 6 (la correcta es la B, posición 1).
    for i, q in enumerate(lesson["questions"]):
        api.post("/practice/answers", json={"version_id": q["id"], "position": 0 if i == 0 else 1})
    first = api.get("/practice/path").json()["units"][0]["lessons"][0]
    assert first["completed"] and first["correct"] == 5 and first["stars"] == 2

    # Repite la primera y acierta: cuenta el último intento.
    api.post("/practice/answers", json={"version_id": lesson["questions"][0]["id"], "position": 1})
    path = api.get("/practice/path").json()
    assert path["units"][0]["lessons"][0]["stars"] == 3
    assert path["xp"] == 60


def test_lecciones_inexistentes_y_acceso(api, outbox, engine, clock):
    publish_bank(api, clock)
    verified_account(api, outbox)
    login(api)
    assert api.get("/practice/path").status_code == 402  # sin suscripción
    with Session(engine) as db:
        grant_access(db, EMAIL, "Pruebas", "equipo@proda.cl", clock())
    response = api.get("/practice/lessons/no-existe")
    assert response.status_code == 404 and response.json()["detail"]["code"] == "lesson_not_found"


def test_acciones_masivas_validan_la_accion(api):
    as_admin(api, AUTHOR)
    response = api.post("/admin/questions/bulk", json={"action": "borrar", "ids": []})
    assert response.status_code == 422

"""Plan diario del estudiante (FR-035, AC-047): fecha del examen, meta, avance del día, repaso de
errores y preparación por cédula, todo derivado de las respuestas registradas."""

import pytest

from tests.api.bank import AUTHOR, as_admin, import_rows, publish_all, student
from tests.spreadsheet import row

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]

DAY = 24 * 3600
# El reloj de las pruebas parte el 1 de enero de 2026 a las 9:00 de Chile.
TODAY = "2026-01-01"


def setup(api, outbox, engine, clock, questions: int = 10) -> list[str]:
    """Publica `questions` preguntas de Civil, deja la sesión del estudiante y devuelve los ids."""
    as_admin(api, AUTHOR)
    rows = [row(subtema="Fuentes", enunciado=f"Pregunta {n}") for n in range(questions)]
    import_rows(api, rows)
    publish_all(api)
    student(api, outbox, engine, clock)
    [unit] = api.get("/practice/path").json()["units"]
    return [
        q["id"]
        for lesson in unit["lessons"]
        for q in api.get(f"/practice/lessons/{lesson['id']}").json()["questions"]
    ]


def answer(api, clock, version_id: str, correct: bool) -> None:
    clock.advance(5)
    position = 1 if correct else 0  # en la planilla de prueba la correcta es la B
    api.post("/practice/answers", json={"version_id": version_id, "position": position})


def test_sin_configurar_no_hay_cuenta_regresiva_ni_meta_sugerida(api, outbox, engine, clock):
    setup(api, outbox, engine, clock)
    today = api.get("/study/today").json()
    assert today == {
        "exam_date": None,
        "days_left": None,
        "daily_goal": None,
        "suggested_goal": None,
        "answered_today": 0,
        "review_due": 0,
        "remaining": 10,
    }


def test_con_fecha_de_examen_cuenta_los_dias_y_sugiere_la_meta(api, outbox, engine, clock):
    setup(api, outbox, engine, clock, questions=40)
    saved = api.put("/study/profile", json={"exam_date": "2026-01-05", "daily_goal": 20})
    assert saved.status_code == 204

    today = api.get("/study/today").json()
    assert (today["days_left"], today["daily_goal"]) == (4, 20)
    assert today["suggested_goal"] == 10  # 40 preguntas por dominar en 4 días

    past = api.put("/study/profile", json={"exam_date": "2025-12-31"})
    assert past.status_code == 400
    assert past.json()["detail"]["code"] == "invalid_exam_date"
    assert api.put("/study/profile", json={"daily_goal": 0}).status_code == 422


def test_el_avance_del_dia_se_cuenta_en_hora_de_chile(api, outbox, engine, clock):
    ids = setup(api, outbox, engine, clock)
    answer(api, clock, ids[0], correct=True)
    answer(api, clock, ids[1], correct=False)
    assert api.get("/study/today").json()["answered_today"] == 2

    clock.advance(14 * 3600)  # 23:00 en Chile, 02:00 UTC del día siguiente: sigue siendo hoy
    answer(api, clock, ids[2], correct=True)
    assert api.get("/study/today").json()["answered_today"] == 3

    clock.advance(2 * 3600)  # ya es mañana en Chile
    assert api.get("/study/today").json()["answered_today"] == 0


def test_los_errores_vuelven_al_dia_siguiente_como_repaso(api, outbox, engine, clock):
    ids = setup(api, outbox, engine, clock)
    answer(api, clock, ids[0], correct=False)
    answer(api, clock, ids[1], correct=True)
    assert api.get("/practice/review").json() == []
    assert api.get("/study/today").json()["review_due"] == 0

    clock.advance(DAY)
    [due] = api.get("/practice/review").json()
    assert due["id"] == ids[0] and "correct_position" not in due
    assert api.get("/study/today").json()["review_due"] == 1

    answer(api, clock, ids[0], correct=True)  # acertada en el repaso: vuelve en 3 días
    assert api.get("/practice/review").json() == []


def test_la_preparacion_por_cedula_cuenta_las_que_domina(api, outbox, engine, clock):
    ids = setup(api, outbox, engine, clock)
    answer(api, clock, ids[0], correct=True)
    answer(api, clock, ids[1], correct=True)
    answer(api, clock, ids[2], correct=False)

    [unit] = api.get("/practice/path").json()["units"]
    assert (unit["mastered"], unit["total"]) == (2, 10)
    assert api.get("/study/today").json()["remaining"] == 8


def test_sin_suscripcion_no_hay_plan_diario(api, outbox, engine, clock):
    student(api, outbox, engine, clock, with_access=False)
    assert api.get("/study/today").status_code == 402
    assert api.get("/practice/review").status_code == 402

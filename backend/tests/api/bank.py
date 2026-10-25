"""Ayudas para las pruebas del banco de preguntas: administradores, preguntas y estudiantes."""

from sqlalchemy.orm import Session

from app.billing.grants import grant_access
from tests.api.test_auth import EMAIL, login, verified_account
from tests.spreadsheet import xlsx

ADMIN_PASSWORD = "administra el banco 2026"
AUTHOR, REVIEWER = "autora@ejemplo.cl", "revisor@ejemplo.cl"

QUESTION = {
    "subject": "Derecho Procesal",
    "subtopic": "La jurisdicción",
    "difficulty": 2,
    "prompt": "¿Qué es la jurisdicción?",
    "options": ["Un poder-deber del Estado", "Un contrato", "Una costumbre"],
    "correct_position": 0,
    "explanation": "Es el poder-deber de resolver conflictos con efecto de cosa juzgada.",
    "source": "Código Orgánico de Tribunales, art. 1",
}


def as_admin(api, email: str) -> None:
    assert login(api, email=email, password=ADMIN_PASSWORD).status_code == 204


def create_question(api, **overrides) -> str:
    """Crea una pregunta desde el panel con la sesión actual y devuelve el id de su versión."""
    response = api.post("/admin/questions", json=QUESTION | overrides)
    assert response.status_code == 201, response.json()
    return response.json()["id"]


def import_rows(api, rows: list[list]) -> dict:
    return api.post("/admin/questions/import", content=xlsx(rows)).json()


def publish(api, version_id: str) -> None:
    """La autora envía a revisión y el revisor aprueba y publica. Deja la sesión del revisor."""
    as_admin(api, AUTHOR)
    assert api.post(f"/admin/questions/{version_id}/submit").status_code == 204
    as_admin(api, REVIEWER)
    review = api.post(f"/admin/questions/{version_id}/review", json={"decision": "approved"})
    assert review.status_code == 204
    assert api.post(f"/admin/questions/{version_id}/publish").status_code == 204


def publish_all(api) -> None:
    """Publica todo lo que esté en borrador con las acciones masivas (autora y revisor)."""
    as_admin(api, AUTHOR)
    drafts = [v["id"] for v in api.get("/admin/questions", params={"status": "draft"}).json()]
    api.post("/admin/questions/bulk", json={"action": "submit", "ids": drafts})
    as_admin(api, REVIEWER)
    for action in ("approve", "publish"):
        result = api.post("/admin/questions/bulk", json={"action": action, "ids": drafts}).json()
        assert result["skipped"] == [], result


def student(api, outbox, engine, clock, *, with_access: bool = True) -> None:
    """Deja la sesión de un estudiante, con acceso de cortesía al estudio salvo que se indique."""
    verified_account(api, outbox)
    if with_access:
        with Session(engine) as db:
            grant_access(db, EMAIL, "Pruebas", "equipo@proda.cl", clock())
    assert login(api).status_code == 204

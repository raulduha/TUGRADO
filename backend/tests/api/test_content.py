"""Banco de preguntas: importación, revisión por otro administrador y práctica (FR-006,
FR-013, FR-014, AC-029)."""

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.billing.grants import grant_access
from app.cli import create_admin
from app.persistence.content_models import ContentEventRow, PracticeAttemptRow
from tests.api.test_auth import EMAIL, code, login, verified_account
from tests.test_question_import import row, xlsx

pytestmark = pytest.mark.integration

PASSWORD = "administra el banco 2026"
AUTHOR, REVIEWER = "autora@ejemplo.cl", "revisor@ejemplo.cl"


@pytest.fixture
def admins(engine, monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", PASSWORD)
    create_admin(AUTHOR, engine=engine)
    create_admin(REVIEWER, engine=engine)


def as_admin(api, email):
    assert login(api, email=email, password=PASSWORD).status_code == 204


def import_one(api) -> str:
    as_admin(api, AUTHOR)
    response = api.post("/admin/questions/import", content=xlsx([row()]))
    assert response.json() == {"imported": 1, "errors": []}
    [version] = api.get("/admin/questions").json()
    return version["id"]


def approve_and_publish(api, vid):
    as_admin(api, REVIEWER)
    assert (
        api.post(f"/admin/questions/{vid}/review", json={"decision": "approved"}).status_code == 204
    )
    assert api.post(f"/admin/questions/{vid}/publish").status_code == 204


def test_importar_con_errores_no_importa_nada(api, admins):
    as_admin(api, AUTHOR)
    response = api.post("/admin/questions/import", content=xlsx([row(), row(dificultad=9)]))
    body = response.json()
    assert body["imported"] == 0 and body["errors"][0]["row"] == 3
    assert api.get("/admin/questions").json() == []


def test_flujo_completo_y_quien_crea_no_aprueba_ni_publica(api, admins):
    vid = import_one(api)
    assert api.get(f"/admin/questions/{vid}").json()["status"] == "draft"
    assert api.post(f"/admin/questions/{vid}/submit").status_code == 204

    # La autora no puede revisar su propia versión.
    response = api.post(f"/admin/questions/{vid}/review", json={"decision": "approved"})
    assert response.status_code == 403 and code(response) == "author_cannot_review"

    as_admin(api, REVIEWER)
    assert api.post(f"/admin/questions/{vid}/publish").status_code == 409  # aún no aprobada
    approve_and_publish(api, vid)
    detail = api.get(f"/admin/questions/{vid}").json()
    assert detail["status"] == "published" and detail["reviews"][0]["reviewer"] == REVIEWER


def test_la_autora_tampoco_publica_aunque_otro_apruebe(api, admins):
    vid = import_one(api)
    api.post(f"/admin/questions/{vid}/submit")
    as_admin(api, REVIEWER)
    api.post(f"/admin/questions/{vid}/review", json={"decision": "approved"})
    as_admin(api, AUTHOR)
    response = api.post(f"/admin/questions/{vid}/publish")
    assert response.status_code == 403 and code(response) == "author_cannot_review"


def test_pedir_cambios_exige_comentario_y_vuelve_a_borrador(api, admins):
    vid = import_one(api)
    api.post(f"/admin/questions/{vid}/submit")
    as_admin(api, REVIEWER)
    response = api.post(f"/admin/questions/{vid}/review", json={"decision": "changes_requested"})
    assert response.status_code == 400
    response = api.post(
        f"/admin/questions/{vid}/review",
        json={"decision": "changes_requested", "comment": "Citar el artículo completo"},
    )
    assert response.status_code == 204
    assert api.get(f"/admin/questions/{vid}").json()["status"] == "draft"


def test_editar_crea_version_nueva_y_publicarla_retira_la_anterior(api, admins, engine):
    vid = import_one(api)
    api.post(f"/admin/questions/{vid}/submit")
    approve_and_publish(api, vid)

    # El revisor edita: nace la versión 2 como borrador, con él como autor.
    edit = {
        "subject": "Derecho Civil",
        "subtopic": "Personas",
        "difficulty": 2,
        "prompt": "¿Cuándo principia la existencia legal de toda persona?",
        "options": ["Desde la concepción", "Al nacer", "Al inscribirse"],
        "correct_position": 1,
        "explanation": "Al separarse completamente de su madre.",
        "source": "Código Civil, art. 74",
    }
    v2 = api.post(f"/admin/questions/{vid}/edit", json=edit).json()["id"]
    assert api.get(f"/admin/questions/{vid}").json()["status"] == "published"  # intacta
    v2_detail = api.get(f"/admin/questions/{v2}").json()
    assert v2_detail["number"] == 2 and v2_detail["is_author"] is True

    api.post(f"/admin/questions/{v2}/submit")
    as_admin(api, AUTHOR)  # ahora la autora original revisa y publica la v2
    api.post(f"/admin/questions/{v2}/review", json={"decision": "approved"})
    assert api.post(f"/admin/questions/{v2}/publish").status_code == 204
    assert api.get(f"/admin/questions/{vid}").json()["status"] == "retired"
    assert api.get(f"/admin/questions/{v2}").json()["status"] == "published"
    with Session(engine) as db:
        actions = [
            e.action for e in db.scalars(select(ContentEventRow).order_by(ContentEventRow.id))
        ]
    assert actions.count("published") == 2 and "retired" in actions


def test_un_estudiante_no_administra_el_banco(api, outbox):
    verified_account(api, outbox)
    login(api)
    assert api.get("/admin/questions").status_code == 403
    assert api.post("/admin/questions/import", content=b"x").status_code == 403


def test_la_practica_solo_usa_publicadas_y_revela_la_respuesta_al_responder(
    api, admins, outbox, engine, clock
):
    vid = import_one(api)
    api.post(f"/admin/questions/{vid}/submit")

    verified_account(api, outbox)
    with Session(engine) as db:
        grant_access(db, EMAIL, "Pruebas", "equipo@proda.cl", clock())
    login(api)
    assert api.get("/practice/questions").json() == []  # en revisión: no se muestra

    approve_and_publish(api, vid)
    login(api)
    [question] = api.get("/practice/questions").json()
    assert question["options"] == ["Desde la concepción", "Al nacer"]
    assert "correct_position" not in question and "explanation" not in question

    wrong = api.post("/practice/answers", json={"version_id": vid, "position": 0}).json()
    assert wrong["correct"] is False and wrong["correct_position"] == 1
    assert wrong["source"] == "Código Civil, art. 74"
    assert api.post("/practice/answers", json={"version_id": vid, "position": 7}).status_code == 400
    with Session(engine) as db:
        assert len(list(db.scalars(select(PracticeAttemptRow)))) == 1


def test_la_practica_exige_acceso(api, outbox):
    verified_account(api, outbox)
    login(api)
    assert api.get("/practice/questions").status_code == 402

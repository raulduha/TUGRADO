"""Flujo editorial del banco de preguntas desde el panel (FR-013, FR-014, AC-029, AC-046):
versiones inmutables, revisión por otro administrador, retiro sin borrar y búsqueda."""

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.content_models import ContentEventRow, QuestionVersionRow
from tests.api.bank import AUTHOR, QUESTION, REVIEWER, as_admin, create_question, publish
from tests.api.test_auth import code, login, verified_account

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]


def detail(api, version_id: str) -> dict:
    return api.get(f"/admin/questions/{version_id}").json()


# ------------------------------------------------------------------ crear y validar


def test_una_pregunta_nueva_queda_como_borrador_v1_de_quien_la_crea(api):
    as_admin(api, AUTHOR)
    created = detail(api, create_question(api))
    assert (created["status"], created["number"], created["is_author"]) == ("draft", 1, True)
    assert created["options"] == QUESTION["options"]
    assert [h["number"] for h in created["history"]] == [1]


def test_el_formulario_aplica_las_mismas_reglas_que_la_planilla(api):
    as_admin(api, AUTHOR)
    for overrides, expected in (
        ({"options": ["Sí", " sí "]}, "invalid_options"),  # repetidas
        ({"correct_position": 3}, "invalid_options"),  # no es una de las alternativas
        ({"prompt": "   "}, "invalid_content"),  # vacío tras quitar espacios
    ):
        response = api.post("/admin/questions", json=QUESTION | overrides)
        assert (response.status_code, code(response)) == (400, expected), overrides
    assert api.get("/admin/questions").json() == []


# ------------------------------------------------------------- revisar y publicar


def test_quien_crea_una_version_no_la_aprueba_ni_la_publica(api):
    as_admin(api, AUTHOR)
    vid = create_question(api)
    api.post(f"/admin/questions/{vid}/submit")
    own_review = api.post(f"/admin/questions/{vid}/review", json={"decision": "approved"})
    assert (own_review.status_code, code(own_review)) == (403, "author_cannot_review")

    as_admin(api, REVIEWER)
    api.post(f"/admin/questions/{vid}/review", json={"decision": "approved"})
    as_admin(api, AUTHOR)
    own_publish = api.post(f"/admin/questions/{vid}/publish")
    assert (own_publish.status_code, code(own_publish)) == (403, "author_cannot_review")
    assert detail(api, vid)["status"] == "approved"


def test_publicar_exige_aprobacion_y_pedir_cambios_exige_un_comentario(api):
    as_admin(api, AUTHOR)
    vid = create_question(api)
    api.post(f"/admin/questions/{vid}/submit")

    as_admin(api, REVIEWER)
    assert api.post(f"/admin/questions/{vid}/publish").status_code == 409
    no_comment = api.post(f"/admin/questions/{vid}/review", json={"decision": "changes_requested"})
    assert (no_comment.status_code, code(no_comment)) == (400, "comment_required")
    api.post(
        f"/admin/questions/{vid}/review",
        json={"decision": "changes_requested", "comment": "Citar el artículo completo"},
    )
    reviewed = detail(api, vid)
    assert reviewed["status"] == "draft"  # vuelve a la autora
    assert reviewed["reviews"][0]["comment"] == "Citar el artículo completo"


def test_editar_crea_una_version_nueva_y_la_publicada_sigue_hasta_publicar_la_nueva(api, engine):
    as_admin(api, AUTHOR)
    v1 = create_question(api)
    publish(api, v1)

    # El revisor edita: la v2 es suya y queda en borrador; la v1 sigue publicada e intacta.
    v2 = api.post(f"/admin/questions/{v1}/edit", json=QUESTION | {"difficulty": 3}).json()["id"]
    assert (detail(api, v2)["number"], detail(api, v2)["status"]) == (2, "draft")
    assert detail(api, v1)["status"] == "published"
    assert detail(api, v1)["difficulty"] == QUESTION["difficulty"]

    # La autora original revisa y publica la v2 del revisor: la v1 se retira sola.
    api.post(f"/admin/questions/{v2}/submit")
    as_admin(api, AUTHOR)
    api.post(f"/admin/questions/{v2}/review", json={"decision": "approved"})
    api.post(f"/admin/questions/{v2}/publish")
    assert [(h["number"], h["status"]) for h in detail(api, v2)["history"]] == [
        (2, "published"),
        (1, "retired"),
    ]
    with Session(engine) as db:
        actions = list(db.scalars(select(ContentEventRow.action).order_by(ContentEventRow.id)))
    assert actions.count("published") == 2 and actions[-2:] == ["retired", "published"]


# ------------------------------------------------------------------------ retirar


def test_descartar_un_borrador_no_afecta_a_la_version_publicada(api):
    as_admin(api, AUTHOR)
    v1 = create_question(api)
    publish(api, v1)
    v2 = api.post(f"/admin/questions/{v1}/edit", json=QUESTION | {"difficulty": 1}).json()["id"]

    assert api.post(f"/admin/questions/{v2}/retire").status_code == 204
    assert detail(api, v1)["status"] == "published"
    again = api.post(f"/admin/questions/{v2}/retire")
    assert (again.status_code, code(again)) == (409, "invalid_transition")


def test_retirar_la_pregunta_retira_todas_sus_versiones_sin_borrarlas(api, engine):
    as_admin(api, AUTHOR)
    v1 = create_question(api)
    publish(api, v1)
    v2 = api.post(f"/admin/questions/{v1}/edit", json=QUESTION | {"difficulty": 1}).json()["id"]

    assert api.post(f"/admin/questions/{v2}/retire-question").status_code == 204
    assert [h["status"] for h in detail(api, v1)["history"]] == ["retired", "retired"]
    assert api.post(f"/admin/questions/{v1}/retire-question").status_code == 409
    with Session(engine) as db:
        assert len(db.scalars(select(QuestionVersionRow)).all()) == 2


# ------------------------------------------------------------------ buscar y en bloque


def test_buscar_por_texto_y_materia_con_paginacion(api):
    as_admin(api, AUTHOR)
    create_question(api)
    create_question(api, prompt="¿Qué es la competencia?", subtopic="La competencia")
    create_question(
        api, subject="Derecho Civil", subtopic="Personas", prompt="¿Cuándo principia la persona?"
    )

    def prompts(**params) -> list[str]:
        return [v["prompt"] for v in api.get("/admin/questions", params=params).json()]

    assert prompts(q="competencia") == ["¿Qué es la competencia?"]
    assert prompts(q="PERSONAS") == ["¿Cuándo principia la persona?"]  # también en el subtema
    assert sorted(prompts(subject="Derecho Procesal")) == [
        "¿Qué es la competencia?",
        "¿Qué es la jurisdicción?",
    ]
    first_page, second_page = prompts(limit=2), prompts(limit=2, offset=2)
    assert len(first_page) == 2 and len(second_page) == 1
    assert not set(first_page) & set(second_page)

    subjects = {s["name"]: s["subtopics"] for s in api.get("/admin/questions/subjects").json()}
    assert subjects == {
        "Derecho Civil": ["Personas"],
        "Derecho Procesal": ["La competencia", "La jurisdicción"],
    }


def test_las_acciones_en_bloque_aplican_las_reglas_de_cada_version(api):
    as_admin(api, AUTHOR)
    ids = [create_question(api, prompt=f"Pregunta {n}") for n in range(3)]
    submitted = api.post("/admin/questions/bulk", json={"action": "submit", "ids": ids}).json()
    assert submitted == {"done": 3, "skipped": []}

    # La autora no puede aprobar lo suyo: se salta cada una, con el motivo.
    own = api.post("/admin/questions/bulk", json={"action": "approve", "ids": ids}).json()
    assert own["done"] == 0 and len(own["skipped"]) == 3
    assert "otro administrador" in own["skipped"][0]["message"]

    as_admin(api, REVIEWER)
    for action in ("approve", "publish"):
        result = api.post("/admin/questions/bulk", json={"action": action, "ids": ids}).json()
        assert result == {"done": 3, "skipped": []}
    assert {detail(api, vid)["status"] for vid in ids} == {"published"}


def test_un_estudiante_no_puede_administrar_el_banco(api, outbox):
    verified_account(api, outbox)
    login(api)
    for method, path in (
        ("get", "/admin/questions"),
        ("post", "/admin/questions"),
        ("post", "/admin/questions/import"),
        ("get", "/admin/questions/export"),
        ("post", "/admin/questions/bulk"),
    ):
        assert getattr(api, method)(path).status_code == 403, path

"""Glosario y rosco legal (FR-038, AC-050): flujo de revisión con autor distinto del revisor,
solo términos publicados en el rosco, y la respuesta se revela al corregir."""

import pytest

from tests.api.bank import AUTHOR, REVIEWER, as_admin, student
from tests.test_glossary import xlsx

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]

TERMS = [
    ["Derecho Civil", "Tradición", "Modo de adquirir el dominio por entrega.", "CC, art. 670"],
    ["Derecho Civil", "Ocupación", "Modo de adquirir cosas sin dueño.", "CC, art. 606"],
    ["Derecho Procesal", "Jurisdicción", "Poder deber de resolver conflictos.", "COT, art. 1"],
]


def load(api) -> list[dict]:
    as_admin(api, AUTHOR)
    assert api.post("/admin/glossary/import", content=xlsx(TERMS)).json()["created"] == 3
    return api.get("/admin/glossary").json()


def bulk(api, action: str, ids: list[str]) -> dict:
    return api.post("/admin/glossary/bulk", json={"action": action, "ids": ids}).json()


def test_quien_carga_no_aprueba_ni_publica_y_solo_lo_publicado_llega_al_rosco(
    api, outbox, engine, clock
):
    rows = load(api)
    ids = [r["id"] for r in rows]
    assert {r["status"] for r in rows} == {"draft"} and all(r["mine"] for r in rows)
    own = bulk(api, "approve", ids)
    assert own["done"] == 0 and len(own["skipped"]) == 3

    as_admin(api, REVIEWER)
    assert bulk(api, "publish", ids)["done"] == 0  # hay que aprobar antes de publicar
    civil = [r["id"] for r in rows if r["subject"] == "Derecho Civil"]
    assert bulk(api, "approve", ids)["done"] == 3
    assert bulk(api, "publish", civil)["done"] == 2

    student(api, outbox, engine, clock)
    items = api.get("/practice/rosco").json()
    assert sorted((i["letter"], i["mode"]) for i in items) == [("O", "starts"), ("T", "starts")]
    assert all("term" not in i for i in items)  # la respuesta no viaja con la pregunta
    assert api.get("/practice/rosco", params={"subject": "Derecho Procesal"}).json() == []

    tradicion = next(i for i in items if i["letter"] == "T")
    right = api.post(
        "/practice/rosco/check", json={"id": tradicion["id"], "answer": "la tradicion"}
    )
    assert right.json() == {"correct": True, "term": "Tradición"}
    passed = api.post("/practice/rosco/check", json={"id": tradicion["id"], "answer": ""})
    assert passed.json() == {"correct": False, "term": "Tradición"}


def test_un_termino_no_le_quita_su_letra_a_otro_y_sobrantes_van_por_contiene(
    api, outbox, engine, clock
):
    as_admin(api, AUTHOR)
    rows = [
        ["Derecho Civil", "Tradición", "Modo de adquirir por entrega.", "CC, art. 670"],
        ["Derecho Civil", "Tradente", "Quien entrega en la tradición del dominio.", "CC"],
        ["Derecho Civil", "Acción", "Derecho que se ejerce ante tribunales.", "CC"],
    ]
    api.post("/admin/glossary/import", content=xlsx(rows))
    ids = [r["id"] for r in api.get("/admin/glossary").json()]
    as_admin(api, REVIEWER)
    bulk(api, "approve", ids)
    bulk(api, "publish", ids)
    student(api, outbox, engine, clock)

    for _ in range(5):  # el azar no cambia la regla
        items = {i["letter"]: i["mode"] for i in api.get("/practice/rosco").json()}
        assert items["A"] == "starts" and items["T"] == "starts"
        # El término de T que sobra se usa en otra letra que contiene.
        assert len(items) == 3 and list(items.values()).count("contains") == 1


def test_un_termino_vigente_no_se_puede_cargar_dos_veces(api, outbox, engine, clock):
    load(api)
    again = api.post("/admin/glossary/import", content=xlsx(TERMS[:1]))
    assert again.status_code == 409


def test_un_termino_retirado_sale_del_rosco(api, outbox, engine, clock):
    rows = load(api)
    ids = [r["id"] for r in rows]
    as_admin(api, REVIEWER)
    bulk(api, "approve", ids)
    bulk(api, "publish", ids)
    bulk(api, "retire", ids[:1])
    student(api, outbox, engine, clock)
    assert len(api.get("/practice/rosco").json()) == 2
    gone = api.post("/practice/rosco/check", json={"id": ids[0], "answer": "x"})
    assert gone.status_code == 404


def test_el_rosco_exige_acceso_y_el_glosario_es_solo_para_administradores(
    api, outbox, engine, clock
):
    student(api, outbox, engine, clock, with_access=False)
    assert api.get("/practice/rosco").status_code == 402
    assert api.get("/admin/glossary").status_code == 403

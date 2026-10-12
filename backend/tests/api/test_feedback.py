"""Comentarios de usuarios (FR-028, AC-037)."""

import pytest

from app.cli import create_admin
from tests.api.test_auth import EMAIL, code, login, verified_account

pytestmark = pytest.mark.integration

ADMIN_EMAIL = "admin@ejemplo.cl"
ADMIN_PASSWORD = "administra el banco 2026"


def send(api, **overrides):
    body = {
        "category": "suggestion",
        "message": "Me gustaría practicar por subtemas.",
        "page": "/panel",
    }
    body.update(overrides)
    return api.post("/feedback", json=body)


def as_admin(api, engine, monkeypatch):
    api.post("/auth/logout")
    monkeypatch.setenv("ADMIN_PASSWORD", ADMIN_PASSWORD)
    assert create_admin(ADMIN_EMAIL, engine=engine) == 0
    assert login(api, email=ADMIN_EMAIL, password=ADMIN_PASSWORD).status_code == 204


def test_estudiante_envia_y_el_administrador_lo_lee(api, outbox, engine, monkeypatch, clock):
    verified_account(api, outbox)
    login(api)
    assert send(api).status_code == 201
    assert send(api, category="problem", message="  No carga el panel.  ").status_code == 201

    as_admin(api, engine, monkeypatch)
    response = api.get("/feedback")
    assert response.status_code == 200
    items = response.json()
    assert sorted(item["category"] for item in items) == ["problem", "suggestion"]
    problem = next(item for item in items if item["category"] == "problem")
    assert problem["message"] == "No carga el panel."  # se recortan espacios
    assert problem["user_email"] == EMAIL
    assert problem["page"] == "/panel"


def test_sin_sesion_no_se_puede_enviar(api):
    response = send(api)
    assert response.status_code == 401
    assert code(response) == "not_authenticated"


def test_estudiante_no_puede_leer_comentarios(api, outbox):
    verified_account(api, outbox)
    login(api)
    response = api.get("/feedback")
    assert response.status_code == 403
    assert code(response) == "forbidden"


@pytest.mark.parametrize(
    "overrides",
    [
        {"message": "   "},
        {"message": "x" * 2001},
        {"category": "insulto"},
    ],
)
def test_comentarios_invalidos_se_rechazan(api, outbox, overrides):
    verified_account(api, outbox)
    login(api)
    assert send(api, **overrides).status_code == 422


def test_mensaje_de_2000_caracteres_se_acepta(api, outbox):
    verified_account(api, outbox)
    login(api)
    assert send(api, message="x" * 2000).status_code == 201


def test_pagina_externa_se_descarta(api, outbox, engine, monkeypatch):
    verified_account(api, outbox)
    login(api)
    send(api, page="https://otro-sitio.example/robar")
    as_admin(api, engine, monkeypatch)
    assert api.get("/feedback").json()[0]["page"] is None

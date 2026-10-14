"""Correo de ánimo tras días sin entrar (FR-034, AC-043)."""

import pytest
from sqlalchemy.orm import Session

from app.billing.grants import grant_access
from app.config import get_settings
from tests.api.test_auth import EMAIL, login, verified_account

pytestmark = pytest.mark.integration

DAY = 24 * 3600
SECRET = "clave-cron-de-prueba"
AUTH = {"Authorization": f"Bearer {SECRET}"}


@pytest.fixture
def cron(monkeypatch):
    monkeypatch.setenv("CRON_SECRET", SECRET)
    get_settings.cache_clear()


def reminders(outbox):
    return [m for m in outbox.to(EMAIL) if m.subject == "Apruvi te está esperando"]


def active_student(api, outbox, engine, clock):
    verified_account(api, outbox)
    with Session(engine) as db:
        grant_access(db, EMAIL, "Pruebas", "equipo@proda.cl", clock())
    login(api)
    api.post("/engagement/checkin")


def test_sin_clave_configurada_no_existe(api, monkeypatch):
    monkeypatch.setenv("CRON_SECRET", "")
    get_settings.cache_clear()
    assert api.get("/engagement/reminders/run", headers=AUTH).status_code == 404


def test_rechaza_una_clave_incorrecta(api, cron):
    response = api.get("/engagement/reminders/run", headers={"Authorization": "Bearer otra"})
    assert response.status_code == 401


def test_un_solo_correo_por_ausencia(api, outbox, engine, clock, cron):
    active_student(api, outbox, engine, clock)

    clock.advance(1 * DAY)
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 0}

    clock.advance(1 * DAY)  # dos días sin entrar
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 1}
    [message] = reminders(outbox)
    assert "/panel" in message.body
    assert "/correos/baja?token=" in message.body
    assert message.headers and "List-Unsubscribe" in message.headers
    assert "no garantizan la aprobación" in message.body

    clock.advance(1 * DAY)
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 0}

    # Vuelve a entrar y se ausenta de nuevo: corresponde otro correo.
    login(api)
    api.post("/engagement/checkin")
    clock.advance(2 * DAY)
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 1}
    assert len(reminders(outbox)) == 2


def test_quien_se_da_de_baja_no_recibe_mas(api, outbox, engine, clock, cron):
    active_student(api, outbox, engine, clock)
    clock.advance(2 * DAY)
    api.get("/engagement/reminders/run", headers=AUTH)
    token = reminders(outbox)[0].body.split("/correos/baja?token=")[1].split()[0]

    assert api.post("/engagement/reminders/unsubscribe", json={"token": token}).status_code == 204
    # El mismo enlace funciona dos veces (idempotente).
    assert api.post("/engagement/reminders/unsubscribe", json={"token": token}).status_code == 204

    login(api)
    api.post("/engagement/checkin")
    clock.advance(3 * DAY)
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 0}


def test_enlace_de_baja_invalido(api):
    response = api.post("/engagement/reminders/unsubscribe", json={"token": "no-existe"})
    assert response.status_code == 404


def test_sin_acceso_no_recibe_recordatorios(api, outbox, clock, cron):
    verified_account(api, outbox)
    login(api)
    api.post("/engagement/checkin")
    clock.advance(3 * DAY)
    assert api.get("/engagement/reminders/run", headers=AUTH).json() == {"sent": 0}

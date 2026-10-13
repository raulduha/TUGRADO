"""Registro diario y racha (FR-033, AC-042)."""

import pytest

from tests.api.test_auth import login, verified_account

pytestmark = pytest.mark.integration

DAY = 24 * 3600


def test_la_racha_sube_un_dia_a_la_vez_y_celebra_una_sola_vez(api, outbox, clock):
    verified_account(api, outbox)
    assert login(api).status_code == 204

    first = api.post("/engagement/checkin").json()
    assert first["current"] == 1 and first["new_today"] is True
    assert first["week"] == [False] * 6 + [True]

    # Volver el mismo día no repite la celebración ni suma.
    again = api.post("/engagement/checkin").json()
    assert again["current"] == 1 and again["new_today"] is False

    clock.advance(DAY)
    login(api)
    second = api.post("/engagement/checkin").json()
    assert second["current"] == 2 and second["new_today"] is True
    assert second["week"][-2:] == [True, True]

    # Dos días sin entrar: la racha vuelve a 1 y se conserva la mejor.
    clock.advance(3 * DAY)
    login(api)
    after_gap = api.post("/engagement/checkin").json()
    assert after_gap["current"] == 1 and after_gap["best"] == 2


def test_requiere_sesion(api):
    assert api.post("/engagement/checkin").status_code == 401

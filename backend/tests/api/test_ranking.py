"""Ranking mensual voluntario (FR-039, AC-051): solo inscritos, solo el apodo, XP del mes."""

from datetime import timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.persistence.auth_models import UserAccountRow
from app.persistence.content_models import PracticeAttemptRow
from tests.api.bank import AUTHOR, as_admin, create_question, publish, student
from tests.api.test_auth import EMAIL

pytestmark = [pytest.mark.integration, pytest.mark.usefixtures("admins")]


def correct_answers(engine, email: str, version_id: str, n: int, at) -> None:
    with Session(engine) as db:
        user = db.scalars(select(UserAccountRow).where(UserAccountRow.email == email)).one()
        for i in range(n):
            db.add(
                PracticeAttemptRow(
                    user_id=user.id,
                    version_id=version_id,
                    chosen_position=0,
                    correct=True,
                    answered_at=at + timedelta(seconds=i),
                )
            )
        db.commit()


def test_solo_aparecen_los_inscritos_con_su_apodo_y_la_xp_del_mes(api, outbox, engine, clock):
    as_admin(api, AUTHOR)
    version = create_question(api)
    publish(api, version)
    student(api, outbox, engine, clock)
    assert api.get("/engagement/ranking").json() == {"entries": [], "me": None, "alias": None}

    assert api.put("/engagement/ranking/profile", json={"alias": "Toga Feliz"}).status_code == 204
    correct_answers(engine, EMAIL, version, 3, clock())
    correct_answers(engine, EMAIL, version, 5, clock() - timedelta(days=40))  # otro mes

    result = api.get("/engagement/ranking").json()
    assert result["me"] == {"position": 1, "alias": "Toga Feliz", "xp": 30, "me": True}
    assert EMAIL not in str(result)  # nunca el correo

    assert api.put("/engagement/ranking/profile", json={"alias": "a@b"}).status_code == 400
    assert api.delete("/engagement/ranking/profile").status_code == 204
    assert api.get("/engagement/ranking").json()["entries"] == []


def test_dos_personas_no_pueden_usar_el_mismo_apodo(api, outbox, engine, clock):
    student(api, outbox, engine, clock)
    assert api.put("/engagement/ranking/profile", json={"alias": "Procurador"}).status_code == 204
    as_admin(api, AUTHOR)  # los administradores también tienen acceso al estudio
    taken = api.put("/engagement/ranking/profile", json={"alias": "procurador"})
    assert taken.status_code == 409

import pytest

from app.cli import create_admin
from tests.api.bank import ADMIN_PASSWORD, AUTHOR, REVIEWER


@pytest.fixture
def admins(engine, monkeypatch):
    """Dos administradores: la autora del contenido y el revisor que lo aprueba y publica."""
    monkeypatch.setenv("ADMIN_PASSWORD", ADMIN_PASSWORD)
    create_admin(AUTHOR, engine=engine)
    create_admin(REVIEWER, engine=engine)

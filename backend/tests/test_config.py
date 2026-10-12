import pytest
from pydantic import ValidationError

from app.config import Settings


def test_falla_si_falta_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValidationError, match="database_url"):
        Settings(_env_file=None)


def test_lee_database_url_del_entorno(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@localhost:5432/x")
    assert Settings(_env_file=None).database_url.endswith("/x")

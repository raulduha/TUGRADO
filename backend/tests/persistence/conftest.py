from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

BACKEND_DIR = Path(__file__).resolve().parents[2]


class _TestDatabase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIR.parent / ".env", BACKEND_DIR / ".env"), extra="ignore"
    )

    test_database_url: str


@pytest.fixture(scope="session")
def engine():
    url = make_url(_TestDatabase().test_database_url)
    # Crea la base de pruebas si no existe (conectándose a la base administrativa).
    admin = create_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    with admin.connect() as conn:
        exists = conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": url.database}
        )
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{url.database}"'))
    admin.dispose()

    config = Config(str(BACKEND_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    config.set_main_option("sqlalchemy.url", url.render_as_string(hide_password=False))
    command.upgrade(config, "head")

    engine = create_engine(url)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def _clean_tables(engine):
    yield
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE simulation_session CASCADE"))

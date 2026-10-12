from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from app.api.deps import get_clock, get_email_sender
from app.config import get_settings
from app.db import get_engine
from tests.fakes import FakeClock, Outbox

BACKEND_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def _clear_caches():
    get_settings.cache_clear()
    get_engine.cache_clear()
    yield
    get_settings.cache_clear()
    get_engine.cache_clear()


@pytest.fixture
def client() -> TestClient:
    from app.main import create_app

    return TestClient(create_app())


# ---------------------------------------------------- base de datos de integración


class _TestDatabase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BACKEND_DIR.parent / ".env", BACKEND_DIR / ".env"), extra="ignore"
    )

    test_database_url: str


@pytest.fixture(scope="session")
def migrated_engine():
    """Base `tugrado_test`: se crea si no existe y se migra a la última versión."""
    url = make_url(_TestDatabase().test_database_url)
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


@pytest.fixture
def engine(migrated_engine):
    """Motor de la base de pruebas; vacía las tablas al terminar cada prueba."""
    yield migrated_engine
    with migrated_engine.begin() as conn:
        conn.execute(text("TRUNCATE user_account, simulation_session, user_feedback CASCADE"))


# ------------------------------------------------------------------ API con base real


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def outbox() -> Outbox:
    return Outbox()


@pytest.fixture
def api(engine, clock, outbox) -> TestClient:
    """Cliente HTTP contra la base de pruebas, con reloj y correo controlados."""
    from app.main import create_app

    app = create_app()
    app.dependency_overrides[get_engine] = lambda: engine
    app.dependency_overrides[get_clock] = lambda: clock
    app.dependency_overrides[get_email_sender] = lambda: outbox
    # El origen del frontend: así lo enviaría un navegador desde la app.
    return TestClient(app, headers={"Origin": get_settings().frontend_origin})

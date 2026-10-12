import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.db import get_engine


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

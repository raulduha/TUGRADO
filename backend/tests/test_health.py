import pytest
from sqlalchemy import create_engine

from app.db import get_engine


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_db_no_disponible_devuelve_503(client):
    # Puerto 1: nada escucha ahí, la conexión falla de inmediato.
    engine = create_engine("postgresql+psycopg://u:p@127.0.0.1:1/x?connect_timeout=2")
    client.app.dependency_overrides[get_engine] = lambda: engine
    response = client.get("/health/db")
    assert response.status_code == 503
    assert response.json() == {"detail": "Base de datos no disponible"}


@pytest.mark.integration
def test_health_db_con_postgres(client):
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

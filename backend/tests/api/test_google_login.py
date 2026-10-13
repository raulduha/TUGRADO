"""Ingreso con Google de punta a punta, con Google simulado (FR-001b, AC-040)."""

from urllib.parse import parse_qs, urlsplit

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_clock, get_email_sender, get_google_provider
from app.auth.google import GoogleAuthError, GoogleIdentity
from app.config import get_settings
from app.db import get_engine
from app.persistence.auth_models import UserAccountRow, UserIdentityRow
from tests.api.test_auth import EMAIL, login, verified_account

pytestmark = pytest.mark.integration


class FakeGoogle:
    """Simula a Google: autoriza cualquier código y devuelve la identidad configurada."""

    def __init__(self) -> None:
        self.identity = GoogleIdentity(subject="google-1", email=EMAIL, email_verified=True)
        self.fail = False
        self.seen_nonce: str | None = None

    def authorize_url(self, state, nonce, code_challenge, redirect_uri):
        return f"https://google.example/auth?state={state}&redirect_uri={redirect_uri}"

    def identify(self, code, code_verifier, redirect_uri, nonce):
        self.seen_nonce = nonce
        if self.fail:
            raise GoogleAuthError("código inválido")
        return self.identity


@pytest.fixture
def google():
    return FakeGoogle()


@pytest.fixture
def gapi(engine, clock, outbox, google, monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import create_app

    monkeypatch.setenv("GOOGLE_CLIENT_ID", "cliente.apps.googleusercontent.com")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "secreto")
    monkeypatch.setenv("OAUTH_STATE_SECRET", "clave-para-firmar-el-estado")
    get_settings.cache_clear()
    app = create_app()
    app.dependency_overrides[get_engine] = lambda: engine
    app.dependency_overrides[get_clock] = lambda: clock
    app.dependency_overrides[get_email_sender] = lambda: outbox
    app.dependency_overrides[get_google_provider] = lambda: google
    return TestClient(app, follow_redirects=False)


def start(gapi, next_path="/panel") -> str:
    response = gapi.get(f"/auth/google/start?next={next_path}")
    assert response.status_code == 302
    assert "tugrado_google" in response.cookies
    return parse_qs(urlsplit(response.headers["location"]).query)["state"][0]


def callback(gapi, state, code="codigo"):
    return gapi.get(f"/auth/google/callback?code={code}&state={state}")


def users(engine):
    with Session(engine) as db:
        return list(db.scalars(select(UserAccountRow)))


def test_proveedores_con_google_activado(gapi):
    assert gapi.get("/auth/providers").json() == {"google": True}


def test_sin_credenciales_google_queda_desactivado(api):
    # Configuración de .env: sin GOOGLE_CLIENT_ID.
    assert api.get("/auth/providers").json() == {"google": False}
    assert api.get("/auth/google/start").status_code == 404


def test_primer_ingreso_crea_cuenta_verificada_de_estudiante(gapi, engine, google):
    state = start(gapi)
    response = callback(gapi, state)
    assert response.status_code == 302
    assert response.headers["location"] == "http://localhost:3000/panel"
    assert "tugrado_session" in response.cookies
    assert google.seen_nonce  # el nonce guardado viaja a la validación del id_token

    gapi.cookies.set("tugrado_session", response.cookies["tugrado_session"])
    me = gapi.get("/auth/me").json()
    assert me["email"] == EMAIL
    assert me["roles"] == ["student"]
    [user] = users(engine)
    assert user.email_verified_at is not None
    assert user.password_hash is None


def test_correo_existente_se_vincula_a_la_misma_cuenta(gapi, api, outbox, engine):
    verified_account(api, outbox)
    original = users(engine)[0].id
    response = callback(gapi, start(gapi))
    assert response.status_code == 302
    assert "tugrado_session" in response.cookies
    assert [u.id for u in users(engine)] == [original]
    # La contraseña sigue funcionando.
    assert login(api).status_code == 204


def test_segundo_ingreso_usa_el_vinculo_aunque_cambie_el_correo(gapi, engine, google):
    callback(gapi, start(gapi))
    google.identity = GoogleIdentity(
        subject="google-1", email="nuevo@gmail.com", email_verified=True
    )
    gapi.cookies.clear()
    callback(gapi, start(gapi))
    assert len(users(engine)) == 1
    with Session(engine) as db:
        assert len(db.scalars(select(UserIdentityRow)).all()) == 1


def test_cuenta_creada_con_google_no_entra_con_contrasena(gapi, api):
    callback(gapi, start(gapi))
    assert login(api, password="cualquier clave larga").status_code == 401


@pytest.mark.parametrize("bad_state", ["otro-state", ""])
def test_state_que_no_coincide_se_rechaza(gapi, engine, bad_state):
    start(gapi)
    response = callback(gapi, bad_state)
    assert response.headers["location"] == "http://localhost:3000/iniciar-sesion?error=google"
    assert "tugrado_session" not in response.cookies
    assert users(engine) == []


def test_sin_la_cookie_de_estado_se_rechaza(gapi, engine):
    state = start(gapi)
    gapi.cookies.clear()
    assert callback(gapi, state).headers["location"].endswith("?error=google")
    assert users(engine) == []


def test_cookie_de_estado_vencida_se_rechaza(gapi, engine, clock):
    state = start(gapi)
    clock.advance(10 * 60)
    assert callback(gapi, state).headers["location"].endswith("?error=google")
    assert users(engine) == []


def test_correo_no_verificado_por_google_se_rechaza(gapi, engine, google):
    google.identity = GoogleIdentity(subject="google-2", email=EMAIL, email_verified=False)
    assert callback(gapi, start(gapi)).headers["location"].endswith("?error=google")
    assert users(engine) == []


def test_codigo_invalido_se_rechaza(gapi, engine, google):
    google.fail = True
    assert callback(gapi, start(gapi)).headers["location"].endswith("?error=google")
    assert users(engine) == []


def test_next_externo_no_redirige_fuera_del_sitio(gapi):
    state = start(gapi, next_path="https://malicioso.example")
    assert callback(gapi, state).headers["location"] == "http://localhost:3000/panel"

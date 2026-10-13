"""Cliente de Google y cookie firmada (FR-001b, AC-040). Sin red: Google se simula."""

import json
import time
from datetime import UTC, datetime, timedelta

import httpx
import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.auth.google import (
    JWKS_URL,
    TOKEN_URL,
    GoogleAuthError,
    GoogleOAuth,
    pkce_challenge,
)
from app.auth.signed import InvalidSignedValue, sign, unsign

CLIENT_ID = "cliente-de-prueba.apps.googleusercontent.com"
NOW = datetime(2026, 10, 13, 12, 0, tzinfo=UTC)


def test_pkce_vector_oficial_rfc7636():
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    assert pkce_challenge(verifier) == "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"


# ------------------------------------------------------------------ cookie firmada


def test_cookie_firmada_ida_y_vuelta():
    value = sign({"state": "abc"}, "secreto", NOW + timedelta(minutes=10))
    assert unsign(value, "secreto", NOW)["state"] == "abc"


@pytest.mark.parametrize(
    ("mutate", "now"),
    [
        (lambda v: v[:-1] + ("0" if v[-1] != "0" else "1"), NOW),  # firma alterada
        (lambda v: v, NOW + timedelta(minutes=10)),  # vencida
        (lambda v: "basura", NOW),
        (lambda v: None, NOW),
    ],
)
def test_cookie_alterada_o_vencida_se_rechaza(mutate, now):
    value = sign({"state": "abc"}, "secreto", NOW + timedelta(minutes=10))
    with pytest.raises(InvalidSignedValue):
        unsign(mutate(value), "secreto", now)


def test_cookie_con_otra_clave_se_rechaza():
    value = sign({"state": "abc"}, "secreto", NOW + timedelta(minutes=10))
    with pytest.raises(InvalidSignedValue):
        unsign(value, "otra-clave", NOW)


# ------------------------------------------------------------------ id_token de Google


@pytest.fixture(scope="module")
def google_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def jwks_for(key, kid="clave-1") -> dict:
    public = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
    return {"keys": [{**public, "kid": kid, "alg": "RS256", "use": "sig"}]}


def id_token(key, kid="clave-1", **overrides) -> str:
    now = int(time.time())
    claims = {
        "iss": "https://accounts.google.com",
        "aud": CLIENT_ID,
        "sub": "1234567890",
        "email": "Estudiante@Gmail.com",
        "email_verified": True,
        "nonce": "nonce-1",
        "iat": now,
        "exp": now + 600,
    }
    claims.update(overrides)
    return jwt.encode(claims, key, algorithm="RS256", headers={"kid": kid})


def google_with(token: str | None, jwks: dict, token_status: int = 200) -> GoogleOAuth:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url) == TOKEN_URL:
            body = {"id_token": token} if token else {}
            return httpx.Response(token_status, json=body)
        if str(request.url) == JWKS_URL:
            return httpx.Response(200, json=jwks)
        return httpx.Response(404)

    return GoogleOAuth(CLIENT_ID, "secreto", httpx.Client(transport=httpx.MockTransport(handler)))


def identify(google: GoogleOAuth):
    return google.identify("codigo", "verificador", "https://x/callback", "nonce-1")


def test_id_token_valido(google_key):
    identity = identify(google_with(id_token(google_key), jwks_for(google_key)))
    assert identity.subject == "1234567890"
    assert identity.email == "Estudiante@Gmail.com"
    assert identity.email_verified is True


@pytest.mark.parametrize(
    "overrides",
    [
        {"aud": "otra-aplicacion"},
        {"iss": "https://malicioso.example"},
        {"nonce": "otro-nonce"},
        {"exp": int(time.time()) - 10},
    ],
)
def test_id_token_invalido_se_rechaza(google_key, overrides):
    google = google_with(id_token(google_key, **overrides), jwks_for(google_key))
    with pytest.raises(GoogleAuthError):
        identify(google)


def test_id_token_firmado_con_otra_clave_se_rechaza(google_key):
    attacker = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with pytest.raises(GoogleAuthError):
        identify(google_with(id_token(attacker), jwks_for(google_key)))


def test_codigo_rechazado_por_google(google_key):
    with pytest.raises(GoogleAuthError):
        identify(google_with(None, jwks_for(google_key), token_status=400))


def test_url_de_autorizacion_incluye_pkce_state_y_nonce():
    url = GoogleOAuth(CLIENT_ID, "s").authorize_url("st", "no", "ch", "https://x/callback")
    query = httpx.URL(url).params
    assert query["state"] == "st"
    assert query["nonce"] == "no"
    assert query["code_challenge"] == "ch"
    assert query["code_challenge_method"] == "S256"
    assert query["scope"] == "openid email"

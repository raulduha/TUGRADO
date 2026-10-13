"""Ingreso con Google (OpenID Connect, código de autorización con PKCE) — FR-001b, AC-040."""

from __future__ import annotations

import base64
import hashlib
import secrets
from dataclasses import dataclass
from typing import Protocol
from urllib.parse import urlencode

import httpx
import jwt

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
JWKS_URL = "https://www.googleapis.com/oauth2/v3/certs"
ISSUERS = ("https://accounts.google.com", "accounts.google.com")


class GoogleAuthError(Exception):
    """La respuesta de Google no es válida. El mensaje no incluye tokens."""


@dataclass(frozen=True)
class GoogleIdentity:
    subject: str
    email: str
    email_verified: bool


def pkce_challenge(verifier: str) -> str:
    """Desafío PKCE S256 (RFC 7636 §4.2)."""
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def new_pkce_pair() -> tuple[str, str]:
    """Devuelve (verifier, challenge S256)."""
    verifier = secrets.token_urlsafe(48)
    return verifier, pkce_challenge(verifier)


class GoogleProvider(Protocol):
    def authorize_url(
        self, state: str, nonce: str, code_challenge: str, redirect_uri: str
    ) -> str: ...

    def identify(
        self, code: str, code_verifier: str, redirect_uri: str, nonce: str
    ) -> GoogleIdentity: ...


class GoogleOAuth:
    def __init__(
        self, client_id: str, client_secret: str, client: httpx.Client | None = None
    ) -> None:
        self.client_id = client_id
        self._secret = client_secret
        self._http = client or httpx.Client(timeout=10)

    def authorize_url(self, state: str, nonce: str, code_challenge: str, redirect_uri: str) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email",
            "state": state,
            "nonce": nonce,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "prompt": "select_account",
        }
        return f"{AUTHORIZE_URL}?{urlencode(params)}"

    def identify(
        self, code: str, code_verifier: str, redirect_uri: str, nonce: str
    ) -> GoogleIdentity:
        try:
            response = self._http.post(
                TOKEN_URL,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self._secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code",
                    "code_verifier": code_verifier,
                },
            )
        except httpx.HTTPError as exc:
            raise GoogleAuthError(f"Google no respondió: {type(exc).__name__}") from exc
        if response.status_code != 200:
            raise GoogleAuthError(f"Google rechazó el código ({response.status_code})")
        id_token = response.json().get("id_token")
        if not id_token:
            raise GoogleAuthError("La respuesta de Google no trae id_token")
        claims = self._verify(id_token)
        if claims.get("nonce") != nonce:
            raise GoogleAuthError("El nonce no coincide")
        email = claims.get("email")
        if not email:
            raise GoogleAuthError("Google no entregó el correo")
        return GoogleIdentity(
            subject=str(claims["sub"]),
            email=str(email),
            email_verified=claims.get("email_verified") is True,
        )

    def _verify(self, id_token: str) -> dict:
        """Valida firma (claves públicas de Google), emisor, audiencia y vencimiento."""
        try:
            keys = jwt.PyJWKSet.from_dict(self._http.get(JWKS_URL).raise_for_status().json())
            kid = jwt.get_unverified_header(id_token).get("kid")
            key = next(k for k in keys.keys if k.key_id == kid)
            return jwt.decode(
                id_token,
                key=key.key,
                algorithms=["RS256"],
                audience=self.client_id,
                issuer=list(ISSUERS),
                options={"require": ["exp", "iat", "iss", "aud", "sub"]},
            )
        except (httpx.HTTPError, StopIteration, jwt.PyJWTError, ValueError) as exc:
            raise GoogleAuthError(f"id_token inválido: {type(exc).__name__}") from exc

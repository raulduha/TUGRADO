"""Reglas de cuentas y sesiones (FR-001, AC-032, AC-036).

Cada método confirma su propia transacción, porque algunos deben guardar cambios aunque la
operación termine en error (por ejemplo, un intento fallido que cuenta para el bloqueo).
Las respuestas no revelan si un correo está registrado, salvo el aviso de bloqueo temporal.
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.auth.email import EmailDeliveryError, EmailMessage, EmailSender
from app.auth.passwords import hash_password, needs_rehash, validate_password, verify_password
from app.auth.policy import AuthPolicy
from app.auth.tokens import hash_token, new_token
from app.errors import AppError
from app.persistence.auth_models import (
    AuthSessionRow,
    EmailTokenPurpose,
    EmailTokenRow,
    Role,
    UserAccountRow,
    UserRoleRow,
)

logger = logging.getLogger("tugrado.auth")

# Escribir last_used_at en cada solicitud es innecesario: basta con esta resolución.
_SESSION_TOUCH_RESOLUTION_SECONDS = 60


class AuthError(AppError):
    pass


@dataclass(frozen=True)
class AuthenticatedUser:
    id: uuid.UUID
    email: str
    roles: frozenset[Role]
    session_id: uuid.UUID


def normalize_email(email: str) -> str:
    return email.strip().lower()


class AuthService:
    def __init__(
        self,
        db: Session,
        policy: AuthPolicy,
        clock: Callable[[], datetime],
        email_sender: EmailSender,
        frontend_base_url: str,
    ) -> None:
        self.db = db
        self.policy = policy
        self.clock = clock
        self.email_sender = email_sender
        self.frontend_base_url = frontend_base_url.rstrip("/")

    # ------------------------------------------------------------------ registro

    def register(self, email: str, password: str) -> None:
        validate_password(password, self.policy)
        email = normalize_email(email)
        existing = self._user_by_email(email)
        if existing is not None:
            # Misma respuesta que un registro nuevo; el aviso llega solo al dueño del correo.
            self._send(
                email,
                "Ya tienes una cuenta en Aprueba tu examen",
                "Alguien intentó registrarse con este correo, que ya tiene una cuenta. "
                "Si fuiste tú, inicia sesión o recupera tu contraseña. Si no, ignora este correo.",
            )
            return
        user = UserAccountRow(email=email, password_hash=hash_password(password))
        user.roles.append(UserRoleRow(role=Role.STUDENT))
        self.db.add(user)
        self.db.flush()
        message = self._verification_message(user)
        self.db.commit()
        self._deliver(message)

    def create_administrator(self, email: str, password: str | None) -> tuple[uuid.UUID, bool]:
        """Crea un administrador verificado o promueve una cuenta existente (uso por consola).

        Devuelve el id y si la cuenta se creó (True) o ya existía (False).
        """
        email = normalize_email(email)
        user = self._user_by_email(email)
        created = user is None
        if user is None:
            if password is None:
                raise AuthError("password_required", "Se requiere contraseña para crear la cuenta")
            validate_password(password, self.policy)
            user = UserAccountRow(
                email=email,
                password_hash=hash_password(password),
                email_verified_at=self.clock(),
            )
            self.db.add(user)
        if Role.ADMINISTRATOR not in user.role_set:
            user.roles.append(UserRoleRow(role=Role.ADMINISTRATOR))
        self.db.commit()
        return user.id, created

    # ------------------------------------------------------- verificación de correo

    def verify_email(self, token: str) -> None:
        row = self._consume_token(token, EmailTokenPurpose.VERIFY_EMAIL)
        user = self.db.get(UserAccountRow, row.user_id)
        assert user is not None
        if user.email_verified_at is None:
            user.email_verified_at = self.clock()
        self.db.commit()

    def resend_verification(self, email: str) -> None:
        user = self._user_by_email(normalize_email(email))
        if user is not None and user.email_verified_at is None:
            message = self._verification_message(user)
            self.db.commit()
            self._deliver(message)

    # ------------------------------------------------------------ inicio de sesión

    def login(self, email: str, password: str) -> str:
        """Devuelve el token de sesión para la cookie."""
        now = self.clock()
        user = self.db.scalars(
            select(UserAccountRow)
            .where(UserAccountRow.email == normalize_email(email))
            .with_for_update()  # serializa los intentos concurrentes sobre la misma cuenta
        ).one_or_none()
        if user is None:
            verify_password(None, password)  # mismo costo que con una cuenta real
            raise _invalid_credentials()
        if user.locked_until is not None and now < user.locked_until:
            raise AuthError(
                "account_locked",
                "Demasiados intentos fallidos. Intenta de nuevo en unos minutos.",
            )
        if not verify_password(user.password_hash, password):
            self._record_failure(user, now)
            self.db.commit()
            raise _invalid_credentials()

        user.failed_login_count = 0
        user.first_failed_login_at = None
        user.locked_until = None
        if needs_rehash(user.password_hash):
            user.password_hash = hash_password(password)
        if user.email_verified_at is None:
            self.db.commit()
            raise AuthError(
                "email_not_verified", "Debes verificar tu correo antes de usar la cuenta"
            )
        token = new_token()
        self.db.add(
            AuthSessionRow(
                user_id=user.id,
                token_hash=hash_token(token),
                created_at=now,
                last_used_at=now,
                expires_at=now + self.policy.session_max_age,
            )
        )
        self.db.commit()
        return token

    def _record_failure(self, user: UserAccountRow, now: datetime) -> None:
        window_start = user.first_failed_login_at
        if window_start is None or now - window_start >= self.policy.login_failure_window:
            user.failed_login_count = 0
            user.first_failed_login_at = now
        user.failed_login_count += 1
        if user.failed_login_count >= self.policy.login_max_failures:
            user.locked_until = now + self.policy.login_lockout
            user.failed_login_count = 0
            user.first_failed_login_at = None

    def authenticate(self, token: str) -> AuthenticatedUser | None:
        """Valida el token de la cookie y renueva la inactividad. None si no es válido."""
        now = self.clock()
        row = self.db.scalars(
            select(AuthSessionRow).where(AuthSessionRow.token_hash == hash_token(token))
        ).one_or_none()
        if row is None or row.revoked_at is not None or now >= row.expires_at:
            return None
        if now - row.last_used_at >= self.policy.session_idle_timeout:
            return None
        user = self.db.get(UserAccountRow, row.user_id)
        if user is None or user.email_verified_at is None:
            return None
        if (now - row.last_used_at).total_seconds() >= _SESSION_TOUCH_RESOLUTION_SECONDS:
            row.last_used_at = now
            self.db.commit()
        return AuthenticatedUser(
            id=user.id, email=user.email, roles=frozenset(user.role_set), session_id=row.id
        )

    def logout(self, token: str) -> None:
        self.db.execute(
            update(AuthSessionRow)
            .where(AuthSessionRow.token_hash == hash_token(token))
            .where(AuthSessionRow.revoked_at.is_(None))
            .values(revoked_at=self.clock())
        )
        self.db.commit()

    # ---------------------------------------------------- recuperación de contraseña

    def request_password_reset(self, email: str) -> None:
        user = self._user_by_email(normalize_email(email))
        if user is None:
            return
        token = self._issue_token(
            user, EmailTokenPurpose.RESET_PASSWORD, self.policy.password_reset_ttl
        )
        minutes = int(self.policy.password_reset_ttl.total_seconds() // 60)
        message = EmailMessage(
            to=user.email,
            subject="Recupera tu contraseña de Aprueba tu examen",
            body=(
                f"Para elegir una nueva contraseña abre este enlace (válido por {minutes} minutos "
                f"y una sola vez):\n{self.frontend_base_url}/restablecer-contrasena?token={token}"
                "\n\nSi no lo pediste, ignora este correo."
            ),
        )
        # El correo sale después del commit: nunca se envía un enlace que no quedó guardado.
        self.db.commit()
        self._deliver(message)

    def reset_password(self, token: str, new_password: str) -> None:
        validate_password(new_password, self.policy)
        row = self._consume_token(token, EmailTokenPurpose.RESET_PASSWORD)
        user = self.db.get(UserAccountRow, row.user_id)
        assert user is not None
        now = self.clock()
        user.password_hash = hash_password(new_password)
        user.failed_login_count = 0
        user.first_failed_login_at = None
        user.locked_until = None
        # El enlace llegó al correo: también prueba que el correo es del usuario.
        if user.email_verified_at is None:
            user.email_verified_at = now
        # Cambiar la contraseña cierra todas las sesiones abiertas.
        self.db.execute(
            update(AuthSessionRow)
            .where(AuthSessionRow.user_id == user.id)
            .where(AuthSessionRow.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        self.db.commit()

    # ------------------------------------------------------------------ internos

    def _user_by_email(self, email: str) -> UserAccountRow | None:
        return self.db.scalars(
            select(UserAccountRow).where(UserAccountRow.email == email)
        ).one_or_none()

    def _verification_message(self, user: UserAccountRow) -> EmailMessage:
        """Emite el token y arma el correo; quien llama lo envía después del commit."""
        token = self._issue_token(
            user, EmailTokenPurpose.VERIFY_EMAIL, self.policy.email_verification_ttl
        )
        hours = int(self.policy.email_verification_ttl.total_seconds() // 3600)
        return EmailMessage(
            to=user.email,
            subject="Verifica tu correo en Aprueba tu examen",
            body=(
                f"Para activar tu cuenta abre este enlace (válido por {hours} horas y una sola "
                f"vez):\n{self.frontend_base_url}/verificar-correo?token={token}"
            ),
        )

    def _issue_token(self, user: UserAccountRow, purpose: EmailTokenPurpose, ttl: timedelta) -> str:
        now = self.clock()
        # Un enlace nuevo invalida los anteriores del mismo tipo.
        self.db.execute(
            update(EmailTokenRow)
            .where(EmailTokenRow.user_id == user.id)
            .where(EmailTokenRow.purpose == purpose)
            .where(EmailTokenRow.used_at.is_(None))
            .values(used_at=now)
        )
        token = new_token()
        self.db.add(
            EmailTokenRow(
                user_id=user.id,
                purpose=purpose,
                token_hash=hash_token(token),
                created_at=now,
                expires_at=now + ttl,
            )
        )
        return token

    def _consume_token(self, token: str, purpose: EmailTokenPurpose) -> EmailTokenRow:
        now = self.clock()
        row = self.db.scalars(
            select(EmailTokenRow)
            .where(EmailTokenRow.token_hash == hash_token(token))
            .where(EmailTokenRow.purpose == purpose)
            .with_for_update()  # dos usos simultáneos del mismo enlace: solo uno gana
        ).one_or_none()
        if row is None or row.used_at is not None or now >= row.expires_at:
            raise AuthError("invalid_token", "El enlace no es válido o ya caducó")
        row.used_at = now
        return row

    def _send(self, to: str, subject: str, body: str) -> None:
        self._deliver(EmailMessage(to=to, subject=subject, body=body))

    def _deliver(self, message: EmailMessage) -> None:
        # Un fallo del proveedor no interrumpe la operación ni revela si la cuenta existe:
        # se registra (sin destinatario) y el estudiante puede pedir el reenvío del enlace.
        try:
            self.email_sender.send(message)
        except EmailDeliveryError as exc:
            logger.error("No se pudo enviar el correo «%s»: %s", message.subject, exc)


def _invalid_credentials() -> AuthError:
    return AuthError("invalid_credentials", "Correo o contraseña incorrectos")

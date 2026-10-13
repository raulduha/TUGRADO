"""Accesos de cortesía (FR-032): cuentas que el equipo autoriza a estudiar sin suscripción,
por ejemplo para pruebas. Se otorgan y revocan desde el CLI; nunca se borran."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.service import normalize_email
from app.errors import AppError
from app.persistence.auth_models import UserAccountRow
from app.persistence.billing_models import AccessGrantRow


class GrantError(AppError):
    pass


def _user(db: Session, email: str) -> UserAccountRow:
    query = select(UserAccountRow).where(UserAccountRow.email == normalize_email(email))
    user = db.scalars(query.with_for_update()).first()
    if user is None:
        raise GrantError("user_not_found", "No existe una cuenta con ese correo")
    return user


def _active(db: Session, user: UserAccountRow) -> AccessGrantRow | None:
    return db.scalars(
        select(AccessGrantRow).where(
            AccessGrantRow.user_id == user.id, AccessGrantRow.revoked_at.is_(None)
        )
    ).first()


def grant_access(db: Session, email: str, reason: str, granted_by: str, now: datetime) -> bool:
    """Otorga el acceso. Devuelve False si la cuenta ya tenía uno vigente."""
    if not reason.strip() or not granted_by.strip():
        raise GrantError("missing_reason", "Indica el motivo y quién otorga el acceso")
    user = _user(db, email)
    if _active(db, user) is not None:
        db.commit()
        return False
    db.add(
        AccessGrantRow(
            user_id=user.id, reason=reason.strip(), granted_by=granted_by.strip(), granted_at=now
        )
    )
    db.commit()
    return True


def revoke_access(db: Session, email: str, now: datetime) -> bool:
    """Revoca el acceso vigente. Devuelve False si la cuenta no tenía uno."""
    user = _user(db, email)
    grant = _active(db, user)
    if grant is None:
        db.commit()
        return False
    grant.revoked_at = now
    db.commit()
    return True

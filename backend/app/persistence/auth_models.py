"""Tablas de cuentas, roles, sesiones de usuario y tokens de correo (FR-001, FR-002, AC-036)."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.base import Base, enum_check, enum_column


class Role(StrEnum):
    STUDENT = "student"
    ADMINISTRATOR = "administrator"


class EmailTokenPurpose(StrEnum):
    VERIFY_EMAIL = "verify_email"
    RESET_PASSWORD = "reset_password"


class UserAccountRow(Base):
    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # Se guarda normalizado (minúsculas, sin espacios) para que la unicidad no dependa del caso.
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    email_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Bloqueo temporal por intentos fallidos.
    failed_login_count: Mapped[int] = mapped_column(Integer, default=0)
    first_failed_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    roles: Mapped[list["UserRoleRow"]] = relationship(cascade="all, delete-orphan", lazy="selectin")

    __table_args__ = (
        CheckConstraint("email = lower(email)", name="email_normalized"),
        CheckConstraint("failed_login_count >= 0", name="failed_login_count_non_negative"),
    )

    @property
    def role_set(self) -> set[Role]:
        return {r.role for r in self.roles}


class UserRoleRow(Base):
    __tablename__ = "user_role"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), primary_key=True
    )
    role: Mapped[Role] = mapped_column(enum_column(Role), primary_key=True)

    __table_args__ = (enum_check("role", Role, "role_valid"),)


class AuthSessionRow(Base):
    """Sesión iniciada. El token vive solo en la cookie; aquí se guarda su hash."""

    __tablename__ = "auth_session"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_used_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # Caducidad absoluta; la de inactividad se calcula con last_used_at.
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class EmailTokenRow(Base):
    """Enlace de un solo uso (verificación de correo o recuperación de contraseña)."""

    __tablename__ = "email_token"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )
    purpose: Mapped[EmailTokenPurpose] = mapped_column(enum_column(EmailTokenPurpose))
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (enum_check("purpose", EmailTokenPurpose, "purpose_valid"),)

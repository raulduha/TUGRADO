"""Suscripciones, su registro de cambios y accesos de cortesía (FR-029 a FR-032). Sin datos de
tarjeta."""

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.persistence.base import Base, enum_check, enum_column


class SubscriptionStatus(StrEnum):
    # Estados de una suscripción (preapproval) en Mercado Pago.
    PENDING = "pending"
    AUTHORIZED = "authorized"
    PAUSED = "paused"
    CANCELLED = "cancelled"


# Estados en los que la suscripción sigue viva: a lo más una por estudiante.
OPEN_STATUSES = (
    SubscriptionStatus.PENDING,
    SubscriptionStatus.AUTHORIZED,
    SubscriptionStatus.PAUSED,
)


class SubscriptionRow(Base):
    __tablename__ = "subscription"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="RESTRICT"), index=True
    )
    provider: Mapped[str] = mapped_column(String(20))
    provider_subscription_id: Mapped[str | None] = mapped_column(String(100), unique=True)
    status: Mapped[SubscriptionStatus] = mapped_column(enum_column(SubscriptionStatus))
    amount_clp: Mapped[int] = mapped_column(Integer)
    trial_days: Mapped[int] = mapped_column(Integer)
    init_point: Mapped[str | None] = mapped_column(String(500))
    # Correo de la cuenta de Mercado Pago que paga; puede diferir del correo de la app.
    payer_email: Mapped[str | None] = mapped_column(String(320))
    next_payment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        enum_check("status", SubscriptionStatus, "status_valid"),
        # Garantía en la base: un estudiante no puede tener dos suscripciones abiertas.
        Index(
            "uq_subscription_one_open_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("status IN ('pending', 'authorized', 'paused')"),
        ),
    )


class BillingEventRow(Base):
    """Registro de solo adición de los cambios de estado de una suscripción."""

    __tablename__ = "billing_event"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("subscription.id", ondelete="RESTRICT"), index=True
    )
    # created | webhook | return | cancel | sync
    source: Mapped[str] = mapped_column(String(20))
    previous_status: Mapped[str | None] = mapped_column(String(20))
    new_status: Mapped[str] = mapped_column(String(20))
    at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AccessGrantRow(Base):
    """Acceso de cortesía sin suscripción (FR-032), otorgado por el equipo desde el CLI.

    Revocar no borra la fila: se registra `revoked_at`, así queda el historial."""

    __tablename__ = "access_grant"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_account.id", ondelete="CASCADE"), index=True
    )
    reason: Mapped[str] = mapped_column(String(200))
    granted_by: Mapped[str] = mapped_column(String(320))
    granted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        # A lo más un acceso vigente por cuenta.
        Index(
            "uq_access_grant_one_active_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("revoked_at IS NULL"),
        ),
    )

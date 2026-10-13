"""Reglas de la suscripción (FR-029 a FR-031, AC-038, AC-039, Gate 11b).

El estado local solo cambia con datos obtenidos de la API del proveedor; nunca con el
contenido de una notificación ni con parámetros de la URL de retorno.
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.billing.gateway import NewSubscription, ProviderError, SubscriptionGateway
from app.errors import AppError
from app.persistence.auth_models import Role, UserAccountRow
from app.persistence.billing_models import (
    OPEN_STATUSES,
    BillingEventRow,
    SubscriptionRow,
    SubscriptionStatus,
)

SUBSCRIPTION_REASON = "Aprueba tu examen - Suscripción mensual"


class BillingError(AppError):
    pass


@dataclass(frozen=True)
class BillingPlan:
    amount_clp: int
    trial_days: int


@dataclass(frozen=True)
class SubscriptionView:
    status: SubscriptionStatus | None
    has_access: bool
    amount_clp: int
    trial_days: int
    next_payment_date: datetime | None
    checkout_url: str | None


class BillingService:
    def __init__(
        self,
        db: Session,
        gateway: SubscriptionGateway,
        plan: BillingPlan,
        clock: Callable[[], datetime],
        provider_name: str,
        frontend_base_url: str,
    ) -> None:
        self.db = db
        self.gateway = gateway
        self.plan = plan
        self.clock = clock
        self.provider_name = provider_name
        self.frontend_base_url = frontend_base_url.rstrip("/")

    # ------------------------------------------------------------------ consultas

    def view(self, user_id: uuid.UUID, roles: frozenset[Role]) -> SubscriptionView:
        row = self.open_subscription(user_id)
        return SubscriptionView(
            status=row.status if row else None,
            has_access=self.has_access(user_id, roles),
            amount_clp=row.amount_clp if row else self.plan.amount_clp,
            trial_days=row.trial_days if row else self.plan.trial_days,
            next_payment_date=row.next_payment_date if row else None,
            checkout_url=row.init_point
            if row and row.status == SubscriptionStatus.PENDING
            else None,
        )

    def has_access(self, user_id: uuid.UUID, roles: frozenset[Role]) -> bool:
        if Role.ADMINISTRATOR in roles:
            return True
        row = self.open_subscription(user_id)
        # Pendiente 5 del README: tras cancelar no se conserva acceso hasta decidirlo.
        return row is not None and row.status == SubscriptionStatus.AUTHORIZED

    # ------------------------------------------------------------------- comandos

    def start(self, user_id: uuid.UUID) -> str:
        """Crea (o reutiliza) la suscripción y devuelve el enlace de pago del proveedor."""
        # Bloquea la cuenta: dos solicitudes simultáneas no crean dos suscripciones.
        user = self.db.scalars(
            select(UserAccountRow).where(UserAccountRow.id == user_id).with_for_update()
        ).one()
        existing = self.open_subscription(user_id)
        if existing is not None:
            if existing.status == SubscriptionStatus.PENDING and existing.init_point:
                self.db.commit()
                return existing.init_point
            raise BillingError("already_subscribed", "Ya tienes una suscripción activa")

        now = self.clock()
        row = SubscriptionRow(
            id=uuid.uuid4(),
            user_id=user_id,
            provider=self.provider_name,
            status=SubscriptionStatus.PENDING,
            amount_clp=self.plan.amount_clp,
            trial_days=self.plan.trial_days,
            created_at=now,
            updated_at=now,
        )
        try:
            created = self.gateway.create(
                NewSubscription(
                    external_reference=str(row.id),
                    payer_email=user.email,
                    reason=SUBSCRIPTION_REASON,
                    amount_clp=self.plan.amount_clp,
                    trial_days=self.plan.trial_days,
                    back_url=f"{self.frontend_base_url}/suscripcion/retorno",
                )
            )
        except ProviderError as exc:
            self.db.rollback()
            raise _unavailable() from exc
        if not created.init_point:
            self.db.rollback()
            raise _unavailable()
        row.provider_subscription_id = created.id
        row.init_point = created.init_point
        row.status = SubscriptionStatus(created.status)
        self.db.add(row)
        self.db.flush()
        self._record(row, "created", None, row.status, now)
        self.db.commit()
        return created.init_point

    def sync_provider_subscription(self, provider_id: str, source: str) -> bool:
        """Actualiza desde el proveedor la suscripción `provider_id`. False si no es nuestra."""
        row = self.db.scalars(
            select(SubscriptionRow)
            .where(SubscriptionRow.provider_subscription_id == provider_id)
            .with_for_update()
        ).one_or_none()
        if row is None:
            return False
        self._refresh(row, source)
        return True

    def sync_user(self, user_id: uuid.UUID, source: str) -> None:
        """Al volver de la página de pago: consulta el estado real de la suscripción abierta."""
        row = self.db.scalars(
            select(SubscriptionRow)
            .where(SubscriptionRow.user_id == user_id)
            .where(SubscriptionRow.status.in_(OPEN_STATUSES))
            .with_for_update()
        ).one_or_none()
        if row is not None:
            self._refresh(row, source)

    def cancel(self, user_id: uuid.UUID) -> None:
        row = self.db.scalars(
            select(SubscriptionRow)
            .where(SubscriptionRow.user_id == user_id)
            .where(SubscriptionRow.status.in_(OPEN_STATUSES))
            .with_for_update()
        ).one_or_none()
        if row is None:
            raise BillingError("no_subscription", "No tienes una suscripción para cancelar")
        assert row.provider_subscription_id is not None
        try:
            remote = self.gateway.cancel(row.provider_subscription_id)
        except ProviderError as exc:
            self.db.rollback()
            raise _unavailable() from exc
        self._apply(row, remote.status, remote.next_payment_date, "cancel")
        self.db.commit()

    # ------------------------------------------------------------------ internos

    def _refresh(self, row: SubscriptionRow, source: str) -> None:
        assert row.provider_subscription_id is not None
        try:
            remote = self.gateway.get(row.provider_subscription_id)
        except ProviderError as exc:
            self.db.rollback()
            raise _unavailable() from exc
        # Defensa: la suscripción remota debe ser la que creamos para esta fila.
        if remote.external_reference not in (None, str(row.id)):
            self.db.rollback()
            raise BillingError("reference_mismatch", "La suscripción no corresponde")
        self._apply(row, remote.status, remote.next_payment_date, source)
        self.db.commit()

    def _apply(
        self, row: SubscriptionRow, status: str, next_payment: datetime | None, source: str
    ) -> None:
        try:
            new_status = SubscriptionStatus(status)
        except ValueError as exc:
            raise BillingError("unknown_status", f"Estado desconocido: {status}") from exc
        now = self.clock()
        row.next_payment_date = next_payment
        if new_status != row.status:
            previous = row.status
            row.status = new_status
            row.updated_at = now
            self._record(row, source, previous, new_status, now)

    def _record(
        self,
        row: SubscriptionRow,
        source: str,
        previous: SubscriptionStatus | None,
        new: SubscriptionStatus,
        at: datetime,
    ) -> None:
        self.db.add(
            BillingEventRow(
                subscription_id=row.id,
                source=source,
                previous_status=previous.value if previous else None,
                new_status=new.value,
                at=at,
            )
        )

    def open_subscription(self, user_id: uuid.UUID) -> SubscriptionRow | None:
        return self.db.scalars(
            select(SubscriptionRow)
            .where(SubscriptionRow.user_id == user_id)
            .where(SubscriptionRow.status.in_(OPEN_STATUSES))
        ).one_or_none()


def _unavailable() -> BillingError:
    return BillingError(
        "billing_unavailable", "No pudimos conectar con el medio de pago. Inténtalo de nuevo."
    )

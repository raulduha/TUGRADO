"""Correo de ánimo tras días sin entrar (FR-034, AC-043).

Una vez al día, el programador llama a `send_due_reminders`. Se escribe a quien tiene acceso al
estudio y lleva `INACTIVE_DAYS` o más sin entrar; un solo correo por ausencia (no se repite
hasta que vuelva a entrar) y nunca a quien se dio de baja.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.auth.email import EmailDeliveryError, EmailMessage, EmailSender
from app.auth.tokens import new_token
from app.clock import chile_date
from app.email_layout import Action, compose
from app.engagement.streaks import compute
from app.persistence.auth_models import Role, UserAccountRow, UserRoleRow
from app.persistence.billing_models import AccessGrantRow, SubscriptionRow, SubscriptionStatus
from app.persistence.engagement_models import ActivityDayRow, ReminderStateRow

logger = logging.getLogger("tugrado.engagement")

INACTIVE_DAYS = 2
BATCH_LIMIT = 500


def _has_access():
    authorized = select(SubscriptionRow.id).where(
        SubscriptionRow.user_id == UserAccountRow.id,
        SubscriptionRow.status == SubscriptionStatus.AUTHORIZED,
    )
    granted = select(AccessGrantRow.id).where(
        AccessGrantRow.user_id == UserAccountRow.id, AccessGrantRow.revoked_at.is_(None)
    )
    admin = select(UserRoleRow.user_id).where(
        UserRoleRow.user_id == UserAccountRow.id, UserRoleRow.role == Role.ADMINISTRATOR
    )
    return or_(authorized.exists(), granted.exists(), admin.exists())


def send_due_reminders(
    db: Session, sender: EmailSender, now: datetime, frontend_base_url: str
) -> int:
    today = chile_date(now)
    last_day = (
        select(ActivityDayRow.user_id, func.max(ActivityDayRow.day).label("last_day"))
        .group_by(ActivityDayRow.user_id)
        .subquery()
    )
    rows = db.execute(
        select(UserAccountRow, last_day.c.last_day, ReminderStateRow)
        .join(last_day, last_day.c.user_id == UserAccountRow.id)
        .outerjoin(ReminderStateRow, ReminderStateRow.user_id == UserAccountRow.id)
        .where(UserAccountRow.email_verified_at.is_not(None))
        .where(last_day.c.last_day <= today - timedelta(days=INACTIVE_DAYS))
        .where(ReminderStateRow.opted_out_at.is_(None))
        .where(_has_access())
        .limit(BATCH_LIMIT)
    ).all()

    sent = 0
    for user, last_active, state in rows:
        # Ya se le escribió en esta ausencia: espera a que vuelva a entrar.
        if state and state.last_sent_at and chile_date(state.last_sent_at) > last_active:
            continue
        if state is None:
            state = ReminderStateRow(user_id=user.id, unsubscribe_token=new_token())
            db.add(state)
        best = compute(
            set(db.scalars(select(ActivityDayRow.day).where(ActivityDayRow.user_id == user.id))),
            today,
        )[1]
        message = _message(user.email, best, state.unsubscribe_token, frontend_base_url)
        try:
            sender.send(message)
        except EmailDeliveryError as exc:
            db.rollback()
            logger.error("No se pudo enviar el recordatorio: %s", exc)
            continue
        state.last_sent_at = now
        db.commit()
        sent += 1
    return sent


def unsubscribe(db: Session, token: str, now: datetime) -> bool:
    state = db.scalars(
        select(ReminderStateRow).where(ReminderStateRow.unsubscribe_token == token)
    ).one_or_none()
    if state is None:
        return False
    if state.opted_out_at is None:
        state.opted_out_at = now
        db.commit()
    return True


def _message(to: str, best_streak: int, token: str, base: str) -> EmailMessage:
    base = base.rstrip("/")
    streak = (
        f"Tu mejor racha es de {best_streak} días: hoy puedes volver a encender el fueguito."
        if best_streak > 1
        else "Un ratito hoy basta para retomar el ritmo."
    )
    return compose(
        to=to,
        subject="Apruvi te está esperando",
        heading="¡Te extrañamos!",
        paragraphs=[
            "Llevas un par de días sin pasar por Aprueba tu examen.",
            streak,
            "Preparar el examen de grado es un camino largo, y la constancia es lo que más "
            "ayuda. ¡Tú puedes con esto!",
        ],
        action=Action("Volver a estudiar", f"{base}/panel"),
        frontend_base_url=base,
        unsubscribe_url=f"{base}/correos/baja?token={token}",
    )

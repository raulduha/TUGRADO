"""Correo de confirmación cuando la suscripción queda activa."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.auth.email import EmailMessage
from app.email_layout import Action, compose

_MONTHS = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def _chile_date(moment: datetime) -> str:
    try:
        zone: timezone | ZoneInfo = ZoneInfo("America/Santiago")
    except ZoneInfoNotFoundError:
        zone = timezone(timedelta(hours=-4))
    local = moment.astimezone(zone)
    return f"{local.day} de {_MONTHS[local.month - 1]} de {local.year}"


def _clp(amount: int) -> str:
    return "$" + f"{amount:,}".replace(",", ".")


def subscription_started(
    to: str,
    amount_clp: int,
    trial_days: int,
    next_payment: datetime | None,
    frontend_base_url: str,
) -> EmailMessage:
    manage = f"{frontend_base_url}/suscripcion"
    if trial_days > 0:
        subject = "Tu prueba gratis de Aprueba tu examen comenzó"
        charge = (
            f"No se te cobrará nada hasta el {_chile_date(next_payment)}; ese día Mercado Pago "
            f"cobrará {_clp(amount_clp)} y luego lo mismo cada mes."
            if next_payment
            else f"Al terminar la prueba, Mercado Pago cobrará {_clp(amount_clp)} cada mes."
        )
        opening = (
            f"Tu suscripción quedó activa y comenzó tu prueba gratis de {trial_days} días. "
            "Ya puedes entrar a estudiar."
        )
        cancel = f"Si cancelas antes de esa fecha, no se te cobrará: {manage}"
    else:
        subject = "Tu suscripción a Aprueba tu examen está activa"
        charge = (
            f"El próximo cobro de {_clp(amount_clp)} será el {_chile_date(next_payment)}."
            if next_payment
            else f"El cobro es de {_clp(amount_clp)} cada mes."
        )
        opening = "Tu suscripción mensual quedó activa. Ya puedes entrar a estudiar."
        cancel = f"Puedes cancelarla cuando quieras: {manage}"
    return compose(
        to=to,
        subject=subject,
        heading="¡Te damos la bienvenida a Aprueba tu examen!",
        paragraphs=[
            opening,
            charge,
            "El pago lo procesa Mercado Pago; nosotros no recibimos los datos de tu tarjeta.",
        ],
        action=Action("Ir a estudiar", f"{frontend_base_url}/panel"),
        note=cancel,
        frontend_base_url=frontend_base_url,
    )

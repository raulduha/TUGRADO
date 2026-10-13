"""Texto del correo de suscripción activa."""

from datetime import UTC, datetime

from app.billing.emails import subscription_started


def test_con_prueba_gratis_indica_la_fecha_del_primer_cobro_en_hora_de_chile():
    # 01:38 en Chile (UTC-3 en octubre) = 04:38 UTC del 20 de octubre.
    first_charge = datetime(2026, 10, 20, 4, 38, tzinfo=UTC)
    message = subscription_started("a@ejemplo.cl", 9990, 7, first_charge, "https://x.cl")
    assert message.subject == "Tu prueba gratis de Aprueba tu examen comenzó"
    assert "hasta el 20 de octubre de 2026" in message.body
    assert "$9.990" in message.body
    assert "https://x.cl/suscripcion" in message.body


def test_sin_prueba_gratis_indica_el_proximo_cobro():
    message = subscription_started("a@ejemplo.cl", 19990, 0, None, "https://x.cl")
    assert message.subject == "Tu suscripción a Aprueba tu examen está activa"
    assert "$19.990" in message.body

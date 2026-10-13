"""Errores de Mercado Pago: el motivo queda en el registro para diagnosticar."""

import logging

import httpx
import pytest

from app.billing.gateway import MERCADOPAGO_API, MercadoPagoGateway, NewSubscription, ProviderError


def _gateway(status: int, body: dict) -> MercadoPagoGateway:
    transport = httpx.MockTransport(lambda request: httpx.Response(status, json=body))
    return MercadoPagoGateway(
        "TEST-token", httpx.Client(base_url=MERCADOPAGO_API, transport=transport)
    )


def test_un_rechazo_registra_el_motivo_de_mercado_pago(caplog):
    gateway = _gateway(
        400, {"message": "Both payer and collector must be real or test users", "status": 400}
    )
    request = NewSubscription(
        external_reference="ref",
        payer_email="estudiante@ejemplo.cl",
        reason="Suscripción",
        amount_clp=9990,
        trial_days=7,
        back_url="https://apruebatuexamen.cl/suscripcion/retorno",
    )
    # Las migraciones de las pruebas (fileConfig de Alembic) desactivan los loggers existentes;
    # en producción corren en otro proceso. Se reactiva y se escucha directo.
    billing_logger = logging.getLogger("tugrado.billing")
    was_disabled = billing_logger.disabled
    billing_logger.disabled = False
    billing_logger.addHandler(caplog.handler)
    try:
        with pytest.raises(ProviderError, match="must be real or test users"):
            gateway.create(request)
    finally:
        billing_logger.removeHandler(caplog.handler)
        billing_logger.disabled = was_disabled
    assert "must be real or test users" in caplog.text
    assert "estudiante@ejemplo.cl" not in caplog.text

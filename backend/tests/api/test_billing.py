"""Suscripción con el simulador del proveedor (FR-029 a FR-031, AC-038, AC-039, Gate 11b)."""

import threading
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import SubscribedUser, get_clock, get_email_sender, get_subscription_gateway
from app.billing.gateway import FakeGateway, ProviderError
from app.billing.grants import GrantError, grant_access, revoke_access
from app.billing.signature import sign
from app.cli import create_admin
from app.config import get_settings
from app.db import get_engine
from app.persistence.billing_models import AccessGrantRow, BillingEventRow, SubscriptionRow
from tests.api.test_auth import EMAIL, code, login, verified_account

pytestmark = pytest.mark.integration

WEBHOOK_SECRET = "secreto-de-prueba"


@pytest.fixture
def gateway() -> FakeGateway:
    return FakeGateway("http://localhost:3000")


def _app(engine, clock, outbox, gateway):
    from app.main import create_app

    app = create_app()
    app.dependency_overrides[get_engine] = lambda: engine
    app.dependency_overrides[get_clock] = lambda: clock
    app.dependency_overrides[get_email_sender] = lambda: outbox
    app.dependency_overrides[get_subscription_gateway] = lambda: gateway

    @app.get("/estudio-de-prueba")
    def protected(user: SubscribedUser) -> dict:
        return {"ok": True}

    return TestClient(app, headers={"Origin": get_settings().frontend_origin})


@pytest.fixture
def billing_api(engine, clock, outbox, gateway, monkeypatch):
    """App con el simulador de pagos (BILLING_PROVIDER=fake, como en desarrollo), sin las
    claves de Mercado Pago que pueda tener el .env local."""
    monkeypatch.setenv("BILLING_PROVIDER", "fake")
    monkeypatch.setenv("MERCADOPAGO_ACCESS_TOKEN", "")
    monkeypatch.setenv("MERCADOPAGO_WEBHOOK_SECRET", "")
    get_settings.cache_clear()
    return _app(engine, clock, outbox, gateway)


@pytest.fixture
def mp_api(engine, clock, outbox, gateway, monkeypatch):
    """App configurada para Mercado Pago (con webhooks); el proveedor sigue simulado."""
    monkeypatch.setenv("BILLING_PROVIDER", "mercadopago")
    monkeypatch.setenv("MERCADOPAGO_ACCESS_TOKEN", "TEST-token")
    monkeypatch.setenv("MERCADOPAGO_WEBHOOK_SECRET", WEBHOOK_SECRET)
    get_settings.cache_clear()
    return _app(engine, clock, outbox, gateway)


def student(api, outbox):
    verified_account(api, outbox)
    assert login(api).status_code == 204


def subscriptions(engine) -> list[SubscriptionRow]:
    with Session(engine) as db:
        return list(db.scalars(select(SubscriptionRow)))


def events(engine) -> list[tuple[str, str | None, str]]:
    with Session(engine) as db:
        rows = db.scalars(select(BillingEventRow).order_by(BillingEventRow.id))
        return [(e.source, e.previous_status, e.new_status) for e in rows]


def webhook(api, provider_id, secret=WEBHOOK_SECRET, body=None, topic="subscription_preapproval"):
    ts = "1760000000"
    request_id = "req-123"
    signature = sign(secret, provider_id, request_id, ts)
    return api.post(
        f"/billing/webhooks/mercadopago?data.id={provider_id}&type={topic}",
        json=body or {"type": topic, "data": {"id": provider_id}},
        headers={"x-signature": f"ts={ts},v1={signature}", "x-request-id": request_id},
    )


# -------------------------------------------------------------------- suscribirse


def test_sin_suscripcion_no_hay_acceso_al_estudio(billing_api, outbox):
    student(billing_api, outbox)
    view = billing_api.get("/billing/subscription").json()
    assert view["status"] is None
    assert view["has_access"] is False
    assert view["amount_clp"] == 9990
    assert view["trial_days"] == 7
    response = billing_api.get("/estudio-de-prueba")
    assert response.status_code == 402
    assert code(response) == "subscription_required"


def test_suscribirse_redirige_al_pago_y_aprobar_da_acceso(billing_api, outbox, engine):
    student(billing_api, outbox)
    response = billing_api.post("/billing/subscription")
    assert response.status_code == 201
    checkout = response.json()["checkout_url"]
    assert checkout.startswith("http://localhost:3000/suscripcion/simulador?id=fake-")

    pending = billing_api.get("/billing/subscription").json()
    assert pending["status"] == "pending"
    assert pending["checkout_url"] == checkout
    assert pending["has_access"] is False

    approved = billing_api.post("/billing/fake/approve").json()
    assert approved["status"] == "authorized"
    assert approved["has_access"] is True
    assert approved["next_payment_date"] is not None  # fin de la prueba gratis
    assert billing_api.get("/estudio-de-prueba").status_code == 200
    assert events(engine) == [("created", None, "pending"), ("return", "pending", "authorized")]


def test_al_activarse_llega_un_correo_de_confirmacion_una_sola_vez(billing_api, outbox, engine):
    student(billing_api, outbox)
    billing_api.post("/billing/subscription", json={"payer_email": "pagos.mp@ejemplo.cl"})
    billing_api.post("/billing/fake/approve")
    # Una nueva consulta sin cambio de estado no repite el correo.
    billing_api.post("/billing/subscription/sync")

    [message] = [m for m in outbox.to(EMAIL) if "prueba gratis" in m.subject]
    # Se envía al correo de la cuenta, no al de Mercado Pago.
    assert not outbox.to("pagos.mp@ejemplo.cl")
    assert "7 días" in message.body
    assert "$9.990" in message.body
    assert "no garantizan la aprobación" in message.body
    assert "http://localhost:3000/suscripcion" in message.body


def test_suscribirse_dos_veces_no_duplica(billing_api, outbox, engine):
    student(billing_api, outbox)
    first = billing_api.post("/billing/subscription").json()["checkout_url"]
    second = billing_api.post("/billing/subscription").json()["checkout_url"]
    assert first == second
    assert len(subscriptions(engine)) == 1


def test_solicitudes_simultaneas_crean_una_sola_suscripcion(billing_api, outbox, engine):
    student(billing_api, outbox)
    barrier = threading.Barrier(4)
    results: list = []

    def worker():
        barrier.wait()
        results.append(billing_api.post("/billing/subscription").json()["checkout_url"])

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    assert len(set(results)) == 1
    assert len(subscriptions(engine)) == 1


def test_el_primer_cobro_es_al_terminar_la_prueba_gratis(billing_api, outbox, clock):
    student(billing_api, outbox)
    billing_api.post("/billing/subscription")
    clock.advance(600)  # el estudiante tarda en pagar en Mercado Pago
    approved = billing_api.post("/billing/fake/approve").json()
    created = clock() - timedelta(seconds=600)
    assert datetime.fromisoformat(approved["next_payment_date"]) == created + timedelta(days=7)


def test_un_pago_pendiente_antiguo_se_reemplaza_para_no_acortar_la_prueba(
    billing_api, outbox, engine, clock
):
    student(billing_api, outbox)
    first = billing_api.post("/billing/subscription").json()["checkout_url"]
    clock.advance(2 * 24 * 3600)  # vuelve dos días después
    second = billing_api.post("/billing/subscription").json()["checkout_url"]
    assert second != first
    rows = subscriptions(engine)
    assert sorted(r.status for r in rows) == ["cancelled", "pending"]
    approved = billing_api.post("/billing/fake/approve").json()
    assert datetime.fromisoformat(approved["next_payment_date"]) == clock() + timedelta(days=7)


def test_con_suscripcion_activa_no_se_puede_volver_a_suscribir(billing_api, outbox):
    student(billing_api, outbox)
    billing_api.post("/billing/subscription")
    billing_api.post("/billing/fake/approve")
    response = billing_api.post("/billing/subscription")
    assert response.status_code == 409
    assert code(response) == "already_subscribed"


def test_proveedor_caido_no_deja_suscripciones_a_medias(billing_api, outbox, engine, gateway):
    student(billing_api, outbox)

    def broken(_):
        raise ProviderError("caído")

    gateway.create = broken
    response = billing_api.post("/billing/subscription")
    assert response.status_code == 503
    assert code(response) == "billing_unavailable"
    assert subscriptions(engine) == []


# ----------------------------------------------------------------------- cancelar


def test_cancelar_quita_el_acceso_y_permite_volver_a_suscribirse(billing_api, outbox, engine):
    student(billing_api, outbox)
    billing_api.post("/billing/subscription")
    billing_api.post("/billing/fake/approve")
    cancelled = billing_api.post("/billing/subscription/cancel").json()
    # Pendiente 5 del README: por ahora el acceso termina al cancelar.
    assert cancelled["status"] is None
    assert cancelled["has_access"] is False
    assert billing_api.get("/estudio-de-prueba").status_code == 402
    assert billing_api.post("/billing/subscription").status_code == 201
    assert [s.status for s in subscriptions(engine)].count("cancelled") == 1


def test_cancelar_sin_suscripcion(billing_api, outbox):
    student(billing_api, outbox)
    response = billing_api.post("/billing/subscription/cancel")
    assert response.status_code == 404


# ------------------------------------------------------------------ administradores


def test_administrador_accede_sin_suscripcion(billing_api, engine, monkeypatch):
    monkeypatch.setenv("ADMIN_PASSWORD", "administra el banco 2026")
    create_admin("admin@ejemplo.cl", engine=engine)
    login(billing_api, email="admin@ejemplo.cl", password="administra el banco 2026")
    assert billing_api.get("/estudio-de-prueba").status_code == 200


# --------------------------------------------------- correo de Mercado Pago del pagador


def test_por_omision_paga_el_correo_de_la_cuenta(billing_api, outbox, engine, gateway):
    student(billing_api, outbox)
    assert billing_api.post("/billing/subscription").status_code == 201
    [row] = subscriptions(engine)
    assert gateway.payers[row.provider_subscription_id] == EMAIL
    assert billing_api.get("/billing/subscription").json()["payer_email"] == EMAIL


def test_el_estudiante_puede_pagar_con_otro_correo_de_mercado_pago(
    billing_api, outbox, engine, gateway
):
    student(billing_api, outbox)
    response = billing_api.post(
        "/billing/subscription", json={"payer_email": " Pagos.MP@Ejemplo.cl "}
    )
    assert response.status_code == 201
    [row] = subscriptions(engine)
    assert gateway.payers[row.provider_subscription_id] == "pagos.mp@ejemplo.cl"

    # Mismo correo: se reutiliza el pago pendiente.
    again = billing_api.post("/billing/subscription", json={"payer_email": "pagos.mp@ejemplo.cl"})
    assert again.json() == response.json()
    assert len(subscriptions(engine)) == 1


def test_cambiar_el_correo_reemplaza_el_pago_pendiente(billing_api, outbox, engine, gateway):
    student(billing_api, outbox)
    first = billing_api.post("/billing/subscription", json={"payer_email": "uno@ejemplo.cl"})
    second = billing_api.post("/billing/subscription", json={"payer_email": "dos@ejemplo.cl"})
    assert second.status_code == 201
    assert second.json() != first.json()
    rows = sorted(subscriptions(engine), key=lambda r: r.created_at)
    assert [r.status for r in rows].count("cancelled") == 1
    [open_row] = [r for r in rows if r.status == "pending"]
    assert open_row.payer_email == "dos@ejemplo.cl"


def test_un_correo_de_pagador_invalido_se_rechaza(billing_api, outbox):
    student(billing_api, outbox)
    response = billing_api.post("/billing/subscription", json={"payer_email": "no-es-correo"})
    assert response.status_code == 422


# ------------------------------------------------------- accesos de cortesía (FR-032)


def test_un_acceso_de_cortesia_da_acceso_sin_suscripcion(billing_api, outbox, engine, clock):
    student(billing_api, outbox)
    assert billing_api.get("/estudio-de-prueba").status_code == 402

    with Session(engine) as db:
        assert grant_access(db, EMAIL.upper(), "Cuenta de prueba", "equipo@proda.cl", clock())
        # Repetirlo no crea un segundo acceso.
        assert not grant_access(db, EMAIL, "Otra vez", "equipo@proda.cl", clock())

    view = billing_api.get("/billing/subscription").json()
    assert view["has_access"] is True and view["status"] is None
    assert billing_api.get("/estudio-de-prueba").status_code == 200


def test_revocar_el_acceso_lo_quita_y_conserva_el_historial(billing_api, outbox, engine, clock):
    student(billing_api, outbox)
    with Session(engine) as db:
        grant_access(db, EMAIL, "Cuenta de prueba", "equipo@proda.cl", clock())
        assert revoke_access(db, EMAIL, clock())
        assert not revoke_access(db, EMAIL, clock())

    assert billing_api.get("/estudio-de-prueba").status_code == 402
    with Session(engine) as db:
        grants = list(db.scalars(select(AccessGrantRow)))
    assert len(grants) == 1 and grants[0].revoked_at is not None
    assert grants[0].reason == "Cuenta de prueba" and grants[0].granted_by == "equipo@proda.cl"


def test_el_acceso_exige_cuenta_existente_y_motivo(engine, clock):
    with Session(engine) as db:
        with pytest.raises(GrantError):
            grant_access(db, "nadie@ejemplo.cl", "Pruebas", "equipo@proda.cl", clock())
        with pytest.raises(GrantError):
            grant_access(db, "nadie@ejemplo.cl", " ", "equipo@proda.cl", clock())


# ------------------------------------------------------------------------ webhooks


def test_webhook_valido_actualiza_desde_el_proveedor(mp_api, outbox, engine, gateway, clock):
    student(mp_api, outbox)
    mp_api.post("/billing/subscription")
    provider_id = subscriptions(engine)[0].provider_subscription_id
    gateway.approve(provider_id, clock())  # el estudiante pagó en Mercado Pago

    assert webhook(mp_api, provider_id).status_code == 200
    assert subscriptions(engine)[0].status == "authorized"
    # Una notificación repetida no duplica el cambio.
    assert webhook(mp_api, provider_id).status_code == 200
    assert events(engine) == [("created", None, "pending"), ("webhook", "pending", "authorized")]


def test_webhook_con_firma_invalida_se_rechaza_sin_cambios(mp_api, outbox, engine, gateway, clock):
    student(mp_api, outbox)
    mp_api.post("/billing/subscription")
    provider_id = subscriptions(engine)[0].provider_subscription_id
    gateway.approve(provider_id, clock())

    response = webhook(mp_api, provider_id, secret="clave-falsa")
    assert response.status_code == 401
    assert code(response) == "invalid_signature"
    unsigned = mp_api.post(
        f"/billing/webhooks/mercadopago?data.id={provider_id}&type=subscription_preapproval"
    )
    assert unsigned.status_code == 401
    assert subscriptions(engine)[0].status == "pending"


def test_el_contenido_del_webhook_no_se_usa_como_dato(mp_api, outbox, engine):
    student(mp_api, outbox)
    mp_api.post("/billing/subscription")
    provider_id = subscriptions(engine)[0].provider_subscription_id
    # Firma válida, pero el cuerpo afirma "authorized" y el proveedor dice "pending".
    forged = {
        "type": "subscription_preapproval",
        "data": {"id": provider_id},
        "status": "authorized",
    }
    assert webhook(mp_api, provider_id, body=forged).status_code == 200
    assert subscriptions(engine)[0].status == "pending"


def test_webhook_de_otro_topico_o_suscripcion_ajena_se_ignora(mp_api, outbox, engine):
    student(mp_api, outbox)
    assert webhook(mp_api, "123", topic="payment").json() == {"status": "ignored"}
    assert webhook(mp_api, "suscripcion-de-otro").status_code == 200
    assert events(engine) == []


def test_simulador_no_existe_con_mercadopago(mp_api, outbox):
    student(mp_api, outbox)
    assert mp_api.post("/billing/fake/approve").status_code == 404


def test_webhook_deshabilitado_sin_clave(billing_api):
    assert webhook(billing_api, "x").status_code == 404


def test_referencia_externa_ajena_se_rechaza(billing_api, outbox, engine, gateway):
    student(billing_api, outbox)
    billing_api.post("/billing/subscription")
    provider_id = subscriptions(engine)[0].provider_subscription_id
    from dataclasses import replace

    gateway._items[provider_id] = replace(gateway._items[provider_id], external_reference="otra")
    assert billing_api.post("/billing/subscription/sync").status_code == 400
    assert subscriptions(engine)[0].status == "pending"

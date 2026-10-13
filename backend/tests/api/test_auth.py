"""Flujo de cuentas por HTTP contra PostgreSQL (FR-001, AC-001, AC-032, AC-036, Gate 5)."""

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import AdminUser, CurrentUser, get_clock, get_email_sender, require_role
from app.cli import create_admin
from app.db import get_engine
from app.persistence.auth_models import Role, UserAccountRow

pytestmark = pytest.mark.integration

EMAIL = "estudiante@ejemplo.cl"
PASSWORD = "derecho civil 2026"
HOUR = 3600
DAY = 24 * HOUR


def register(api, email=EMAIL, password=PASSWORD):
    return api.post("/auth/register", json={"email": email, "password": password})


def login(api, email=EMAIL, password=PASSWORD):
    return api.post("/auth/login", json={"email": email, "password": password})


def verified_account(api, outbox, email=EMAIL):
    assert register(api, email).status_code == 202
    assert (
        api.post("/auth/verify-email", json={"token": outbox.last_token(email)}).status_code == 204
    )


def code(response) -> str:
    return response.json()["detail"]["code"]


# ------------------------------------------------------------- registro y verificación


def test_flujo_completo_registro_verificacion_sesion_y_cierre(api, outbox):
    assert register(api).status_code == 202
    assert len(outbox.to(EMAIL)) == 1
    assert "verificar-correo?token=" in outbox.to(EMAIL)[0].body

    response = login(api)
    assert response.status_code == 403
    assert code(response) == "email_not_verified"
    assert api.get("/auth/me").status_code == 401

    assert (
        api.post("/auth/verify-email", json={"token": outbox.last_token(EMAIL)}).status_code == 204
    )
    response = login(api)
    assert response.status_code == 204
    cookie = response.headers["set-cookie"]
    assert "tugrado_session=" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=lax" in cookie

    me = api.get("/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == EMAIL
    assert me.json()["roles"] == ["student"]

    assert api.post("/auth/logout").status_code == 204
    assert api.get("/auth/me").status_code == 401


def test_el_correo_se_normaliza(api, outbox):
    verified_account(api, outbox, email="estudiante@ejemplo.cl")
    assert login(api, email="  Estudiante@Ejemplo.CL ").status_code == 204


def test_registro_con_correo_existente_no_revela_la_cuenta(api, outbox, engine):
    first = register(api)
    second = register(api, password="otra clave distinta 99")
    assert first.status_code == second.status_code == 202
    assert first.json() == second.json()
    assert "Ya tienes una cuenta" in outbox.to(EMAIL)[-1].subject
    with Session(engine) as db:
        assert len(db.scalars(select(UserAccountRow)).all()) == 1


@pytest.mark.parametrize(
    ("password", "expected"),
    [
        ("corta-11ch.", "password_too_short"),
        ("1q2w3e4r5t6y", "password_too_common"),
    ],
)
def test_registro_rechaza_contrasenas_invalidas(api, password, expected):
    response = register(api, password=password)
    assert response.status_code == 422
    assert code(response) == expected


def test_enlace_de_verificacion_es_de_un_solo_uso(api, outbox):
    register(api)
    token = outbox.last_token(EMAIL)
    assert api.post("/auth/verify-email", json={"token": token}).status_code == 204
    response = api.post("/auth/verify-email", json={"token": token})
    assert response.status_code == 400
    assert code(response) == "invalid_token"


def test_enlace_de_verificacion_caduca_a_las_24_horas(api, outbox, clock):
    register(api)
    token = outbox.last_token(EMAIL)
    clock.advance(DAY)
    assert api.post("/auth/verify-email", json={"token": token}).status_code == 400


def test_enlace_de_verificacion_valido_justo_antes_de_24_horas(api, outbox, clock):
    register(api)
    token = outbox.last_token(EMAIL)
    clock.advance(DAY - 1)
    assert api.post("/auth/verify-email", json={"token": token}).status_code == 204


def test_reenviar_verificacion_invalida_el_enlace_anterior(api, outbox):
    register(api)
    old = outbox.last_token(EMAIL)
    assert api.post("/auth/resend-verification", json={"email": EMAIL}).status_code == 202
    new = outbox.last_token(EMAIL)
    assert api.post("/auth/verify-email", json={"token": old}).status_code == 400
    assert api.post("/auth/verify-email", json={"token": new}).status_code == 204


# ------------------------------------------------------------------ inicio de sesión


def test_correo_inexistente_y_contrasena_incorrecta_responden_igual(api, outbox):
    verified_account(api, outbox)
    wrong_password = login(api, password="no es la clave 123")
    unknown_email = login(api, email="nadie@ejemplo.cl")
    assert wrong_password.status_code == unknown_email.status_code == 401
    assert wrong_password.json() == unknown_email.json()


def test_sesion_caduca_tras_7_dias_sin_actividad(api, outbox, clock):
    verified_account(api, outbox)
    login(api)
    clock.advance(7 * DAY - 1)
    assert api.get("/auth/me").status_code == 200
    clock.advance(7 * DAY)
    assert api.get("/auth/me").status_code == 401


def test_la_actividad_renueva_la_inactividad_pero_no_supera_30_dias(api, outbox, clock):
    verified_account(api, outbox)
    login(api)
    for _ in range(4):  # actividad cada 6 días: nunca 7 días sin uso
        clock.advance(6 * DAY)
        assert api.get("/auth/me").status_code == 200
    clock.advance(6 * DAY - 1)  # día 30 menos un segundo
    assert api.get("/auth/me").status_code == 200
    clock.advance(1)  # día 30 exacto
    assert api.get("/auth/me").status_code == 401


def test_bloqueo_tras_10_intentos_fallidos(api, outbox, clock):
    verified_account(api, outbox)
    for _ in range(9):
        assert login(api, password="clave equivocada 1").status_code == 401
    # Con 9 fallos la cuenta sigue disponible.
    assert login(api).status_code == 204

    for _ in range(10):
        login(api, password="clave equivocada 1")
    response = login(api)
    assert response.status_code == 429
    assert code(response) == "account_locked"

    clock.advance(15 * 60 - 1)
    assert login(api).status_code == 429
    clock.advance(1)
    assert login(api).status_code == 204


def test_los_fallos_fuera_de_la_ventana_de_15_minutos_no_se_acumulan(api, outbox, clock):
    verified_account(api, outbox)
    for _ in range(9):
        login(api, password="clave equivocada 1")
    clock.advance(15 * 60)
    login(api, password="clave equivocada 1")
    assert login(api).status_code == 204


# -------------------------------------------------------- recuperación de contraseña


def test_recuperacion_cambia_la_clave_y_cierra_las_sesiones(api, outbox):
    verified_account(api, outbox)
    login(api)
    assert api.get("/auth/me").status_code == 200

    assert api.post("/auth/password-reset/request", json={"email": EMAIL}).status_code == 202
    token = outbox.last_token(EMAIL)
    new_password = "nueva clave procesal 2026"
    response = api.post(
        "/auth/password-reset/confirm", json={"token": token, "password": new_password}
    )
    assert response.status_code == 204

    assert api.get("/auth/me").status_code == 401  # la sesión anterior quedó revocada
    assert login(api).status_code == 401
    assert login(api, password=new_password).status_code == 204
    reuse = api.post(
        "/auth/password-reset/confirm", json={"token": token, "password": new_password}
    )
    assert reuse.status_code == 400


def test_enlace_de_recuperacion_caduca_a_los_30_minutos(api, outbox, clock):
    verified_account(api, outbox)
    api.post("/auth/password-reset/request", json={"email": EMAIL})
    token = outbox.last_token(EMAIL)
    clock.advance(30 * 60)
    response = api.post(
        "/auth/password-reset/confirm", json={"token": token, "password": "nueva clave 2026 ok"}
    )
    assert response.status_code == 400
    assert code(response) == "invalid_token"


def test_recuperacion_de_correo_inexistente_responde_igual_y_no_envia(api, outbox):
    response = api.post("/auth/password-reset/request", json={"email": "nadie@ejemplo.cl"})
    assert response.status_code == 202
    assert outbox.messages == []


def test_recuperacion_rechaza_contrasena_comun(api, outbox):
    verified_account(api, outbox)
    api.post("/auth/password-reset/request", json={"email": EMAIL})
    response = api.post(
        "/auth/password-reset/confirm",
        json={"token": outbox.last_token(EMAIL), "password": "1q2w3e4r5t6y"},
    )
    assert response.status_code == 422


# ------------------------------------------------------------- origen y autorización


def test_operacion_desde_otro_origen_se_rechaza(api, outbox):
    response = api.post(
        "/auth/register",
        json={"email": EMAIL, "password": PASSWORD},
        headers={"Origin": "https://sitio-malicioso.example"},
    )
    assert response.status_code == 403
    assert code(response) == "origin_not_allowed"
    assert outbox.messages == []


def test_consulta_get_desde_otro_origen_no_se_bloquea(api):
    response = api.get("/health", headers={"Origin": "https://sitio-malicioso.example"})
    assert response.status_code == 200


@pytest.fixture
def protected_api(engine, clock, outbox, api):
    """App mínima con rutas protegidas, para probar las dependencias de autorización."""
    app = FastAPI()

    @app.get("/solo-estudiante")
    def student_only(user: CurrentUser) -> dict:
        return {"id": str(user.id)}

    @app.get("/solo-admin", dependencies=[Depends(require_role(Role.ADMINISTRATOR))])
    def admin_only() -> dict:
        return {"ok": True}

    @app.get("/admin-anotado")
    def admin_annotated(user: AdminUser) -> dict:
        return {"email": user.email}

    app.dependency_overrides[get_engine] = lambda: engine
    app.dependency_overrides[get_clock] = lambda: clock
    app.dependency_overrides[get_email_sender] = lambda: outbox
    return TestClient(app)


def share_session(api, protected_api):
    """Copia la cookie de la sesión iniciada en `api` al cliente de rutas protegidas."""
    protected_api.cookies.set("tugrado_session", api.cookies.get("tugrado_session"))


def test_estudiante_no_accede_a_operaciones_de_administrador(api, outbox, protected_api):
    verified_account(api, outbox)
    login(api)
    share_session(api, protected_api)
    assert protected_api.get("/solo-estudiante").status_code == 200
    response = protected_api.get("/solo-admin")
    assert response.status_code == 403
    assert code(response) == "forbidden"


def test_administrador_creado_por_consola_accede(api, protected_api, engine, monkeypatch):
    admin_password = "administra el banco 2026"
    monkeypatch.setenv("ADMIN_PASSWORD", admin_password)
    assert create_admin("Admin@Ejemplo.cl", engine=engine) == 0
    assert login(api, email="admin@ejemplo.cl", password=admin_password).status_code == 204
    share_session(api, protected_api)
    assert protected_api.get("/solo-admin").status_code == 200
    assert protected_api.get("/admin-anotado").json() == {"email": "admin@ejemplo.cl"}


def test_consola_promueve_una_cuenta_existente(api, outbox, engine, protected_api):
    verified_account(api, outbox)
    assert create_admin(EMAIL, engine=engine) == 0
    login(api)
    assert sorted(api.get("/auth/me").json()["roles"]) == ["administrator", "student"]


def test_sin_sesion_no_hay_acceso(protected_api):
    response = protected_api.get("/solo-estudiante")
    assert response.status_code == 401
    assert code(response) == "not_authenticated"


def test_si_el_correo_falla_el_registro_igual_responde_y_se_puede_reenviar(api, outbox, engine):
    from app.auth.email import EmailDeliveryError

    original = outbox.send
    outbox.send = lambda message: (_ for _ in ()).throw(EmailDeliveryError("caído"))
    response = register(api)
    assert response.status_code == 202
    with Session(engine) as db:
        assert db.scalars(select(UserAccountRow)).one().email == EMAIL

    outbox.send = original
    assert api.post("/auth/resend-verification", json={"email": EMAIL}).status_code == 202
    verify = api.post("/auth/verify-email", json={"token": outbox.last_token(EMAIL)})
    assert verify.status_code == 204

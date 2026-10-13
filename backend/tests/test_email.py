import json

import httpx
import pytest

from app.auth.email import EmailDeliveryError, EmailMessage, ResendEmailSender

MESSAGE = EmailMessage(to="estudiante@ejemplo.cl", subject="Verifica tu correo", body="Hola")


def sender_with(handler):
    client = httpx.Client(base_url=ResendEmailSender.API, transport=httpx.MockTransport(handler))
    return ResendEmailSender(
        "re_clave_de_prueba", "Aprueba tu examen <no-reply@ejemplo.cl>", client
    )


def test_envia_a_la_api_de_resend():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["auth"] = request.headers["authorization"]
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"id": "49a3999c"})

    sender_with(handler).send(MESSAGE)
    assert seen["url"] == "https://api.resend.com/emails"
    assert seen["auth"] == "Bearer re_clave_de_prueba"
    assert seen["body"] == {
        "from": "Aprueba tu examen <no-reply@ejemplo.cl>",
        "to": ["estudiante@ejemplo.cl"],
        "subject": "Verifica tu correo",
        "text": "Hola",
    }


@pytest.mark.parametrize("status", [401, 422, 500])
def test_error_del_proveedor_no_expone_la_clave(status):
    sender = sender_with(lambda request: httpx.Response(status, json={"message": "error"}))
    with pytest.raises(EmailDeliveryError) as exc:
        sender.send(MESSAGE)
    assert "re_clave_de_prueba" not in str(exc.value)
    assert "estudiante@ejemplo.cl" not in str(exc.value)


def test_proveedor_inalcanzable():
    def handler(request):
        raise httpx.ConnectError("sin red")

    with pytest.raises(EmailDeliveryError):
        sender_with(handler).send(MESSAGE)


def test_envia_la_version_html_si_existe():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"id": "1"})

    message = EmailMessage(to="a@ejemplo.cl", subject="S", body="Hola", html="<p>Hola</p>")
    sender_with(handler).send(message)
    assert seen["body"]["text"] == "Hola"
    assert seen["body"]["html"] == "<p>Hola</p>"

"""Plantilla de correos: HTML seguro y texto plano equivalente."""

from app.email_layout import Action, compose


def _message():
    return compose(
        to="a@ejemplo.cl",
        subject="Verifica tu correo",
        heading="Confirma <tu> correo",
        paragraphs=["Hola & bienvenida"],
        action=Action("Confirmar", "https://x.cl/verificar-correo?token=abc&x=1"),
        note="Si no fuiste tú, ignora este correo.",
        frontend_base_url="https://x.cl/",
    )


def test_el_texto_plano_conserva_el_enlace_y_el_aviso():
    body = _message().body
    assert "Confirmar: https://x.cl/verificar-correo?token=abc&x=1" in body
    assert "no garantizan la aprobación" in body
    assert "<" not in body.replace("<tu>", "")


def test_el_html_escapa_el_contenido_y_usa_el_logo_del_sitio():
    html = _message().html
    assert html is not None
    assert "Confirma &lt;tu&gt; correo" in html
    assert "Hola &amp; bienvenida" in html
    assert 'href="https://x.cl/verificar-correo?token=abc&amp;x=1"' in html
    assert 'src="https://x.cl/apple-icon"' in html

"""Plantilla común de los correos: versión HTML (estilos en línea, compatible con clientes de
correo) y versión de texto plano con el mismo contenido y los mismos enlaces."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape

from app.auth.email import EmailMessage

BRAND = "#2f5bd3"
INK = "#1f2430"
MUTED = "#5d6474"
LINE = "#e7e1d6"
BACKGROUND = "#fbf8f3"
FOOTER = (
    "Aprueba tu examen es un servicio de PRODA SpA · contacto@proda.cl\n"
    "Las evaluaciones son orientativas y no garantizan la aprobación del examen."
)


@dataclass(frozen=True)
class Action:
    label: str
    url: str


def compose(
    *,
    to: str,
    subject: str,
    heading: str,
    paragraphs: list[str],
    frontend_base_url: str,
    action: Action | None = None,
    note: str | None = None,
) -> EmailMessage:
    """Arma el correo. `note` va en letra chica bajo el botón (p. ej. «si no lo pediste…»)."""
    text_parts = [heading, *paragraphs]
    if action:
        text_parts.append(f"{action.label}: {action.url}")
    if note:
        text_parts.append(note)
    text_parts.append(FOOTER)
    body = "\n\n".join(text_parts)
    return EmailMessage(
        to=to,
        subject=subject,
        body=body,
        html=_html(subject, heading, paragraphs, action, note, frontend_base_url.rstrip("/")),
    )


def _html(
    subject: str,
    heading: str,
    paragraphs: list[str],
    action: Action | None,
    note: str | None,
    base: str,
) -> str:
    font = "font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;"
    paras = "".join(
        f'<p style="margin:0 0 16px;{font}font-size:16px;line-height:1.6;color:{INK};">'
        f"{escape(p)}</p>"
        for p in paragraphs
    )
    button = ""
    if action:
        url = escape(action.url, quote=True)
        button = (
            '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:8px 0 20px;">'
            f'<tr><td style="border-radius:12px;background:{BRAND};">'
            f'<a href="{url}" style="display:inline-block;padding:14px 28px;{font}font-size:16px;'
            f'font-weight:600;color:#ffffff;text-decoration:none;border-radius:12px;">'
            f"{escape(action.label)}</a></td></tr></table>"
            f'<p style="margin:0 0 16px;{font}font-size:13px;line-height:1.5;color:{MUTED};">'
            "Si el botón no funciona, copia este enlace en tu navegador:<br>"
            f'<a href="{url}" style="color:{BRAND};word-break:break-all;">{escape(action.url)}</a>'
            "</p>"
        )
    small = (
        f'<p style="margin:0;{font}font-size:13px;line-height:1.5;color:{MUTED};">'
        f"{escape(note)}</p>"
        if note
        else ""
    )
    footer = "<br>".join(escape(line) for line in FOOTER.split("\n"))
    return f"""<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{escape(subject)}</title></head>
<body style="margin:0;padding:0;background:{BACKGROUND};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"
 style="background:{BACKGROUND};">
<tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
<tr><td style="padding:0 4px 20px;">
<a href="{escape(base, quote=True)}" style="text-decoration:none;">
<img src="{escape(base, quote=True)}/apple-icon" width="36" height="36" alt=""
 style="vertical-align:middle;border-radius:9px;border:0;">
<span style="vertical-align:middle;margin-left:8px;{font}font-size:18px;font-weight:600;
color:{INK};">Aprueba tu examen</span></a>
</td></tr>
<tr><td style="background:#ffffff;border:1px solid {LINE};border-radius:20px;padding:32px 28px;">
<h1 style="margin:0 0 16px;{font}font-size:22px;line-height:1.3;color:{INK};">{escape(heading)}</h1>
{paras}{button}{small}
</td></tr>
<tr><td style="padding:20px 8px 0;{font}font-size:12px;line-height:1.6;color:{MUTED};
text-align:center;">{footer}</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""

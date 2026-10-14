"""Genera la hoja de bocetos (storyboard.html) de los videos de bienvenida y motivación,
reutilizando estilos y símbolos SVG de la hoja del Reel de Apruvi. Ejecutar desde marketing/."""

from pathlib import Path

base = Path("reel-apruvi/storyboard.html").read_text(encoding="utf-8")
head = base[: base.index("<header>")]  # <head>, estilos y símbolos (#apruvi, #flame)

LOGO = (
    '<svg viewBox="0 0 32 32" style="width:9cqw"><rect width="32" height="32" rx="9" fill="#2f5bd3"/>'
    '<path d="M16 8 5 13l11 5 11-5-11-5Z" fill="#fff"/></svg>'
)


def ap(left, top, width):
    return f'<svg class="apruvi" style="left:{left}%;top:{top}%;width:{width}%"><use href="#apruvi"/></svg>'


def flame(left, top, width, dim=False):
    style = "filter:grayscale(1);opacity:.45;" if dim else ""
    return (
        f'<svg style="position:absolute;left:{left}%;top:{top}%;width:{width}%;{style}" '
        f'viewBox="0 0 32 40"><use href="#flame"/></svg>'
    )


def lockup(top):
    return (
        f'<div class="t" style="top:{top}%;font-size:6.5cqw;display:flex;gap:2cqw;justify-content:center;align-items:center">'
        f"{LOGO}Aprueba tu examen</div>"
        f'<div class="t" style="top:{top + 5.5}%;font-size:5cqw;color:var(--brand);font-weight:600">apruebatuexamen.cl</div>'
    )


def cell(n, name, span, body, note, chip, bg=""):
    style = f' style="background:{bg}"' if bg else ""
    return f"""
  <section class="cell" id="frame-{n:02d}">
    <div class="frame"{style}>
      <div class="safe top"></div><div class="safe bot"></div>
      {body}
    </div>
    <div class="label"><span>{n:02d} · {name}</span><span>{span}</span></div>
    <p class="note">{note}</p>
    <span class="chip">{chip}</span>
  </section>"""


def sheet(title, dek, tag, cells):
    return (
        head
        + f"""<header>
  <h1>{title}</h1>
  <p class="dek">{dek}</p>
  <span class="tag">{tag}</span>
</header>
<main class="grid">{''.join(cells)}
</main>
</body>
</html>
"""
    )


welcome = [
    cell(1, "HOLA", "0–3,39 s",
         ap(22, 40, 56)
         + '<div class="bubble" style="left:12%;right:12%;top:20%;text-align:center">¡Hola! Soy Apruvi</div>'
         + '<div class="t" style="top:74%;font-size:8cqw">Te damos la bienvenida</div>',
         "<b>Intro tranquila:</b> Apruvi aparece y saluda; el globo entra en 1,81 y la bienvenida en 2,6.",
         "corte duro en 3,39 (subida)"),
    cell(2, "MAPA", "3,39–7,57 s",
         '<div class="t" style="top:17%;font-size:10cqw">Tu mapa<br>de estudio</div>'
         '<div class="node" style="left:43%;top:40%;background:var(--success);border-color:#05603a">✓</div>'
         '<div class="node" style="left:63%;top:53%;background:var(--brand);border-color:var(--brand-strong)">2</div>'
         '<div class="node" style="left:27%;top:66%;background:#ece7de;border-color:#d6cfc2;color:var(--muted)">3</div>'
         + ap(64, 40, 22),
         "<b>El camino se dibuja y aparece un nodo por golpe</b> (4,41 · 5,02 · 5,99 · 6,78); Apruvi salta de nodo en nodo.",
         "corte duro en 7,57"),
    cell(3, "PRÁCTICA", "7,57–10,96 s",
         '<div class="t" style="top:17%;font-size:10cqw">Practica<br><span style="color:var(--brand)">y simula el oral</span></div>'
         '<div class="bubble" style="left:10%;right:10%;top:42%;font-size:5cqw">A · Desde la concepción</div>'
         '<div class="bubble" style="left:10%;right:10%;top:51%;font-size:5cqw;border-color:var(--success);background:#e7f6ee">B · Al nacer ✓</div>'
         '<div class="bubble" style="left:10%;right:10%;top:60%;font-size:5cqw">C · Al inscribirse</div>'
         + ap(36, 68, 26),
         "<b>Una tarjeta de alternativas entra en 7,57</b>; la B se pone verde en el golpe 9,2 y en 10,17 aparecen las barras de voz.",
         "corte duro en 10,96"),
    cell(4, "RACHA", "10,96–14,35 s",
         '<div class="t" style="top:17%;font-size:10cqw">Cuida tu racha</div>'
         + flame(32, 28, 36)
         + '<div class="t" style="top:52%;font-size:30cqw;color:#c2410c">7</div>'
         '<div class="t" style="top:71%;font-size:7cqw;color:var(--muted);font-weight:600">días seguidos</div>',
         "<b>La llama entra en 10,96</b> y el contador sube de 1 a 7, fijándose con un golpe en 13,38.",
         "corte duro en 14,35",
         "radial-gradient(circle at 50% 38%, #fff1e6, #fdf1dc 42%, #fbf8f3 75%)"),
    cell(5, "EMPIEZA", "14,35–16,91 s",
         '<div class="btn" style="top:22%">Empieza tus<br>7 días gratis</div>'
         + ap(34, 42, 32) + lockup(64),
         "<b>El botón entra en 14,35</b>; en 15,91 cae la marca con confeti y se mantiene durante el desvanecido.",
         "fin con desvanecido"),
]

motivation = [
    cell(1, "PREGUNTA", "0–3,3 s",
         '<div class="t" style="top:20%;font-size:12cqw">¿Un par de días<br><span style="color:var(--brand)">sin estudiar?</span></div>'
         + ap(18, 50, 44) + flame(64, 60, 18, dim=True),
         "<b>Arranque suave:</b> Apruvi descansa junto a una llama apagada; las dos líneas aparecen en 1,04 y 1,81. Tono amable, sin culpa.",
         "corte en 3,3"),
    cell(2, "ESPERA", "3,3–6,66 s",
         ap(28, 46, 44)
         + '<div class="bubble" style="left:14%;right:14%;top:26%;text-align:center">Te estoy esperando</div>'
         + flame(68, 62, 14, dim=True),
         "<b>Apruvi se levanta y dice “Te estoy esperando”</b> (4,16); respira tranquilo y se agacha un poco antes de la subida.",
         "corte duro en 6,66 (subida)"),
    cell(3, "RATITO", "6,66–9,89 s",
         flame(30, 22, 40)
         + '<div class="t" style="top:52%;font-size:12cqw">Un ratito hoy<br><span style="color:var(--brand)">ya cuenta</span></div>'
         + ap(36, 68, 26),
         "<b>La llama se enciende de golpe en 6,66</b> con rayos; el texto cae en 7,36 y Apruvi salta en 8,34 y 9,12.",
         "corte duro en 9,89",
         "radial-gradient(circle at 50% 30%, #fff1e6, #fdf1dc 42%, #fbf8f3 75%)"),
    cell(4, "VUELVE", "9,89–13 s",
         '<div class="t" style="top:17%;font-size:10cqw">Vuelve a encender<br>tu racha</div>'
         + flame(40, 34, 20) + ap(34, 46, 32) + lockup(66),
         "<b>La semana se enciende en 9,89 y 10,68</b>; en el golpe 11,54 cae la marca con confeti.",
         "fin con desvanecido"),
]

Path("reel-bienvenida/storyboard.html").write_text(
    sheet("Video de bienvenida · storyboard v1",
          "Para quien recién se registra: Apruvi presenta el mapa, la práctica, el oral y la racha, e invita a los 7 días gratis.",
          "1080×1920 · 16,9 s · 30 fps · música “Wake up” (MBB) 99,5–116,5 s",
          welcome), encoding="utf-8")
Path("reel-motivacion/storyboard.html").write_text(
    sheet("Video de motivación · storyboard v1",
          "Para el correo de ánimo y redes: después de unos días sin entrar, Apruvi invita a volver con calma, sin culpa.",
          "1080×1920 · 13 s · 30 fps · música “Wake up” (MBB) 28,3–41,3 s",
          motivation), encoding="utf-8")
print("ok")

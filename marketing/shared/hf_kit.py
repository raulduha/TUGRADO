"""Kit compartido de los videos de Apruvi (HyperFrames): Apruvi, llama, logo, fuente,
movimiento vivo y la plantilla de cada escena. Lo importan los build_frames.py de cada proyecto.

Origen: el generador del Reel de Apruvi (marketing/reel-apruvi).

Cada escena es una subcomposición con su propio timeline de GSAP en pausa. Apruvi, la fuente
y los colores salen de frame.md / motion.md. Ejecutar desde la raíz del proyecto:
    python scripts/build_frames.py
"""

from pathlib import Path

OUT = Path("compositions/frames")
W, H = 1080, 1920

FONT = """
@font-face { font-family: "Geist"; src: url("assets/fonts/Geist-latin.woff2") format("woff2"); font-weight: 100 900; }
"""

COLORS = """
--bg:#fbf8f3; --fg:#1f2430; --muted:#5d6474; --line:#e7e1d6; --brand:#2f5bd3; --brand-strong:#2448ad;
--brand-soft:#e8eefc; --accent:#f5a524; --accent-soft:#fdf1dc; --success:#067647;
--flame:#f97316; --flame-in:#fbbf24;
"""


def apruvi(pid: str, extra: str = "") -> str:
    """SVG de Apruvi (frontend/src/components/apruvi.tsx) con partes animables namespaced."""
    return f"""
<svg id="{pid}" class="apruvi" viewBox="0 0 120 130" {extra}>
  <ellipse id="{pid}-shadow" cx="60" cy="122" rx="30" ry="5" fill="#1f2430" opacity=".14"/>
  <g id="{pid}-body">
    <ellipse cx="46" cy="116" rx="9" ry="5" fill="#2448ad"/>
    <ellipse cx="74" cy="116" rx="9" ry="5" fill="#2448ad"/>
    <path d="M60 38c24 0 38 18 38 42 0 22-16 36-38 36S22 102 22 80c0-24 14-42 38-42Z" fill="#2f5bd3"/>
    <ellipse cx="60" cy="90" rx="22" ry="19" fill="#ffffff" opacity=".92"/>
    <path id="{pid}-arm-l" d="M24 82c-7 2-10 8-8 13" stroke="#2f5bd3" stroke-width="8" stroke-linecap="round" fill="none"/>
    <path id="{pid}-arm-r" d="M96 82c7 2 10 8 8 13" stroke="#2f5bd3" stroke-width="8" stroke-linecap="round" fill="none"/>
    <g id="{pid}-eyes">
      <ellipse cx="47" cy="66" rx="9" ry="10.5" fill="#fff"/>
      <ellipse cx="73" cy="66" rx="9" ry="10.5" fill="#fff"/>
      <circle cx="48.5" cy="68" r="5.5" fill="#1f2430"/>
      <circle cx="71.5" cy="68" r="5.5" fill="#1f2430"/>
      <circle cx="50.5" cy="65.5" r="2" fill="#fff"/>
      <circle cx="73.5" cy="65.5" r="2" fill="#fff"/>
    </g>
    <ellipse cx="37" cy="78" rx="5.5" ry="3.5" fill="#f7a8b8"/>
    <ellipse cx="83" cy="78" rx="5.5" ry="3.5" fill="#f7a8b8"/>
    <path d="M53 79c3.5 4 10.5 4 14 0" stroke="#1f2430" stroke-width="2.6" stroke-linecap="round" fill="none"/>
    <path d="M60 14 26 28l34 14 34-14-34-14Z" fill="#1f2a4d"/>
    <path d="M40 34v8c0 4 9 7 20 7s20-3 20-7v-8l-20 8-20-8Z" fill="#2b3864"/>
    <g id="{pid}-tassel">
      <path d="M88 30v14" stroke="#f5a524" stroke-width="2.4" stroke-linecap="round"/>
      <circle cx="88" cy="46" r="3.6" fill="#f5a524"/>
    </g>
    <circle cx="60" cy="28" r="2.4" fill="#f5a524"/>
  </g>
</svg>"""


FLAME = """<svg {attrs} viewBox="0 0 32 40">
  <path class="fl-out" d="M16 2c1 7 9 10 9 21a9 9 0 0 1-18 0c0-5 3-8 5-11 0 4 2 6 3 6-1-6 0-11 1-16Z" fill="#f97316"/>
  <path class="fl-in" d="M16 18c1 4 5 6 5 11a5 5 0 0 1-10 0c0-3 2-5 3-7 0 2 1 3 2 3-1-3 0-5 0-7Z" fill="#fbbf24"/>
</svg>"""

LOGO = """<svg {attrs} viewBox="0 0 32 32">
  <rect width="32" height="32" rx="9" fill="#2f5bd3"/>
  <path d="M16 8 5 13l11 5 11-5-11-5Z" fill="#fff"/>
  <path d="M9.5 15.2v4.6c0 1.6 2.9 3.2 6.5 3.2s6.5-1.6 6.5-3.2v-4.6L16 18.1l-6.5-2.9Z" fill="#fff" opacity=".85"/>
  <path d="M26 13.5v5.5" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/>
  <circle cx="26" cy="20" r="1.4" fill="#f5a524"/>
</svg>"""

# Movimiento vivo de Apruvi (motion.md): respiración 3,8 s, borla 3,8 s, parpadeo.
LIFE_JS = """
function apruviLife(tl, pid, dur, blinks) {
  const body = '#' + pid + '-body';
  const n = Math.max(0, Math.floor(dur / 1.9) - 1);
  tl.fromTo(body, { scaleX: 1, scaleY: 1 }, { scaleX: 0.985, scaleY: 1.035, duration: 1.9, ease: 'sine.inOut',
    yoyo: true, repeat: n, transformOrigin: '50% 100%' }, 0);
  tl.fromTo('#' + pid + '-tassel', { rotation: -5 }, { rotation: 6, duration: 1.9, ease: 'sine.inOut',
    yoyo: true, repeat: n, transformOrigin: '50% 0%' }, 0);
  blinks.forEach(function (t) {
    tl.to('#' + pid + '-eyes', { scaleY: 0.1, duration: 0.07, yoyo: true, repeat: 1, ease: 'none',
      transformOrigin: '50% 55%' }, t);
  });
}
function popIn(tl, sel, t, from) {
  tl.fromTo(sel, Object.assign({ opacity: 0, scale: 0.85, y: 40 }, from || {}),
    { opacity: 1, scale: 1, y: 0, duration: 0.45, ease: 'back.out(2.2)' }, t);
}
"""


def frame(fid: str, dur: float, css: str, body: str, js: str, bg: str) -> str:
    # Un id que empieza con número no sirve como selector CSS: se usa el atributo.
    root = f'[data-composition-id="{fid}"]'
    css = css.replace(f"#{fid}", root)
    return f"""<!doctype html>
<html lang="es">
<head><meta charset="UTF-8" /></head>
<body>
<template>
<style>
{FONT}
{root} {{
  position: absolute; inset: 0; width: {W}px; height: {H}px; overflow: hidden;
  font-family: "Geist", system-ui, sans-serif; color: #1f2430; background: {bg};
  {COLORS}
}}
{root} * {{ box-sizing: border-box; margin: 0; }}
{root} .layer {{ position: absolute; inset: 0; }}
{root} .apruvi {{ position: absolute; overflow: visible; }}
{root} .t {{ position: absolute; left: 80px; right: 80px; text-align: center; font-weight: 700; letter-spacing: -0.03em; line-height: 1; }}
{css}
</style>
<div id="{fid}" data-composition-id="{fid}" data-width="{W}" data-height="{H}" data-duration="{dur}">
{body}
</div>
<script>
(function () {{
{LIFE_JS}
const tl = gsap.timeline({{ paused: true }});
{js}
tl.seek(0);
window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
</body>
</html>
"""


WARM_BG = "linear-gradient(180deg, #e8eefc 0%, #fbf8f3 55%, #fdf1dc 100%)"

ICONS = {
    "check": "M5 12 l5 5 L20 7",
    "list": "M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01",
    "lock": "M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3",
    "cap": "M12 4 2 9l10 5 10-5-10-5ZM6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5",
    "mic": "M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3ZM19 11a7 7 0 0 1-14 0M12 18v3",
    "book": "M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2V5ZM8 7h7",
}

WARM_BG = "linear-gradient(180deg, #e8eefc 0%, #fbf8f3 55%, #fdf1dc 100%)"


def write(name: str, html: str) -> None:
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print("escrito", name)

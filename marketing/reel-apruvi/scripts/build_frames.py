"""Genera compositions/frames/*.html del Reel de Apruvi a partir del plan (STORYBOARD.md).

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

# ------------------------------------------------------------------ 01 · intro (0–3,3 s)
f1 = frame(
    "01-intro",
    3.3,
    """
#01-intro .bubble-deco { position: absolute; border-radius: 50%; }
#01-intro #i-q { top: 300px; font-size: 136px; }
#01-intro #i-q div { will-change: transform; }
#01-intro #i-q .brand { color: #2f5bd3; }
#01-intro #i-ap { left: 250px; top: 860px; width: 580px; height: 628px; }
""",
    f"""
<div class="layer" id="i-deco">
  <div class="bubble-deco" id="i-c1" style="left:-120px;top:520px;width:380px;height:380px;background:#2f5bd3;opacity:.07"></div>
  <div class="bubble-deco" id="i-c2" style="right:-90px;top:1180px;width:300px;height:300px;background:#f5a524;opacity:.16"></div>
  <div class="bubble-deco" id="i-c3" style="right:120px;top:220px;width:90px;height:90px;background:#067647;opacity:.12"></div>
</div>
<div class="t" id="i-q">
  <div id="i-l1">¿Se viene</div>
  <div id="i-l2">tu examen</div>
  <div id="i-l3" class="brand">de grado?</div>
</div>
{apruvi("i-ap")}
""",
    """
// Apruvi aterriza en el primer pulso (0,07) con aplastamiento y rebote.
tl.fromTo('#i-ap', { y: -260, scaleX: 0.9, scaleY: 1.1, transformOrigin: '50% 100%' },
  { y: 0, duration: 0.07, ease: 'power2.in' }, 0);
tl.to('#i-ap', { scaleX: 1.14, scaleY: 0.86, duration: 0.08, ease: 'power1.out' }, 0.07);
tl.to('#i-ap', { scaleX: 1, scaleY: 1, duration: 0.5, ease: 'elastic.out(1, 0.45)' }, 0.15);
apruviLife(tl, 'i-ap', 3.3, [1.15, 2.85]);
// Una línea de la pregunta por pulso (0,79 · 1,58 · 2,51), entrando un poco antes.
[['#i-l1', 0.79], ['#i-l2', 1.58], ['#i-l3', 2.51]].forEach(function (p) {
  popIn(tl, p[0], p[1] - 0.12, { y: 70 });
});
// Saltito de Apruvi con cada línea.
[0.79, 1.58, 2.51].forEach(function (t) {
  tl.to('#i-ap', { y: -46, duration: 0.18, ease: 'power2.out' }, t - 0.02);
  tl.to('#i-ap', { y: 0, duration: 0.2, ease: 'power2.in' }, t + 0.16);
});
// Decoración flotando suave todo el tramo.
tl.fromTo('#i-c1', { y: 0 }, { y: -60, duration: 3.3, ease: 'sine.inOut' }, 0);
tl.fromTo('#i-c2', { y: 0 }, { y: 50, duration: 3.3, ease: 'sine.inOut' }, 0);
// Golpe de 3,2: la pregunta golpea en escala y se tiñe un instante.
tl.to('#i-q', { scale: 1.1, duration: 0.08, ease: 'power3.out' }, 3.12);
tl.to('#i-ap', { scaleX: 1.12, scaleY: 0.9, duration: 0.08, ease: 'power3.out', transformOrigin: '50% 100%' }, 3.12);
""",
    WARM_BG,
)

# ------------------------------------------------------------------ 02 · mapa (3,3–9,91 s)
# Locales: nodos en 0 · 0,88 · 1,67 · 2,44; g2 en 3,39; globo en 4,18; fin 6,61.
N = [(540, 700), (780, 940), (330, 1180), (600, 1400)]
path_d = (
    f"M {N[0][0]} {N[0][1]} C {N[0][0]} 820, {N[1][0]} 820, {N[1][0]} {N[1][1]} "
    f"C {N[1][0]} 1060, {N[2][0]} 1060, {N[2][0]} {N[2][1]} "
    f"C {N[2][0]} 1300, {N[3][0]} 1300, {N[3][0]} {N[3][1]}"
)
done_d = f"M {N[0][0]} {N[0][1]} C {N[0][0]} 820, {N[1][0]} 820, {N[1][0]} {N[1][1]}"
node_html = ""
node_styles = [
    ("#067647", "#05603a", "check", "#fff"),
    ("#2f5bd3", "#2448ad", "list", "#fff"),
    ("#ece7de", "#d6cfc2", "lock", "#5d6474"),
    ("#ece7de", "#d6cfc2", "cap", "#5d6474"),
]
ICONS = {
    "check": "M5 12 l5 5 L20 7",
    "list": "M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01",
    "lock": "M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3",
    "cap": "M12 4 2 9l10 5 10-5-10-5ZM6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5",
}
for i, ((x, y), (bgc, border, icon, ink)) in enumerate(zip(N, node_styles)):
    halo = (
        '<div class="halo"></div>' if i == 1 else ""
    )
    node_html += f"""
<div class="node" id="m-n{i}" style="left:{x - 80}px;top:{y - 80}px;background:{bgc};border-bottom-color:{border}">
  {halo}<svg viewBox="0 0 24 24" width="76" height="76" fill="none" stroke="{ink}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[icon]}"/></svg>
</div>"""

f2 = frame(
    "02-mapa",
    6.61,
    """
#02-mapa #m-title { top: 300px; font-size: 104px; line-height: 0.98; }
#02-mapa #m-sub { top: 520px; font-size: 48px; font-weight: 600; color: #5d6474; letter-spacing: -0.01em; }
#02-mapa .node { position: absolute; width: 160px; height: 160px; border-radius: 50%; border-bottom: 16px solid; display: grid; place-items: center; }
#02-mapa .halo { position: absolute; inset: -26px; border-radius: 50%; background: rgba(47,91,211,.16); z-index: -1; }
#02-mapa #m-ap { left: 820px; top: 600px; width: 230px; height: 249px; }
#02-mapa #m-big { left: 70px; top: 1010px; width: 470px; height: 509px; }
#02-mapa #m-bubble { position: absolute; left: 360px; right: 70px; top: 760px; background: #fff; border: 3px solid #e7e1d6;
  border-radius: 56px; padding: 44px 50px; font-size: 76px; font-weight: 700; line-height: 1.05; letter-spacing: -0.03em;
  box-shadow: 0 30px 70px rgba(31,36,48,.12); }
#02-mapa #m-bubble::after { content: ""; position: absolute; left: 60px; bottom: -34px; width: 70px; height: 70px; background: #fff;
  border-right: 3px solid #e7e1d6; border-bottom: 3px solid #e7e1d6; transform: rotate(45deg); border-radius: 0 0 14px 0; }
#02-mapa #m-bubble .b { color: #2f5bd3; }
""",
    f"""
<div class="layer" id="g1">
  <div class="t" id="m-title">Tu mapa<br>de estudio</div>
  <div class="t" id="m-sub">Avanza paso a paso</div>
  <svg class="layer" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
    <path id="m-path" d="{path_d}" fill="none" stroke="#e7e1d6" stroke-width="44" stroke-linecap="round"/>
    <path id="m-dash" d="{path_d}" fill="none" stroke="#fff" stroke-width="10" stroke-dasharray="4 28" stroke-linecap="round"/>
    <path id="m-done" d="{done_d}" fill="none" stroke="#067647" stroke-width="44" stroke-linecap="round" opacity=".55"/>
  </svg>
  {node_html}
  {apruvi("m-ap")}
</div>
<div class="layer" id="g2">
  {apruvi("m-big")}
  <div id="m-bubble">Nivel a nivel,<br><span class="b">yo te acompaño.</span></div>
</div>
""",
    """
// g1 visible todo el tramo (queda atenuado detrás de g2); g2 entra en 3,39.
tl.set('#g2', { autoAlpha: 0 }, 0);
tl.set('#g2', { autoAlpha: 1 }, 3.39);
popIn(tl, '#m-title', 0, { y: 30 });
popIn(tl, '#m-sub', 0.2, { y: 20 });
// El camino se dibuja hasta cada nodo; un nodo por pulso.
const path = document.querySelector('#m-path');
const len = path.getTotalLength();
['#m-path', '#m-dash'].forEach(function (s) {
  tl.set(s, { strokeDasharray: s === '#m-dash' ? '4 28' : len, strokeDashoffset: s === '#m-dash' ? 0 : len }, 0);
});
tl.set('#m-dash', { opacity: 0 }, 0);
tl.to('#m-path', { strokeDashoffset: 0, duration: 2.44, ease: 'none' }, 0);
tl.to('#m-dash', { opacity: 1, duration: 0.3 }, 2.3);
const done = document.querySelector('#m-done');
const dl = done.getTotalLength();
tl.set('#m-done', { strokeDasharray: dl, strokeDashoffset: dl }, 0);
tl.to('#m-done', { strokeDashoffset: 0, duration: 0.8, ease: 'power2.inOut' }, 0.1);
[0, 0.88, 1.67, 2.44].forEach(function (t, i) {
  tl.fromTo('#m-n' + i, { scale: 0, rotation: -12 }, { scale: 1, rotation: 0, duration: 0.42, ease: 'back.out(2.4)' }, Math.max(0, t - 0.1));
});
// Apruvi junto al primer nodo; salta al nodo actual en 0,88 y celebra en los pulsos siguientes.
tl.set('#m-ap', { x: -190, y: 0 }, 0);
tl.to('#m-ap', { x: 0, duration: 0.42, ease: 'power1.inOut' }, 0.46);
tl.to('#m-ap', { y: -120, duration: 0.21, ease: 'power2.out' }, 0.46);
tl.to('#m-ap', { y: 240, duration: 0.21, ease: 'power2.in' }, 0.67);
tl.to('#m-ap', { scaleX: 1.15, scaleY: 0.86, duration: 0.07, transformOrigin: '50% 100%' }, 0.88);
tl.to('#m-ap', { scaleX: 1, scaleY: 1, duration: 0.4, ease: 'elastic.out(1,0.5)' }, 0.95);
[1.67, 2.44].forEach(function (t) {
  tl.to('#m-ap', { y: 200, duration: 0.17, ease: 'power2.out' }, t - 0.02);
  tl.to('#m-ap', { y: 240, duration: 0.18, ease: 'power2.in' }, t + 0.15);
});
apruviLife(tl, 'm-ap', 3.39, [1.2, 3.0]);
// g2: el mapa se atenúa; Apruvi grande sube y habla durante la pausa.
tl.to('#g1', { opacity: 0.28, scale: 0.97, duration: 0.35, ease: 'power2.out', transformOrigin: '50% 55%' }, 3.39);
tl.fromTo('#m-big', { y: 520 }, { y: 0, duration: 0.5, ease: 'back.out(1.6)' }, 3.39);
apruviLife(tl, 'm-big', 6.61, [5.0, 6.2]);
popIn(tl, '#m-bubble', 4.06, { scale: 0.6, y: 60, transformOrigin: '15% 100%' });
tl.fromTo('#m-big-arm-r', { rotation: 0 }, { rotation: -55, duration: 0.25, yoyo: true, repeat: 3, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 4.2);
""",
    WARM_BG,
)

# ------------------------------------------------------------------ 03 · racha (9,91–13,3 s)
# Locales: 0 subida · 0,96 golpe · 1,63 golpe · 2,61 fija · fin 3,39.
rays = "".join(
    f'<div class="ray" style="transform:rotate({i * 30}deg)"><i></i></div>' for i in range(12)
)
dots = "".join(
    f'<div class="dot" id="r-d{i}" data-layout-allow-overflow><span>{d}</span>{FLAME.format(attrs=f"class=dflame id=r-df{i}")}</div>'
    for i, d in enumerate(["L", "M", "M", "J", "V", "S", "D"])
)
nums = "".join(f'<span class="n" id="r-n{i}">{i}</span>' for i in range(1, 8))
f3 = frame(
    "03-racha",
    3.39,
    """
#03-racha #r-title { top: 300px; font-size: 100px; }
#03-racha #r-rays { position: absolute; left: 540px; top: 700px; width: 0; height: 0; }
#03-racha .ray { position: absolute; left: 0; top: 0; width: 0; height: 0; }
#03-racha .ray i { position: absolute; left: -9px; top: -460px; width: 18px; height: 150px; border-radius: 9px; background: #f97316; opacity: .5; }
#03-racha #r-flame { position: absolute; left: 380px; top: 470px; width: 320px; height: 400px; overflow: visible; }
#03-racha #r-num .n { position: absolute; left: 0; right: 0; opacity: 0; }
#03-racha #r-num { top: 900px; height: 340px; font-size: 330px; font-weight: 800; letter-spacing: -0.06em; font-variant-numeric: tabular-nums; }
#03-racha #r-lbl { top: 1220px; font-size: 64px; font-weight: 600; color: #5d6474; letter-spacing: -0.02em; }
#03-racha #r-week { position: absolute; left: 110px; right: 110px; top: 1330px; display: flex; justify-content: space-between; }
#03-racha .dot { position: relative; width: 104px; height: 104px; border-radius: 50%; background: #fff; border: 3px solid #e7e1d6; display: grid; place-items: center; }
#03-racha .dot span { position: absolute; bottom: -54px; font-size: 32px; font-weight: 600; color: #5d6474; }
#03-racha .dflame { width: 54px; height: 68px; opacity: 0; }
#03-racha #r-ap { left: -40px; top: 980px; width: 300px; height: 325px; }
""",
    f"""
<div id="r-rays">{rays}</div>
{FLAME.format(attrs='id="r-flame"')}
<div class="t" id="r-title">Rachas con fueguito</div>
<div class="t" id="r-num">{nums}</div>
<div class="t" id="r-lbl">días seguidos</div>
<div id="r-week">{dots}</div>
{apruvi("r-ap", 'data-layout-allow-overflow')}
""",
    """
// Subida: zoom brusco a la llama y rayos hacia afuera.
tl.fromTo('#r-flame', { scale: 3.2, opacity: 0.4 }, { scale: 1, opacity: 1, duration: 0.36, ease: 'expo.out', transformOrigin: '50% 80%' }, 0);
tl.fromTo('#r-rays .ray i', { scaleY: 0.2, opacity: 0.8 }, { scaleY: 1.4, opacity: 0, y: -160, duration: 0.7, ease: 'power3.out', transformOrigin: '50% 100%' }, 0);
tl.fromTo('#r-flame .fl-out', { scaleX: 1, scaleY: 1 }, { scaleX: 0.95, scaleY: 1.06, duration: 0.4, yoyo: true, repeat: 7, ease: 'sine.inOut', transformOrigin: '50% 100%' }, 0.36);
tl.fromTo('#r-flame .fl-in', { scaleX: 1, scaleY: 1 }, { scaleX: 1.05, scaleY: 0.94, duration: 0.28, yoyo: true, repeat: 10, ease: 'sine.inOut', transformOrigin: '50% 100%' }, 0.36);
popIn(tl, '#r-title', 0.08, { y: 30 });
popIn(tl, '#r-lbl', 0.3, { y: 20 });
popIn(tl, '#r-week', 0.3, { y: 30 });
popIn(tl, '#r-num', 0.12, { scale: 0.5 });
// Contador 1 → 7 entre los golpes (0,96 … 2,61); cada número enciende un día.
const steps = [0.96, 1.24, 1.5, 1.63, 1.98, 2.3, 2.61];
tl.set('#r-n1', { opacity: 1 }, 0);
steps.forEach(function (t, i) {
  if (i > 0) { tl.set('#r-n' + i, { opacity: 0 }, t); tl.set('#r-n' + (i + 1), { opacity: 1 }, t); }
  tl.fromTo('#r-num', { scale: 1.16 }, { scale: 1, duration: 0.22, ease: 'power3.out' }, t);
  tl.to('#r-d' + i, { backgroundColor: '#fff1e6', borderColor: '#f97316', duration: 0.12 }, t);
  tl.fromTo('#r-df' + i, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(3)' }, t);
});
// Fijación con golpe en 2,61 y rayos otra vez.
tl.fromTo('#r-num', { scale: 1.35, color: '#c2410c' }, { scale: 1, color: '#c2410c', duration: 0.45, ease: 'back.out(2.5)', immediateRender: false }, 2.61);
tl.fromTo('#r-rays .ray i', { scaleY: 0.2, opacity: 0.7, y: 0 }, { scaleY: 1.4, opacity: 0, y: -160, duration: 0.6, ease: 'power3.out', transformOrigin: '50% 100%', immediateRender: false }, 2.61);
// Apruvi asoma desde la izquierda en 1,63 y celebra.
tl.fromTo('#r-ap', { x: -320, rotation: -12 }, { x: 0, rotation: 0, duration: 0.42, ease: 'back.out(2)' }, 1.5);
tl.fromTo('#r-ap-arm-r', { rotation: 0 }, { rotation: -60, duration: 0.2, yoyo: true, repeat: 5, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 1.9);
apruviLife(tl, 'r-ap', 3.39, [2.9]);
""",
    "radial-gradient(circle at 50% 38%, #fff1e6 0%, #fdf1dc 42%, #fbf8f3 75%)",
)


# ------------------------------------------------------------------ 04 · oral (13,3–16,7 s)
# Locales: 0 · 0,8 · 1,72 · 2,51 · fin 3,4.
bars = "".join(f'<i id="o-b{i}" class="{"acc" if i == 4 else ""}"></i>' for i in range(9))
f4 = frame(
    "04-oral",
    3.4,
    """
#04-oral { color: #fff; }
#04-oral #o-title { top: 300px; font-size: 108px; color: #fff; }
#04-oral #o-sub { top: 545px; font-size: 54px; font-weight: 600; color: #cfdcff; letter-spacing: -0.01em; }
#04-oral #o-wave { position: absolute; left: 150px; right: 150px; top: 700px; height: 230px; display: flex; gap: 22px; align-items: center; }
#04-oral #o-wave i { flex: 1; height: 40%; border-radius: 30px; background: #fff; }
#04-oral #o-wave i.acc { background: #f5a524; }
#04-oral #o-timer { position: absolute; left: 50%; top: 975px; transform: translateX(-50%); display: flex; gap: 16px; align-items: center;
  background: rgba(255,255,255,.16); border: 2px solid rgba(255,255,255,.35); border-radius: 999px; padding: 14px 34px; font-size: 48px; font-weight: 700; font-variant-numeric: tabular-nums; }
#04-oral #o-time { position: relative; display: inline-block; width: 110px; height: 58px; }
#04-oral #o-time b { position: absolute; left: 0; top: 0; opacity: 0; }
#04-oral #o-disc { position: absolute; left: 240px; top: 1080px; width: 600px; height: 600px; border-radius: 50%; background: #fff;
  box-shadow: 0 0 0 34px rgba(255,255,255,.14), 0 0 0 70px rgba(255,255,255,.07); }
#04-oral #o-ap { left: 330px; top: 1120px; width: 420px; height: 455px; }
#04-oral #o-mic { position: absolute; left: 700px; top: 1300px; width: 110px; height: 180px; }
""",
    f"""
<div class="t" id="o-title">Simula tu<br>examen oral</div>
<div class="t" id="o-sub">con tiempos reales</div>
<div id="o-wave">{bars}</div>
<div id="o-timer"><svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><path d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18ZM12 7v5l3 2"/></svg><span id="o-time"><b id="o-t0">1:30</b><b id="o-t1">1:29</b><b id="o-t2">1:28</b><b id="o-t3">1:27</b></span></div>
<div id="o-disc"></div>
{apruvi("o-ap")}
<svg id="o-mic" viewBox="0 0 24 40"><rect x="6" y="2" width="12" height="20" rx="6" fill="#1f2430"/><path d="M3 16a9 9 0 0 0 18 0" stroke="#1f2430" stroke-width="2.6" fill="none" stroke-linecap="round"/><path d="M12 25v12" stroke="#1f2430" stroke-width="3" stroke-linecap="round"/></svg>
""",
    """
popIn(tl, '#o-title', 0, { y: 30 });
popIn(tl, '#o-sub', 0.8 - 0.1, { y: 20 });
tl.fromTo('#o-disc', { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(1.8)' }, 0);
tl.fromTo('#o-ap', { y: 160, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0.05);
tl.fromTo('#o-mic', { y: 160, opacity: 0, rotation: 20 }, { y: 0, opacity: 1, rotation: 0, duration: 0.45, ease: 'back.out(1.8)' }, 0.12);
apruviLife(tl, 'o-ap', 3.4, [1.3, 3.0]);
popIn(tl, '#o-timer', 0.2, { y: 20 });
// Barras de voz: un latido por pulso; alturas deterministas por índice.
const beats = [0, 0.8, 1.72, 2.51];
const shapes = [
  [55, 80, 100, 70, 95, 65, 85, 50, 40],
  [40, 70, 85, 100, 75, 90, 60, 80, 55],
  [60, 95, 70, 85, 100, 80, 65, 90, 45],
  [45, 65, 90, 75, 85, 100, 70, 60, 50],
];
beats.forEach(function (t, k) {
  for (let i = 0; i < 9; i++) {
    tl.fromTo('#o-b' + i, { height: shapes[k][i] + '%' }, { height: (shapes[k][i] * 0.35) + '%', duration: 0.7, ease: 'power2.out' }, t);
  }
  tl.fromTo('#o-ap', { scaleX: 1.08, scaleY: 0.93, transformOrigin: '50% 100%' }, { scaleX: 1, scaleY: 1, duration: 0.35, ease: 'elastic.out(1,0.5)' }, t);
});
// El temporizador corre un segundo por pulso.
tl.set('#o-t0', { opacity: 1 }, 0);
[1, 2, 3].forEach(function (k) {
  tl.set('#o-t' + (k - 1), { opacity: 0 }, beats[k]);
  tl.set('#o-t' + k, { opacity: 1 }, beats[k]);
});
""",
    "#2f5bd3",
)

# ------------------------------------------------------------------ 05 · cierre (16,7–21 s)
# Locales: 0 título · 0,78 botón · 3,2 marca + confeti · fin 4,3.
confetti = ""
colors = ["#2f5bd3", "#f5a524", "#067647", "#f97316", "#f7a8b8", "#2448ad"]
for i in range(30):
    c = colors[i % len(colors)]
    shape = "border-radius:50%" if i % 3 == 0 else "border-radius:4px"
    confetti += f'<i class="cf" id="c-p{i}" style="background:{c};{shape}"></i>'
f5 = frame(
    "05-cierre",
    4.3,
    """
#05-cierre #c-title { top: 300px; font-size: 100px; }
#05-cierre #c-title .b { color: #2f5bd3; }
#05-cierre #c-btn { position: absolute; left: 150px; right: 150px; top: 560px; text-align: center; background: #2f5bd3; color: #fff;
  font-size: 92px; font-weight: 800; letter-spacing: -0.03em; border-radius: 60px; padding: 46px 0; box-shadow: 0 18px 0 #2448ad, 0 40px 80px rgba(47,91,211,.3); overflow: hidden; }
#05-cierre #c-shine { position: absolute; top: 0; bottom: 0; left: -40%; width: 30%; background: linear-gradient(90deg, transparent, rgba(255,255,255,.45), transparent); transform: skewX(-20deg); }
#05-cierre #c-ap { left: 370px; top: 800px; width: 340px; height: 368px; }
#05-cierre #c-lock { position: absolute; left: 0; right: 0; top: 1230px; display: flex; gap: 26px; justify-content: center; align-items: center; font-size: 78px; font-weight: 700; letter-spacing: -0.03em; }
#05-cierre #c-logo { width: 120px; height: 120px; }
#05-cierre #c-url { top: 1385px; font-size: 58px; font-weight: 600; color: #2f5bd3; letter-spacing: -0.01em; }
#05-cierre .cf { position: absolute; left: 540px; top: 1260px; width: 26px; height: 16px; opacity: 0; }
""",
    f"""
<div class="t" id="c-title">Prepara tu examen<br><span class="b">con Apruvi</span></div>
<div id="c-btn" data-layout-allow-overflow>7 días gratis<div id="c-shine" data-layout-allow-overflow></div></div>
<div id="c-confetti">{confetti}</div>
{apruvi("c-ap")}
<div id="c-lock">{LOGO.format(attrs='id="c-logo"')}<span>Aprueba tu examen</span></div>
<div class="t" id="c-url">apruebatuexamen.cl</div>
""",
    """
popIn(tl, '#c-title', 0, { y: 30 });
tl.fromTo('#c-ap', { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: 'back.out(1.8)' }, 0.1);
apruviLife(tl, 'c-ap', 4.3, [1.6, 3.9]);
// Botón "7 días gratis" en 0,78 (entra antes para caer en el pulso) y brillo durante la pausa.
popIn(tl, '#c-btn', 0.66, { scale: 0.5, y: 80 });
tl.fromTo('#c-shine', { x: 0 }, { x: 1250, duration: 0.9, ease: 'power2.inOut' }, 1.6);
// Golpe final 3,2: marca + URL + confeti; Apruvi salta y saluda.
tl.set(['#c-lock', '#c-url'], { opacity: 0 }, 0);
popIn(tl, '#c-lock', 3.12, { scale: 0.6, y: 60 });
popIn(tl, '#c-url', 3.3, { y: 30 });
tl.to('#c-ap', { y: -70, duration: 0.18, ease: 'power2.out' }, 3.12);
tl.to('#c-ap', { y: 0, duration: 0.3, ease: 'bounce.out' }, 3.31);
tl.fromTo('#c-ap-arm-r', { rotation: 0 }, { rotation: -60, duration: 0.18, yoyo: true, repeat: 5, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 3.3);
for (let i = 0; i < 30; i++) {
  const a = (i / 30) * Math.PI * 2 + (i % 2) * 0.2;
  const r = 380 + (i % 5) * 70;
  const dx = Math.cos(a) * r;
  const dy = Math.sin(a) * r * 0.75 - 220;
  tl.set('#c-p' + i, { opacity: 1, x: 0, y: 0, rotation: 0 }, 3.18);
  tl.to('#c-p' + i, { x: dx, y: dy, rotation: (i % 2 ? 1 : -1) * (200 + i * 12), duration: 0.6, ease: 'power3.out' }, 3.18);
  tl.to('#c-p' + i, { y: dy + 420, opacity: 0, duration: 0.85, ease: 'power1.in' }, 3.78);
}
""",
    WARM_BG,
)

for name, html in [
    ("01-intro", f1),
    ("02-mapa", f2),
    ("03-racha", f3),
    ("04-oral", f4),
    ("05-cierre", f5),
]:
    (OUT / f"{name}.html").write_text(html, encoding="utf-8")
    print("escrito", name)

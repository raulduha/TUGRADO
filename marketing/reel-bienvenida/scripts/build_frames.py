"""Escenas del video de bienvenida (plan en STORYBOARD.md). Ejecutar desde la raíz del proyecto:
    python scripts/build_frames.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))

from hf_kit import FLAME, ICONS, LOGO, W, H, WARM_BG, apruvi, frame, write  # noqa: E402

BUBBLE_CSS = """
#{fid} .bubble {{ position: absolute; background: #fff; border: 3px solid #e7e1d6; border-radius: 56px;
  padding: 36px 48px; font-size: 76px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.05;
  box-shadow: 0 30px 70px rgba(31,36,48,.12); text-align: center; }}
"""


def confetti(prefix: str, n: int = 28) -> str:
    colors = ["#2f5bd3", "#f5a524", "#067647", "#f97316", "#f7a8b8", "#2448ad"]
    out = ""
    for i in range(n):
        shape = "border-radius:50%" if i % 3 == 0 else "border-radius:4px"
        out += f'<i class="cf" id="{prefix}{i}" style="background:{colors[i % len(colors)]};{shape}"></i>'
    return out


CONFETTI_JS = """
function burst(tl, prefix, n, t, cx, cy) {
  for (let i = 0; i < n; i++) {
    const a = (i / n) * Math.PI * 2 + (i % 2) * 0.2;
    const r = 340 + (i % 5) * 70;
    const dx = Math.cos(a) * r, dy = Math.sin(a) * r * 0.75 - 200;
    tl.set('#' + prefix + i, { opacity: 1, x: 0, y: 0, rotation: 0, left: cx, top: cy }, t);
    tl.to('#' + prefix + i, { x: dx, y: dy, rotation: (i % 2 ? 1 : -1) * (200 + i * 12), duration: 0.55, ease: 'power3.out' }, t);
    tl.to('#' + prefix + i, { y: dy + 380, opacity: 0, duration: 0.8, ease: 'power1.in' }, t + 0.55);
  }
}
"""

# ------------------------------------------------------------- 01 · hola (0–3,39)
write("01-hola", frame(
    "01-hola", 3.39,
    BUBBLE_CSS.format(fid="01-hola") + """
#01-hola #h-ap { left: 250px; top: 760px; width: 580px; height: 628px; }
#01-hola #h-bubble { left: 120px; right: 120px; top: 330px; }
#01-hola #h-welcome { top: 1410px; font-size: 84px; }
#01-hola #h-welcome .b { color: #2f5bd3; }
""",
    f"""
{apruvi("h-ap")}
<div class="bubble" id="h-bubble">¡Hola! Soy Apruvi</div>
<div class="t" id="h-welcome">Te damos la <span class="b">bienvenida</span></div>
""",
    """
tl.fromTo('#h-ap', { scale: 0.4, opacity: 0, transformOrigin: '50% 100%' }, { scale: 1, opacity: 1, duration: 0.6, ease: 'back.out(1.8)' }, 0.25);
apruviLife(tl, 'h-ap', 3.39, [2.2]);
tl.fromTo('#h-ap-arm-r', { rotation: 0 }, { rotation: -60, duration: 0.22, yoyo: true, repeat: 5, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 0.8);
popIn(tl, '#h-bubble', 1.81 - 0.12, { scale: 0.6, y: 60 });
popIn(tl, '#h-welcome', 2.6 - 0.12, { y: 50 });
""",
    WARM_BG,
))

# ------------------------------------------------------------- 02 · mapa (3,39–7,57)
# Locales: 0 corte · 1,02 · 1,63 · 2,60 · 3,39 nodos.
N = [(540, 720), (780, 960), (330, 1200), (600, 1420)]
path_d = (
    f"M {N[0][0]} {N[0][1]} C {N[0][0]} 840, {N[1][0]} 840, {N[1][0]} {N[1][1]} "
    f"C {N[1][0]} 1080, {N[2][0]} 1080, {N[2][0]} {N[2][1]} "
    f"C {N[2][0]} 1320, {N[3][0]} 1320, {N[3][0]} {N[3][1]}"
)
styles = [("#067647", "#05603a", "check", "#fff"), ("#2f5bd3", "#2448ad", "list", "#fff"),
          ("#ece7de", "#d6cfc2", "lock", "#5d6474"), ("#ece7de", "#d6cfc2", "cap", "#5d6474")]
nodes = "".join(
    f'<div class="node" id="m-n{i}" style="left:{x - 80}px;top:{y - 80}px;background:{bg};border-bottom-color:{bd}">'
    f'<svg viewBox="0 0 24 24" width="76" height="76" fill="none" stroke="{ink}" stroke-width="2.6" '
    f'stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[icon]}"/></svg></div>'
    for i, ((x, y), (bg, bd, icon, ink)) in enumerate(zip(N, styles))
)
write("02-mapa", frame(
    "02-mapa", 4.18,
    """
#02-mapa #m-title { top: 300px; font-size: 90px; }
#02-mapa #m-sub { top: 405px; font-size: 52px; font-weight: 600; color: #2f5bd3; }
#02-mapa .node { position: absolute; width: 160px; height: 160px; border-radius: 50%; border-bottom: 16px solid; display: grid; place-items: center; }
#02-mapa #m-ap { left: 0; top: 0; width: 230px; height: 249px; }
""",
    f"""
<div class="t" id="m-title">Tu mapa de estudio</div>
<div class="t" id="m-sub">nivel a nivel</div>
<svg class="layer" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <path id="m-path" d="{path_d}" fill="none" stroke="#e7e1d6" stroke-width="44" stroke-linecap="round"/>
</svg>
{nodes}
{apruvi("m-ap")}
""",
    f"""
popIn(tl, '#m-title', 0, {{ y: 30 }});
popIn(tl, '#m-sub', 0.25, {{ y: 20 }});
const path = document.querySelector('#m-path');
const len = path.getTotalLength();
tl.set('#m-path', {{ strokeDasharray: len, strokeDashoffset: len }}, 0);
tl.to('#m-path', {{ strokeDashoffset: 0, duration: 3.39, ease: 'none' }}, 0);
const beats = [1.02, 1.63, 2.6, 3.39];
const pts = {json.dumps([list(p) for p in N])};
beats.forEach(function (t, i) {{
  tl.fromTo('#m-n' + i, {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: 0.42, ease: 'back.out(2.4)' }}, t - 0.1);
}});
// Apruvi salta de nodo en nodo (se para a la derecha de cada nodo).
tl.set('#m-ap', {{ x: pts[0][0] + 70, y: pts[0][1] - 230 }}, 0);
for (let i = 1; i < 4; i++) {{
  const t = beats[i] - 0.4;
  tl.to('#m-ap', {{ x: pts[i][0] + 70, duration: 0.4, ease: 'power1.inOut' }}, t);
  tl.to('#m-ap', {{ y: pts[i][1] - 380, duration: 0.2, ease: 'power2.out' }}, t);
  tl.to('#m-ap', {{ y: pts[i][1] - 230, duration: 0.2, ease: 'power2.in' }}, t + 0.2);
}}
apruviLife(tl, 'm-ap', 4.18, [3.8]);
""",
    WARM_BG,
))

# --------------------------------------------------------- 03 · práctica (7,57–10,96)
# Locales: 0 tarjeta · 0,93 · 1,63 golpe (verde) · 2,6 voz.
opts = [("A", "Desde la concepción"), ("B", "Al nacer"), ("C", "Al inscribirse")]
cards = "".join(
    f'<div class="opt" id="p-o{i}"><span class="l">{letter}</span>{text}</div>'
    for i, (letter, text) in enumerate(opts)
)
bars = "".join(f'<i id="p-b{i}" class="{"acc" if i == 3 else ""}"></i>' for i in range(7))
write("03-practica", frame(
    "03-practica", 3.39,
    """
#03-practica #p-title { top: 300px; font-size: 104px; line-height: 0.98; }
#03-practica #p-title .b { color: #2f5bd3; }
#03-practica #p-opts { position: absolute; left: 100px; right: 100px; top: 600px; display: flex; flex-direction: column; gap: 26px; }
#03-practica .opt { display: flex; align-items: center; gap: 26px; background: #fff; border: 4px solid #e7e1d6; border-bottom-width: 10px;
  border-radius: 36px; padding: 30px 36px; font-size: 54px; font-weight: 600; }
#03-practica .opt .l { width: 74px; height: 74px; border-radius: 18px; border: 4px solid #e7e1d6; display: grid; place-items: center; font-size: 40px; color: #5d6474; }
#03-practica #p-voice { position: absolute; left: 110px; right: 290px; top: 1190px; height: 200px; display: flex; gap: 20px; align-items: center; opacity: 0; }
#03-practica #p-voice i { flex: 1; height: 30%; border-radius: 30px; background: #2f5bd3; }
#03-practica #p-voice i.acc { background: #f5a524; }
#03-practica #p-ap { left: 850px; top: 1230px; width: 190px; height: 206px; }
""",
    f"""
<div class="t" id="p-title">Practica<br><span class="b">y simula el oral</span></div>
<div id="p-opts">{cards}</div>
<div id="p-voice">{bars}</div>
{apruvi("p-ap")}
""",
    """
popIn(tl, '#p-title', 0, { y: 30 });
[0, 1, 2].forEach(function (i) { popIn(tl, '#p-o' + i, 0.05 + i * 0.12, { x: -80, y: 0 }); });
// Golpe 1,63: la B se pone verde.
tl.to('#p-o1', { borderColor: '#067647', backgroundColor: '#e7f6ee', duration: 0.12 }, 1.6);
tl.fromTo('#p-o1', { scale: 1.08 }, { scale: 1, duration: 0.35, ease: 'back.out(3)', immediateRender: false }, 1.63);
tl.to('#p-o1 .l', { backgroundColor: '#067647', borderColor: '#067647', color: '#fff', duration: 0.12 }, 1.6);
// 2,6: la voz late junto a Apruvi.
tl.to('#p-voice', { opacity: 1, duration: 0.2 }, 2.5);
const shapes = [[60, 90, 70, 100, 80, 95, 55], [45, 70, 100, 85, 95, 60, 75]];
[2.6, 3.0].forEach(function (t, k) {
  for (let i = 0; i < 7; i++) {
    tl.fromTo('#p-b' + i, { height: shapes[k][i] + '%' }, { height: (shapes[k][i] * 0.35) + '%', duration: 0.38, ease: 'power2.out', immediateRender: false }, t);
  }
});
tl.fromTo('#p-ap', { y: 260 }, { y: 0, duration: 0.45, ease: 'back.out(1.8)' }, 0.2);
apruviLife(tl, 'p-ap', 3.39, [1.2]);
""",
    WARM_BG,
))

# ------------------------------------------------------------ 04 · racha (10,96–14,35)
# Locales: 0 llama · 0,77 · 1,72 · 2,42 fija.
rays = "".join(f'<div class="ray" style="transform:rotate({i * 30}deg)"><i></i></div>' for i in range(12))
nums = "".join(f'<span class="n" id="r-n{i}">{i}</span>' for i in range(1, 8))
dots = "".join(
    f'<div class="dot" id="r-d{i}" data-layout-allow-overflow><span>{d}</span>'
    f'{FLAME.format(attrs=f"class=dflame id=r-df{i}")}</div>'
    for i, d in enumerate(["L", "M", "M", "J", "V", "S", "D"])
)
write("04-racha", frame(
    "04-racha", 3.39,
    """
#04-racha #r-title { top: 300px; font-size: 104px; }
#04-racha #r-rays { position: absolute; left: 540px; top: 680px; width: 0; height: 0; }
#04-racha .ray { position: absolute; left: 0; top: 0; }
#04-racha .ray i { position: absolute; left: -9px; top: -440px; width: 18px; height: 140px; border-radius: 9px; background: #f97316; opacity: .5; }
#04-racha #r-flame { position: absolute; left: 390px; top: 460px; width: 300px; height: 375px; overflow: visible; }
#04-racha #r-num { top: 880px; height: 340px; font-size: 330px; font-weight: 800; letter-spacing: -0.06em; color: #c2410c; }
#04-racha #r-num .n { position: absolute; left: 0; right: 0; opacity: 0; }
#04-racha #r-lbl { top: 1210px; font-size: 64px; font-weight: 600; color: #5d6474; }
#04-racha #r-week { position: absolute; left: 110px; right: 110px; top: 1320px; display: flex; justify-content: space-between; }
#04-racha .dot { position: relative; width: 104px; height: 104px; border-radius: 50%; background: #fff; border: 3px solid #e7e1d6; display: grid; place-items: center; }
#04-racha .dot span { position: absolute; bottom: -52px; font-size: 32px; font-weight: 600; color: #5d6474; }
#04-racha .dflame { width: 54px; height: 68px; opacity: 0; }
""",
    f"""
<div id="r-rays">{rays}</div>
{FLAME.format(attrs='id="r-flame"')}
<div class="t" id="r-title">Cuida tu racha</div>
<div class="t" id="r-num">{nums}</div>
<div class="t" id="r-lbl">días seguidos</div>
<div id="r-week">{dots}</div>
""",
    """
tl.fromTo('#r-flame', { scale: 3, opacity: 0.4 }, { scale: 1, opacity: 1, duration: 0.36, ease: 'expo.out', transformOrigin: '50% 80%' }, 0);
tl.fromTo('#r-rays .ray i', { scaleY: 0.2, opacity: 0.8 }, { scaleY: 1.4, opacity: 0, y: -160, duration: 0.7, ease: 'power3.out', transformOrigin: '50% 100%' }, 0);
tl.fromTo('#r-flame .fl-out', { scaleX: 1, scaleY: 1 }, { scaleX: 0.95, scaleY: 1.06, duration: 0.4, yoyo: true, repeat: 7, ease: 'sine.inOut', transformOrigin: '50% 100%' }, 0.36);
popIn(tl, '#r-title', 0.06, { y: 30 });
popIn(tl, '#r-lbl', 0.25, { y: 20 });
popIn(tl, '#r-week', 0.25, { y: 30 });
const steps = [0.2, 0.77, 1.1, 1.42, 1.72, 2.05, 2.42];
tl.set('#r-n1', { opacity: 1 }, 0);
steps.forEach(function (t, i) {
  if (i > 0) { tl.set('#r-n' + i, { opacity: 0 }, t); tl.set('#r-n' + (i + 1), { opacity: 1 }, t); }
  tl.to('#r-d' + i, { backgroundColor: '#fff1e6', borderColor: '#f97316', duration: 0.12 }, t);
  tl.fromTo('#r-df' + i, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(3)' }, t);
});
tl.fromTo('#r-num', { scale: 1.35 }, { scale: 1, duration: 0.45, ease: 'back.out(2.5)', immediateRender: false }, 2.42);
tl.fromTo('#r-rays .ray i', { scaleY: 0.2, opacity: 0.7, y: 0 }, { scaleY: 1.4, opacity: 0, y: -160, duration: 0.6, ease: 'power3.out', transformOrigin: '50% 100%', immediateRender: false }, 2.42);
""",
    "radial-gradient(circle at 50% 36%, #fff1e6 0%, #fdf1dc 42%, #fbf8f3 75%)",
))

# ----------------------------------------------------------- 05 · empieza (14,35–16,91)
# Locales: 0 botón · 0,77 · 1,56 marca.
write("05-empieza", frame(
    "05-empieza", 2.56,
    """
#05-empieza #e-btn { position: absolute; left: 130px; right: 130px; top: 330px; text-align: center; background: #2f5bd3; color: #fff;
  font-size: 92px; font-weight: 800; letter-spacing: -0.03em; line-height: 1.02; border-radius: 60px; padding: 50px 0;
  box-shadow: 0 18px 0 #2448ad, 0 40px 80px rgba(47,91,211,.3); }
#05-empieza #e-ap { left: 380px; top: 720px; width: 320px; height: 347px; }
#05-empieza #e-lock { position: absolute; left: 0; right: 0; top: 1150px; display: flex; gap: 26px; justify-content: center; align-items: center; font-size: 78px; font-weight: 700; letter-spacing: -0.03em; }
#05-empieza #e-logo { width: 120px; height: 120px; }
#05-empieza #e-url { top: 1300px; font-size: 58px; font-weight: 600; color: #2f5bd3; }
#05-empieza .cf { position: absolute; width: 26px; height: 16px; opacity: 0; }
""",
    f"""
<div id="e-confetti">{confetti("e-c")}</div>
<div id="e-btn">Empieza tus<br>7 días gratis</div>
{apruvi("e-ap")}
<div id="e-lock">{LOGO.format(attrs='id="e-logo"')}<span>Aprueba tu examen</span></div>
<div class="t" id="e-url">apruebatuexamen.cl</div>
""",
    CONFETTI_JS + """
popIn(tl, '#e-btn', 0, { scale: 0.5, y: 80 });
tl.fromTo('#e-ap', { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0.1);
apruviLife(tl, 'e-ap', 2.56, [1.0]);
tl.fromTo('#e-ap-arm-r', { rotation: 0 }, { rotation: -60, duration: 0.18, yoyo: true, repeat: 5, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 0.6);
tl.set(['#e-lock', '#e-url'], { opacity: 0 }, 0);
popIn(tl, '#e-lock', 1.48, { scale: 0.6, y: 60 });
popIn(tl, '#e-url', 1.62, { y: 30 });
burst(tl, 'e-c', 28, 1.52, 540, 1200);
""",
    WARM_BG,
))

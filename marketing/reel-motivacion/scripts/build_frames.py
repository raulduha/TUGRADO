"""Escenas del video de motivación (plan en STORYBOARD.md). Ejecutar desde la raíz del proyecto:
    python scripts/build_frames.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))

from hf_kit import FLAME, LOGO, WARM_BG, apruvi, frame, write  # noqa: E402

SOFT_BG = "linear-gradient(180deg, #eef1fa 0%, #fbf8f3 60%, #f7efe2 100%)"
WARM_GLOW = "radial-gradient(circle at 50% 30%, #fff1e6 0%, #fdf1dc 42%, #fbf8f3 75%)"

# ---------------------------------------------------------- 01 · pregunta (0–3,3)
write("01-pregunta", frame(
    "01-pregunta", 3.3,
    """
#01-pregunta #q-text { top: 320px; font-size: 118px; line-height: 1.0; }
#01-pregunta #q-l2 { color: #2f5bd3; }
#01-pregunta #q-ap { left: 200px; top: 900px; width: 470px; height: 509px; }
#01-pregunta #q-flame { position: absolute; left: 720px; top: 1180px; width: 150px; height: 188px; filter: grayscale(1); opacity: .45; }
""",
    f"""
<div class="t" id="q-text"><div id="q-l1">¿Un par de días</div><div id="q-l2">sin estudiar?</div></div>
{apruvi("q-ap")}
{FLAME.format(attrs='id="q-flame"')}
""",
    """
// Ritmo de frase: entradas lentas, sin golpes.
tl.fromTo('#q-ap', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.9, ease: 'power2.out' }, 0);
tl.fromTo('#q-flame', { opacity: 0 }, { opacity: 0.45, duration: 0.9, ease: 'power1.out' }, 0.2);
apruviLife(tl, 'q-ap', 3.3, [2.6]);
tl.fromTo('#q-l1', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }, 1.04 - 0.2);
tl.fromTo('#q-l2', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }, 1.81 - 0.2);
// Apruvi inclina la cabeza, pensativo.
tl.to('#q-ap', { rotation: -6, duration: 1.2, ease: 'sine.inOut', transformOrigin: '50% 100%' }, 1.6);
""",
    SOFT_BG,
))

# ----------------------------------------------------------- 02 · espera (3,3–6,66)
# Locales: 0 · 0,86 globo · 2,44 anticipación · fin 3,36.
write("02-espera", frame(
    "02-espera", 3.36,
    """
#02-espera #w-ap { left: 260px; top: 780px; width: 560px; height: 606px; }
#02-espera #w-bubble { position: absolute; left: 110px; right: 110px; top: 360px; background: #fff; border: 3px solid #e7e1d6; border-radius: 56px;
  padding: 44px 40px; font-size: 92px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.02; text-align: center;
  box-shadow: 0 30px 70px rgba(31,36,48,.12); }
#02-espera #w-bubble .b { color: #2f5bd3; }
#02-espera #w-flame { position: absolute; left: 820px; top: 1210px; width: 130px; height: 163px; filter: grayscale(1); opacity: .45; }
""",
    f"""
{apruvi("w-ap")}
{FLAME.format(attrs='id="w-flame"')}
<div id="w-bubble">Te estoy<br><span class="b">esperando</span></div>
""",
    """
apruviLife(tl, 'w-ap', 3.36, [1.6]);
tl.fromTo('#w-ap', { y: 40 }, { y: 0, duration: 0.6, ease: 'power2.out' }, 0);
popIn(tl, '#w-bubble', 0.86 - 0.15, { scale: 0.6, y: 60, transformOrigin: '50% 100%' });
// Saludo con el brazo mientras habla.
tl.fromTo('#w-ap-arm-r', { rotation: 0 }, { rotation: -55, duration: 0.3, yoyo: true, repeat: 3, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 1.0);
// Anticipación antes de la subida: se agacha.
tl.to('#w-ap', { scaleX: 1.08, scaleY: 0.9, duration: 0.5, ease: 'power2.in', transformOrigin: '50% 100%' }, 2.8);
""",
    SOFT_BG,
))

# ----------------------------------------------------------- 03 · ratito (6,66–9,89)
# Locales: 0 subida · 0,7 golpe · 1,68 · 2,46 saltos · fin 3,23.
rays = "".join(f'<div class="ray" style="transform:rotate({i * 30}deg)"><i></i></div>' for i in range(12))
write("03-ratito", frame(
    "03-ratito", 3.23,
    """
#03-ratito #t-rays { position: absolute; left: 540px; top: 640px; width: 0; height: 0; }
#03-ratito .ray { position: absolute; left: 0; top: 0; }
#03-ratito .ray i { position: absolute; left: -9px; top: -430px; width: 18px; height: 140px; border-radius: 9px; background: #f97316; opacity: .5; }
#03-ratito #t-flame { position: absolute; left: 380px; top: 360px; width: 320px; height: 400px; overflow: visible; }
#03-ratito #t-text { top: 860px; font-size: 118px; line-height: 1.0; }
#03-ratito #t-text .b { color: #2f5bd3; }
#03-ratito #t-ap { left: 400px; top: 1210px; width: 280px; height: 303px; }
""",
    f"""
<div id="t-rays">{rays}</div>
{FLAME.format(attrs='id="t-flame"')}
<div class="t" id="t-text">Un ratito hoy<br><span class="b">ya cuenta</span></div>
{apruvi("t-ap")}
""",
    """
tl.fromTo('#t-flame', { scale: 0.2, opacity: 0.3, filter: 'grayscale(1)' }, { scale: 1, opacity: 1, filter: 'grayscale(0)', duration: 0.4, ease: 'back.out(2.2)', transformOrigin: '50% 90%' }, 0);
tl.fromTo('#t-rays .ray i', { scaleY: 0.2, opacity: 0.8 }, { scaleY: 1.4, opacity: 0, y: -160, duration: 0.7, ease: 'power3.out', transformOrigin: '50% 100%' }, 0);
tl.fromTo('#t-flame .fl-out', { scaleX: 1, scaleY: 1 }, { scaleX: 0.95, scaleY: 1.06, duration: 0.4, yoyo: true, repeat: 6, ease: 'sine.inOut', transformOrigin: '50% 100%' }, 0.4);
popIn(tl, '#t-text', 0.7 - 0.12, { scale: 0.7, y: 60 });
tl.fromTo('#t-ap', { y: 220, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0.1);
apruviLife(tl, 't-ap', 3.23, [1.2]);
[1.68, 2.46].forEach(function (t) {
  tl.to('#t-ap', { y: -55, duration: 0.18, ease: 'power2.out' }, t - 0.02);
  tl.to('#t-ap', { y: 0, duration: 0.2, ease: 'power2.in' }, t + 0.16);
});
""",
    WARM_GLOW,
))

# ------------------------------------------------------------ 04 · vuelve (9,89–13)
# Locales: 0 · 0,79 · 1,65 golpe · fin 3,11.
dots = "".join(
    f'<div class="dot" id="v-d{i}">{FLAME.format(attrs=f"class=dflame id=v-df{i}")}</div>' for i in range(7)
)
colors = ["#2f5bd3", "#f5a524", "#067647", "#f97316", "#f7a8b8", "#2448ad"]
confetti = "".join(
    f'<i class="cf" id="v-c{i}" style="background:{colors[i % 6]};'
    f'{"border-radius:50%" if i % 3 == 0 else "border-radius:4px"}"></i>'
    for i in range(28)
)
write("04-vuelve", frame(
    "04-vuelve", 3.11,
    """
#04-vuelve #v-title { top: 300px; font-size: 96px; line-height: 1.0; }
#04-vuelve #v-title .b { color: #c2410c; }
#04-vuelve #v-week { position: absolute; left: 110px; right: 110px; top: 560px; display: flex; justify-content: space-between; }
#04-vuelve .dot { width: 104px; height: 104px; border-radius: 50%; background: #fff; border: 3px solid #e7e1d6; display: grid; place-items: center; }
#04-vuelve .dflame { width: 54px; height: 68px; opacity: 0; }
#04-vuelve #v-ap { left: 395px; top: 740px; width: 290px; height: 314px; }
#04-vuelve #v-lock { position: absolute; left: 0; right: 0; top: 1150px; display: flex; gap: 26px; justify-content: center; align-items: center; font-size: 78px; font-weight: 700; letter-spacing: -0.03em; }
#04-vuelve #v-logo { width: 120px; height: 120px; }
#04-vuelve #v-url { top: 1300px; font-size: 58px; font-weight: 600; color: #2f5bd3; }
#04-vuelve .cf { position: absolute; left: 540px; top: 1200px; width: 26px; height: 16px; opacity: 0; }
""",
    f"""
<div id="v-confetti">{confetti}</div>
<div class="t" id="v-title">Vuelve a encender<br><span class="b">tu racha</span></div>
<div id="v-week">{dots}</div>
{apruvi("v-ap")}
<div id="v-lock">{LOGO.format(attrs='id="v-logo"')}<span>Aprueba tu examen</span></div>
<div class="t" id="v-url">apruebatuexamen.cl</div>
""",
    """
popIn(tl, '#v-title', 0, { y: 30 });
popIn(tl, '#v-week', 0.1, { y: 30 });
// La semana se enciende día a día entre 0 y 0,79.
for (let i = 0; i < 7; i++) {
  const t = 0.12 + i * 0.11;
  tl.to('#v-d' + i, { backgroundColor: '#fff1e6', borderColor: '#f97316', duration: 0.1 }, t);
  tl.fromTo('#v-df' + i, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: 'back.out(3)' }, t);
}
tl.fromTo('#v-ap', { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: 'back.out(1.8)' }, 0.2);
apruviLife(tl, 'v-ap', 3.11, [2.6]);
// Golpe 1,65: marca con confeti; Apruvi salta y saluda.
tl.set(['#v-lock', '#v-url'], { opacity: 0 }, 0);
popIn(tl, '#v-lock', 1.57, { scale: 0.6, y: 60 });
popIn(tl, '#v-url', 1.72, { y: 30 });
tl.to('#v-ap', { y: -60, duration: 0.18, ease: 'power2.out' }, 1.57);
tl.to('#v-ap', { y: 0, duration: 0.3, ease: 'bounce.out' }, 1.76);
tl.fromTo('#v-ap-arm-r', { rotation: 0 }, { rotation: -60, duration: 0.18, yoyo: true, repeat: 5, ease: 'sine.inOut', transformOrigin: '10% 10%' }, 1.8);
for (let i = 0; i < 28; i++) {
  const a = (i / 28) * Math.PI * 2 + (i % 2) * 0.2;
  const r = 340 + (i % 5) * 70;
  const dx = Math.cos(a) * r, dy = Math.sin(a) * r * 0.75 - 200;
  tl.set('#v-c' + i, { opacity: 1, x: 0, y: 0, rotation: 0 }, 1.62);
  tl.to('#v-c' + i, { x: dx, y: dy, rotation: (i % 2 ? 1 : -1) * (200 + i * 12), duration: 0.55, ease: 'power3.out' }, 1.62);
  tl.to('#v-c' + i, { y: dy + 380, opacity: 0, duration: 0.8, ease: 'power1.in' }, 2.17);
}
""",
    WARM_BG,
))

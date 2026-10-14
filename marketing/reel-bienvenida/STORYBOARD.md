---
compositionId: bgm
duration_s: 16.91
canvas: {"w": 1080, "h": 1920, "fps": 30}
style:
  font: "Geist"
  palette: ["#fbf8f3", "#1f2430", "#2f5bd3", "#f5a524", "#067647", "#f97316"]
assets: "assets/fonts/Geist-latin.woff2; Apruvi inline SVG (marketing/shared/hf_kit.py)"
build_notes: ["one paused timeline per frame", "no remote assets", "brand from frame.md", "Reels safe zones: top 288px / bottom 384px"]
avoid: ["dark backgrounds", "promising to pass the exam", "emoji"]
---

Track read: "Wake up" 99.54–116.45 s. Calm intro (0–3), SURGE at 3 with hits 4.41 / 5.02, high to 8, medium, high 10–13 with hit 13.38, surge again at 16, 1 s fade-out. Bars at 4.34 · 7.57 · 10.96 · 14.35.

## Frame 1 — hola

- src: compositions/frames/01-hola.html
- duration: 3.39s
- span_sec: [0.0, 3.39]
- pacing: phrase_flow
- mood: [warm, playful]
- feel: calm near-silent intro with soft onsets before the surge at 3

### Groups

- **g1** — free_design
  - span_sec: [0.0, 3.39]
  - free_design: { dominant_system: "Apruvi waves hello and introduces himself", primitives: ["overlay-pop", "kinetic-letter-in"], density_topology: "accumulate" }
  - anchors: [0.4, 1.81, 2.6]
  - copy: ["¡Hola! Soy Apruvi", "Te damos la bienvenida"]
  - notes: bg-warm. Apruvi (big, center) pops in and waves; speech bubble "¡Hola! Soy Apruvi" on 1.81; line "Te damos la bienvenida" under it on 2.6. Calm, no hard hits.

## Frame 2 — mapa

- src: compositions/frames/02-mapa.html
- duration: 4.18s
- span_sec: [3.39, 7.57]
- pacing: beat_cut
- mood: [hype, playful]
- feel: the SURGE at 3–4 with strong hits at 4.41 and 5.02, high energy on steady beats

### Groups

- **g1** — free_design
  - span_sec: [3.39, 7.57]
  - free_design: { dominant_system: "study map path drawing node by node", primitives: ["directional-fill", "overlay-pop"], density_topology: "accumulate" }
  - anchors: [3.39, 4.41, 5.02, 5.99, 6.78]
  - copy: ["Tu mapa de estudio", "nivel a nivel"]
  - notes: Hard cut in on 3.39. Path draws downward, a node pops per hit/beat (4.41, 5.02, 5.99, 6.78); Apruvi hops along.

## Frame 3 — practica

- src: compositions/frames/03-practica.html
- duration: 3.39s
- span_sec: [7.57, 10.96]
- pacing: beat_cut
- mood: [playful]
- feel: medium bar after a drop at 7–8, strong hit at 9.2, surge at 10

### Groups

- **g1** — free_design
  - span_sec: [7.57, 10.96]
  - free_design: { dominant_system: "answer card checks green, then mic waveform", primitives: ["overlay-pop", "content-swap"], density_topology: "swap" }
  - anchors: [7.57, 8.5, 9.2, 10.17]
  - copy: ["Practica", "y simula el oral"]
  - notes: An alternatives card (A/B/C) pops on 7.57; option B turns green with a check on 9.2; on 10.17 a voice waveform pulses beside a mic. Title words land on 7.57 / 8.5.

## Frame 4 — racha

- src: compositions/frames/04-racha.html
- duration: 3.39s
- span_sec: [10.96, 14.35]
- pacing: beat_cut
- mood: [hype, warm]
- feel: high energy 10–13 with the strong hit at 13.38

### Groups

- **g1** — free_design
  - span_sec: [10.96, 14.35]
  - free_design: { dominant_system: "flame + day counter climbing to a lock", primitives: ["counting-punch", "radial-burst-lines"], density_topology: "build-then-lock" }
  - anchors: [10.96, 11.73, 12.68, 13.38]
  - copy: ["Cuida tu racha", "días seguidos"]
  - notes: Flame bursts in on 10.96; counter 1 → 7 locking with a punch on 13.38; week dots light up.

## Frame 5 — empieza

- src: compositions/frames/05-empieza.html
- duration: 2.56s
- span_sec: [14.35, 16.91]
- pacing: beat_cut
- mood: [warm, cinematic]
- feel: medium/low bar with a final surge at 16 and a 1 s fade-out

### Groups

- **g1** — free_design
  - span_sec: [14.35, 16.91]
  - free_design: { dominant_system: "CTA button then brand lockup", primitives: ["overlay-pop", "particle-burst"], density_topology: "hold-then-sting" }
  - anchors: [14.35, 15.12, 15.91]
  - copy: ["Empieza tus 7 días gratis", "apruebatuexamen.cl"]
  - notes: Button "Empieza tus 7 días gratis" pops on 14.35; Apruvi waves; lockup (logo + "Aprueba tu examen" + URL) lands on 15.91 with confetti; hold through the fade.

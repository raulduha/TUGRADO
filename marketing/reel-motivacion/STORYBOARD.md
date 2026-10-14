---
compositionId: bgm
duration_s: 13.0
canvas: {"w": 1080, "h": 1920, "fps": 30}
style:
  font: "Geist"
  palette: ["#fbf8f3", "#1f2430", "#2f5bd3", "#f5a524", "#067647", "#f97316"]
assets: "assets/fonts/Geist-latin.woff2; Apruvi inline SVG (marketing/shared/hf_kit.py)"
build_notes: ["one paused timeline per frame", "no remote assets", "brand from frame.md", "Reels safe zones: top 288px / bottom 384px"]
avoid: ["dark backgrounds", "guilt-tripping", "promising to pass the exam", "emoji"]
---

Track read: "Wake up" 28.33–41.33 s. Near-silent start (0–6) with sparse onsets, SURGE at 6 (hit 7.36), medium, SURGE at 10–11 (hit 11.54), 0.8 s fade-out. Bars at 3.3 · 6.66 · 9.89 · 12.93.

## Frame 1 — pregunta

- src: compositions/frames/01-pregunta.html
- duration: 3.3s
- span_sec: [0.0, 3.3]
- pacing: phrase_flow
- mood: [warm, dreamy]
- feel: calm, almost silent opening with a few soft onsets

### Groups

- **g1** — free_design
  - span_sec: [0.0, 3.3]
  - free_design: { dominant_system: "gentle question over a resting Apruvi", primitives: ["kinetic-letter-in", "negative-space-hold"], density_topology: "accumulate" }
  - anchors: [1.04, 1.81, 2.51]
  - copy: ["¿Un par de días", "sin estudiar?"]
  - notes: bg-warm, soft. Apruvi sits with a dim (unlit) flame next to him, breathing slowly. Two lines fade up softly on 1.04 / 1.81. No guilt: friendly tone.

## Frame 2 — espera

- src: compositions/frames/02-espera.html
- duration: 3.36s
- span_sec: [3.3, 6.66]
- pacing: phrase_flow
- mood: [warm, dreamy]
- feel: continued calm onset desert until the surge at 6

### Groups

- **g1** — free_design
  - span_sec: [3.3, 6.66]
  - free_design: { dominant_system: "Apruvi holds up a speech bubble", primitives: ["overlay-pop", "negative-space-hold"], density_topology: "hold" }
  - anchors: [3.3, 4.16, 5.74]
  - copy: ["Te estoy esperando"]
  - notes: Apruvi stands and a speech bubble "Te estoy esperando" pops on 4.16; slow breathing; a small anticipation squash before 6.66.

## Frame 3 — ratito

- src: compositions/frames/03-ratito.html
- duration: 3.23s
- span_sec: [6.66, 9.89]
- pacing: beat_cut
- mood: [hype, warm]
- feel: the SURGE at 6 with a strong hit at 7.36, then steady medium beats

### Groups

- **g1** — free_design
  - span_sec: [6.66, 9.89]
  - free_design: { dominant_system: "flame relights with a burst", primitives: ["crash-zoom-in", "radial-burst-lines", "overlay-pop"], density_topology: "build" }
  - anchors: [6.66, 7.36, 8.34, 9.12]
  - copy: ["Un ratito hoy", "ya cuenta"]
  - notes: The dim flame bursts alight on 6.66 with radial lines; title "Un ratito hoy ya cuenta" lands on 7.36; Apruvi jumps happily on 8.34 / 9.12.

## Frame 4 — vuelve

- src: compositions/frames/04-vuelve.html
- duration: 3.11s
- span_sec: [9.89, 13.0]
- pacing: beat_cut
- mood: [hype, warm]
- feel: SURGE at 10–11 with the strong hit at 11.54, fade-out at the end

### Groups

- **g1** — free_design
  - span_sec: [9.89, 13.0]
  - free_design: { dominant_system: "streak relights, then brand lockup", primitives: ["overlay-pop", "particle-burst"], density_topology: "hold-then-sting" }
  - anchors: [9.89, 10.68, 11.54]
  - copy: ["Vuelve a encender tu racha", "apruebatuexamen.cl"]
  - notes: "Vuelve a encender tu racha" + week dots lighting on 9.89 / 10.68; lockup (logo + "Aprueba tu examen" + URL) lands on 11.54 with confetti; hold through the fade.

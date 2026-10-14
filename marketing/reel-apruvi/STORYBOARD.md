---
compositionId: bgm
duration_s: 21.0 # == audiomap.audio.duration_sec
canvas: {"w": 1080, "h": 1920, "fps": 30}
style:
  font: "Geist"
  palette: ["#fbf8f3", "#1f2430", "#2f5bd3", "#f5a524", "#067647", "#f97316"]
assets: "assets/fonts/Geist-latin.woff2 (fuente local); Apruvi como SVG inline desde frontend/src/components/apruvi.tsx"
build_notes:
  - "one paused timeline per frame"
  - "no remote assets"
  - "brand from frame.md (motion.md del sitio), no preset"
  - "Reels safe zones: nothing important in the top 288px or bottom 384px"
  - "Apruvi breathes, blinks and sways the tassel in every frame where it appears"
avoid: ["dark backgrounds", "tiny unreadable text", "promising to pass the exam", "emoji"]
---

Track read: tropical house, ~76 BPM grid (steady, real kicks), bars at 0.07 · 3.3 · 6.69 · 9.91 · 13.3 · 16.7 · 19.99. Arc: soft intro → first hit 3.2 → high 3–7 → break 8–10 → big SURGE at 10 (hit 10.94) → high to 17 → drop + silence 18–19 → final hit 19.9 → fade-out to 21.0.

## Frame 1 — intro

- src: compositions/frames/01-intro.html
- duration: 3.3s
- span_sec: [0.0, 3.3]
- pacing: beat_cut
- mood: [warm, playful]
- feel: soft intro on a steady beat, small build at 2.0, first strong hit at 3.2 closing the bar

### Groups

- **g1** — free_design
  - span_sec: [0.0, 3.3]
  - free_design: { dominant_system: "Apruvi hero + per-beat kinetic question", primitives: ["kinetic-letter-in", "overlay-pop", "braam-punch"], density_topology: "accumulate" }
  - anchors: [0.07, 0.79, 1.58, 2.51, 3.2]
  - copy: ["¿Se viene", "tu examen", "de grado?"]
  - notes: bg-warm. Apruvi drops in from above and lands with a squash on 0.07 (big, centered low, ~520px). The three lines of the question land one per beat (0.79, 1.58, 2.51) above him. On 3.2 the whole question braam-punches (scale slam) as the cut arrives.

## Frame 2 — mapa

- src: compositions/frames/02-mapa.html
- duration: 6.61s
- span_sec: [3.3, 9.91]
- pacing: beat_cut
- mood: [playful, hype]
- feel: high-energy bar (3.3–6.7) on steady kicks, then a break with an onset desert 7–10

### Groups

- **g1** — free_design
  - span_sec: [3.3, 6.69]
  - free_design: { dominant_system: "study map path drawing node by node", primitives: ["directional-fill", "overlay-pop"], density_topology: "accumulate" }
  - anchors: [3.3, 4.18, 4.97, 5.74]
  - copy: ["Tu mapa de estudio"]
  - notes: Title "Tu mapa de estudio" hard-cuts in at 3.3 (top, inside safe zone). A winding path (like the site's map) draws downward; one node pops per beat (4.18, 4.97, 5.74): first node success + check, the rest brand / locked. Apruvi hops from node to node on those same beats (hop curve from frame.md).
- **g2** — free_design
  - span_sec: [6.69, 9.91]
  - free_design: { dominant_system: "Apruvi talks in a speech bubble over the map", primitives: ["negative-space-hold", "overlay-pop"], density_topology: "hold" }
  - anchors: [6.69, 7.48]
  - copy: ["Nivel a nivel,", "yo te acompaño."]
  - notes: On 6.69 the map dims behind; Apruvi (bigger) gets a white speech bubble that pops in on 7.48 and holds through the 8–10 break, breathing. Calm hold — no new hits during the silence.

## Frame 3 — racha

- src: compositions/frames/03-racha.html
- duration: 3.39s
- span_sec: [9.91, 13.3]
- pacing: beat_cut
- mood: [hype, playful]
- feel: the big SURGE at 10 with hits at 10.94 and 11.54, sustained high energy to the 13.3 downbeat

### Groups

- **g1** — free_design
  - span_sec: [9.91, 13.3]
  - free_design: { dominant_system: "streak flame bursts in and the day counter climbs", primitives: ["crash-zoom-in", "counting-punch", "radial-burst-lines"], density_topology: "build-then-lock" }
  - anchors: [9.91, 10.87, 10.94, 11.54, 11.66, 12.52, 13.3]
  - copy: ["Rachas con fueguito", "días seguidos"]
  - notes: SURGE: crash-zoom into a big flame on 9.91 with radial burst lines (warm oranges). Counter climbs 1 → 7 across 10.87–12.52 (one step per hit/beat), locking with a punch on 12.52; label "días seguidos" under the number, title "Rachas con fueguito" at top. Seven week dots light up (flame icons) as the counter climbs. Apruvi peeks from the side cheering.

## Frame 4 — oral

- src: compositions/frames/04-oral.html
- duration: 3.4s
- span_sec: [13.3, 16.7]
- pacing: beat_cut
- mood: [playful, hype]
- feel: medium-high bar with steady kicks on every beat, short drop near 14

### Groups

- **g1** — free_design
  - span_sec: [13.3, 16.7]
  - free_design: { dominant_system: "voice waveform pulsing per beat around a mic", primitives: ["overlay-pop", "kinetic-letter-in"], density_topology: "pulse" }
  - anchors: [13.3, 14.1, 15.02, 15.81]
  - copy: ["Simula tu examen oral", "con tiempos reales"]
  - notes: Hard cut at 13.3 to brand-blue background (white type) — a palette contrast against the warm frames. Apruvi sits on a white circular spotlight disc (so the blue body reads on the blue background) and holds a mic; a rounded waveform (bars) pulses on each beat; a small timer pill ticks. Title lands on 13.3, subtitle on 14.1.

## Frame 5 — cierre

- src: compositions/frames/05-cierre.html
- duration: 4.3s
- span_sec: [16.7, 21.0]
- pacing: beat_cut
- mood: [warm, cinematic]
- feel: last high beat at 16.7, drop at 17 and silence 18–19, final strong hit at 19.9, fade-out to the end

### Groups

- **g1** — free_design
  - span_sec: [16.7, 21.0]
  - free_design: { dominant_system: "offer card then brand lockup on the final hit", primitives: ["overlay-pop", "negative-space-hold", "particle-burst"], density_topology: "hold-then-sting" }
  - anchors: [16.7, 17.48, 19.9]
  - copy: ["Prepara tu examen con Apruvi", "7 días gratis", "apruebatuexamen.cl"]
  - notes: bg-warm. On 16.7 "Prepara tu examen con Apruvi" pops; on 17.48 a game-style button card "7 días gratis" pops and holds through the 18–19 silence (negative space, only breathing). On 19.9 the brand lockup lands: logo mark (graduation cap in blue rounded square) + "Aprueba tu examen" + "apruebatuexamen.cl", with a soft confetti/particle burst in brand/accent colors; Apruvi (smaller, above the lockup, never overlapping it) waves. Lockup sits between 64% and 76% of the height, clear of the bottom safe zone. Hold to 21.0 while the music fades.

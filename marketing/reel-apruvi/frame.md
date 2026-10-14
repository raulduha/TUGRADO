---
version: alpha
name: Aprueba tu examen — Frame (Reel 9:16)
description: >
  Capa de video de la marca Aprueba tu examen, tomada de motion.md (raíz del repo) y del sitio
  https://apruebatuexamen.cl. Tema claro y cálido, Geist en todo, Apruvi como protagonista,
  movimiento con rebote suave. Nunca oscuro, nunca agresivo, nunca promete aprobar el examen.
unit: el frame — 1080×1920 (9:16, Instagram Reels)
principle: los átomos vienen del sitio · la composición es libre · el ritmo lo manda la música

colors:
  background: "#fbf8f3"
  foreground: "#1f2430"
  surface: "#ffffff"
  muted: "#5d6474"
  line: "#e7e1d6"
  brand: "#2f5bd3"
  brand-strong: "#2448ad"
  brand-soft: "#e8eefc"
  accent: "#f5a524"
  accent-soft: "#fdf1dc"
  success: "#067647"
  flame-outer: "#f97316"
  flame-inner: "#fbbf24"
  cap: "#1f2a4d"
  cap-base: "#2b3864"
  cheek: "#f7a8b8"

typography:
  # Geist variable, local: assets/fonts/Geist-latin.woff2 (pesos 100–900)
  display:  { fontFamily: "Geist", px: 132, weight: 700, lineHeight: 0.95, tracking: "-0.035em" }
  headline: { fontFamily: "Geist", px: 96,  weight: 700, lineHeight: 1.0,  tracking: "-0.03em" }
  title:    { fontFamily: "Geist", px: 64,  weight: 600, lineHeight: 1.08, tracking: "-0.02em" }
  body:     { fontFamily: "Geist", px: 44,  weight: 500, lineHeight: 1.3,  color: "muted" }
  label:    { fontFamily: "Geist", px: 34,  weight: 600, tracking: "0.01em" }
  numeral:  { fontFamily: "Geist", px: 300, weight: 800, lineHeight: 0.85, tracking: "-0.05em" }

spacing:
  safe-top: "288px"     # 15 % superior: interfaz de Instagram
  safe-bottom: "384px"  # 20 % inferior: descripción y botones de Reels
  pad-edge: "88px"

components:
  bg-warm:
    background: "linear-gradient(180deg, {colors.brand-soft} 0%, {colors.background} 55%, {colors.accent-soft} 100%)"
    description: "Fondo base del video: degradado vertical del mapa del sitio."
  card:
    background: "{colors.surface}"
    border: "2px solid {colors.line}"
    radius: "48px"
    shadow: "0 24px 60px rgba(31,36,48,0.10)"
  button:
    background: "{colors.brand}"
    color: "#ffffff"
    radius: "32px"
    shadow: "0 10px 0 {colors.brand-strong}"
    description: "Botón tipo juego 2D, como los nodos del mapa."
  node:
    size: "150px circle, borde inferior 14px"
    states: "completado = success + check · actual = brand + halo brand 15 % · bloqueado = #ece7de / #d6cfc2"
  apruvi:
    source: "frontend/src/components/apruvi.tsx (viewBox 120×130), copiado como SVG inline"
    description: >
      Bolita azul con guatita blanca, ojos grandes con brillo, mejillas rosadas, birrete azul
      marino con borla accent. Respira (3,8 s), parpadea (5,2 s) y mece la borla en loop durante
      todo el video. Protagonista de cada escena.
  flame:
    description: "Llama de dos capas (flame-outer / flame-inner) que oscila como vela."

motion:
  feel: "alegre y épica, con rebote suave; cortes duros en los compases, entradas pop-in"
  pop-in: "0,45 s cubic-bezier(0.2, 0.9, 0.3, 1.3) — escala 0,85 → 1 con rebote"
  hop: "1,1 s cubic-bezier(0.45, 0, 0.55, 1) — Apruvi salta 22 px (escalar al canvas: ~60 px)"
  avoid: ["fondos oscuros", "glitch agresivo", "texto que dura menos de un pulso", "promesas de aprobar"]

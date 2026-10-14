# MOTION — guía visual y de movimiento de Aprueba tu examen

Sitio: https://apruebatuexamen.cl

Lee este archivo **antes de diseñar, generar o animar** cualquier cosa: pantallas, correos,
videos (HyperFrames) o piezas para redes. La fuente de verdad del código es
`frontend/src/app/globals.css`; si cambia un valor allá, actualízalo aquí.

## Personalidad

Amigable, cálida y clara. Tema claro único (nunca modo oscuro). Nada agresivo ni "dark".
Nunca prometer que el estudiante aprobará el examen: se anima, no se garantiza.

## Colores

| Token | Hex | Uso |
| --- | --- | --- |
| `background` | `#fbf8f3` | Fondo general (crema cálido) |
| `foreground` | `#1f2430` | Texto principal |
| `surface` | `#ffffff` | Tarjetas |
| `muted` | `#5d6474` | Texto secundario |
| `line` | `#e7e1d6` | Bordes y divisores |
| `brand` | `#2f5bd3` | Azul de marca: botones, nivel en curso, cuerpo de Apruvi |
| `brand-strong` | `#2448ad` | Hover de botones, pies de Apruvi, borde inferior de nodos |
| `brand-soft` | `#e8eefc` | Fondos suaves, degradado superior del mapa |
| `on-brand` | `#ffffff` | Texto sobre azul |
| `accent` | `#f5a524` | Acento decorativo (borla del birrete); **nunca para texto** |
| `accent-soft` | `#fdf1dc` | Degradado inferior del mapa y del hero |
| `success` | `#067647` | Completado, check, tramo recorrido del mapa |
| `danger` | `#b42318` | Errores y acciones destructivas |

Colores de piezas puntuales:

| Uso | Hex |
| --- | --- |
| Llama exterior (racha) | `#f97316` |
| Llama interior | `#fbbf24` |
| Día con racha (fondo / texto) | `#fff1e6` / `#c2410c` |
| Birrete de Apruvi (copa / base) | `#1f2a4d` / `#2b3864` |
| Mejillas de Apruvi | `#f7a8b8` |
| Nodo bloqueado (fondo / borde) | `#ece7de` / `#d6cfc2` |
| Nodo completado (borde inferior) | `#05603a` |

Degradados: hero y mapa van de `brand-soft` a `accent-soft` (diagonal en el hero, vertical
en el mapa con `surface` al medio).

## Tipografía

- Familia única: **Geist** (Google Fonts, variable `--font-geist-sans`), con respaldo
  `-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` (correos).
- Títulos: `font-semibold` (600) con `tracking-tight`. H1 de pantalla 24–30 px; números
  grandes (racha, precio, porcentaje) 30–36 px.
- Texto: 16 px, interlineado 1.5–1.6. Secundario 14 px en `muted`. Etiquetas pequeñas 12 px.
- Botones: 16 px, `font-semibold`.
- Idioma: español de Chile, trato de "tú", sin lenguaje de género innecesario.

## Formas

- Radios: botones `rounded-xl` (12 px), tarjetas `rounded-2xl`/`rounded-3xl` (16–24 px),
  campos `rounded-lg` (8 px), píldoras y nodos `rounded-full`.
- Nodos del mapa: círculos de 64 px con borde inferior de 6 px (efecto botón de juego 2D).
- Sombras suaves: `shadow-sm` en botones, `shadow-xl` solo en diálogos.
- Íconos: trazo de 2 px, puntas redondeadas, 24×24 (SVG propios, sin librerías).

## Apruvi (mascota)

Bolita azul (`brand`) con guatita blanca, ojos grandes con brillo, mejillas rosadas, sonrisa
pequeña, bracitos y birrete azul marino con borla `accent`. Componente:
`frontend/src/components/apruvi.tsx` (viewBox 120×130). Personaje original: no imitar
mascotas de otras marcas.

## Reglas de timing

| Movimiento | Duración | Curva | Detalle |
| --- | --- | --- | --- |
| Respiración de Apruvi | 3,8 s, infinito | ease-in-out | escala (0,985 ; 1,035) desde los pies, pico al 45 % |
| Sombra de Apruvi | 3,8 s | ease-in-out | se achica a 0,94 al inhalar |
| Parpadeo | 5,2 s | ease-in-out | ojos a scaleY 0,1 entre el 92 % y el 95 % |
| Borla del birrete | 3,8 s | ease-in-out | rota de −5° a 6° desde arriba |
| Salto (carga) | 1,1 s | cubic-bezier(0.45, 0, 0.55, 1) | sube 22 px; se aplasta 1,06 × 0,92 al caer |
| Sombra del salto | 1,1 s | igual | escala 0,6 y opacidad 0,5 en lo alto |
| Puntos de carga | 0,9 s, desfase 150 ms | ease-in-out | suben 5 px |
| Frase de carga | 0,4 s | ease-out | entra subiendo 4 px; cambia cada 1,8 s |
| Llama exterior / interior | 1,6 s / 1,1 s (inversa) | ease-in-out | oscila como vela desde la base |
| Entrada de diálogo (pop-in) | 0,45 s | cubic-bezier(0.2, 0.9, 0.3, 1.3) | de 0,85 y +12 px a su lugar, con rebote |
| Apruvi avanzando en el mapa | 0,7 s | ease-out | transición de posición |
| Hover de botones y nodos | ~150 ms | por defecto | nodo seleccionado escala 1,1 |

Siempre respetar `prefers-reduced-motion`: sin animaciones en loop.

## Para video y redes

- Usa estos colores y Geist; Apruvi como protagonista; fondos crema o degradado
  `brand-soft` → `accent-soft`.
- Movimiento con rebote suave (como el pop-in), nunca brusco ni oscuro.
- Cierre con la marca: logo (birrete en cuadrado azul) + "Aprueba tu examen" +
  apruebatuexamen.cl.

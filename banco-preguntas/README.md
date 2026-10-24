# Banco de preguntas

Preguntas de alternativas para `/practica`, organizadas según los temarios oficiales del examen de grado. Cada archivo de `datos/` corresponde a una cédula (o a una parte de ella) y genera una planilla en `salida/` con el formato de la plantilla oficial (`docs/plantillas/preguntas-alternativas.xlsx`).

## Generar las planillas

Desde `backend/`:

```sh
uv run python ../banco-preguntas/build.py                       # datos/*.py → salida/*.xlsx
uv run python ../banco-preguntas/convertir_uandes.py <original>  # banco de la U. de los Andes
```

`build.py` valida cada planilla con el importador real de la app (`app/content/importer.py`) y con reglas propias: 4 alternativas, sin enunciados repetidos, y una explicación que empieza por «Es la X» y descarta cada alternativa incorrecta («La Y no, …»). También reparte la alternativa correcta en ciclo A, B, C, D, para que no se pueda adivinar por la posición.

## Subir a la app

En `/admin/preguntas`, importa la planilla de `salida/`. Las preguntas entran como **borrador**. Un abogado distinto de quien las importó debe revisarlas y aprobarlas antes de publicarlas (AC-029).

## Qué revisar en cada pregunta

- Que la respuesta correcta lo sea según la **ley vigente**. Las cédulas UC son de 2021, y desde entonces cambiaron normas, por ejemplo con la Ley 21.400 de matrimonio igualitario.
- Que los artículos citados en `fuente` digan lo que la explicación afirma.
- Que ninguna alternativa incorrecta sea defendible.

## Origen

| Archivo | Programa | Fuente del temario |
|---|---|---|
| `uc-01*-civil-*.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Civil](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Civil_18.03.2021.pdf) |
| `convertir_uandes.py` | Cedulario U. de los Andes 2026 | Banco «Acto jurídico y prueba» entregado por el equipo |

Los temarios se usan solo como índice de materias: las preguntas son de redacción propia. El programa (UC o U. de los Andes) todavía no se modela en la app, así que cada programa va en planillas separadas.

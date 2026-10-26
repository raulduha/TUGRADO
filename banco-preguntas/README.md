# Banco de preguntas

Preguntas de alternativas para `/practica`, organizadas según los temarios oficiales del examen de grado. Cada archivo de `datos/` corresponde a una cédula (o a una parte de ella) y genera una planilla en `salida/` con el formato de la plantilla oficial (`docs/plantillas/preguntas-alternativas.xlsx`).

## Generar las planillas

Desde `backend/`:

```sh
uv run python ../banco-preguntas/build.py                       # datos/*.py → salida/*.xlsx
uv run python ../banco-preguntas/convertir_uandes.py <original>  # banco de la U. de los Andes
```

`build.py` valida cada planilla con el importador real de la app (`app/content/spreadsheet.py`) y con reglas propias: 4 alternativas, sin enunciados repetidos, y una explicación que empieza por «Es la X» y descarta cada alternativa incorrecta («La Y no, …»). También reparte la alternativa correcta en ciclo A, B, C, D, para que no se pueda adivinar por la posición.

## Glosario del rosco legal

`glosario.py` genera `salida/glosario-civil-procesal.xlsx` (52 términos de Civil y Procesal) y lo valida con el lector de la app. Se sube en `/admin/glosario`: entra en borrador y otro administrador lo aprueba y publica, después de que el abogado revise cada definición.

## Relleno para probar (solo local)

`relleno.py` genera preguntas evidentemente falsas («[Relleno] …») para las 10 electivas que aún no tienen banco, sobre los subtemas reales del temario, y con `--cargar` las importa y publica en el backend local con las cuentas demo. Sirve para ver la ruta y el plan diario con todas las materias. **No es contenido jurídico ni debe subirse a producción**: el script se niega a cargar en un backend que no sea local, y la planilla que genera no se versiona.

## Subir a la app

En `/admin/preguntas`, importa la planilla de `salida/`. Las preguntas entran como **borrador**. Un abogado distinto de quien las importó debe revisarlas y aprobarlas antes de publicarlas (AC-029).

## Qué revisar en cada pregunta

- Que la respuesta correcta lo sea según la **ley vigente**. Las cédulas UC son de 2021, y desde entonces cambiaron normas, por ejemplo con la Ley 21.400 de matrimonio igualitario, la Ley 21.481 (quórum de reforma constitucional), la Ley 21.561 (jornada de 42 horas desde abril de 2026, 40 desde 2028) y la Ley 21.643 (Ley Karin).
- Que los artículos citados en `fuente` digan lo que la explicación afirma.
- Que ninguna alternativa incorrecta sea defendible.

## Origen

| Archivo | Programa | Fuente del temario |
|---|---|---|
| `uc-01*-civil-*.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Civil](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Civil_18.03.2021.pdf) |
| `uc-02*-procesal-*.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Procesal](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Procesal_18.03.2021.pdf) |
| `uc-03-administrativo-i.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Administrativo I](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Administrativo_1_18.03.2021.pdf) |
| `uc-06-comercial-sociedades.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Comercial I](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Comercial_1_Sociedades_18.03.2021.pdf) |
| `uc-09-constitucional-derechos.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Constitucional I](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Constitucional_1_-_Derechos_y_Garantias_18.03.2021.pdf) |
| `uc-10-constitucional-organico.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Constitucional II](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Constitucional_2_-_Constitucional_Organico_18.03.2021.pdf) |
| `uc-14-penal.py` | Cédulas UC (licenciatura, desde 2021) | [Cédula de Derecho Penal](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_Penal_18.03.2021.pdf) |
| `uc-16-trabajo.py` | Cédulas UC (licenciatura, desde 2025) | [Cédula de Derecho del Trabajo](https://derecho.uc.cl/wp-content/uploads/2026/05/Cedula_Derecho_del_Trabajo_02.12.2025.pdf) |
| `convertir_uandes.py` | Cedulario U. de los Andes 2026 | Banco «Acto jurídico y prueba» entregado por el equipo |

Los temarios se usan solo como índice de materias: las preguntas son de redacción propia. El programa (UC o U. de los Andes) todavía no se modela en la app, así que cada programa va en planillas separadas.

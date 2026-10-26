# Planes, precios y proveedores de IA

Decisión de producto del 2026-10-25, delegada por el usuario. Cifras en pesos chilenos con IVA incluido. Los costos de IA son estimaciones (~US$1 por hora de interrogación) y deben recalcularse con el uso real.

## Reglas

1. **Ganamos al menos $5.000 por suscriptor al mes en cada plan, aunque use todo su cupo.** Por eso las horas de interrogación tienen tope mensual, no se acumulan y los descuentos solo se ofrecen donde el margen lo permite.
2. **Solo se cobra por lo que existe.** Hoy se vende Procurador; Litigante y Toga se habilitan cuando la interrogación oral con IA pase la prueba de calidad.
3. **No vendemos horas de abogados.** El abogado del equipo revisa el banco de preguntas y las rúbricas con que la IA corrige; eso es lo que se comunica («contenido y criterios revisados por un abogado»), no clases.

## Mercado (precios publicados, octubre de 2026)

| Alternativa | Precio |
|---|---|
| Profesor particular (Superprof, TusClases) | $10.000 a $25.000 por hora |
| Derecho al Grado | $20.000 por interrogación de 1 h |
| Domina Tu Grado | $29.000 la sesión; $105.000 a $195.000 al mes |
| Preparatugrado | $49.990 a $59.990 al mes por 1 interrogación semanal + simulacro |

Una preparación con personas cuesta entre $200.000 y $600.000 en total y da unas 4 horas de interrogación al mes. Se titulan ~4.900 abogados al año (Mineduc 2024).

## Planes

| | **Procurador** | **Litigante** | **Toga** |
|---|---|---|---|
| Precio | $7.990/mes | $14.990/mes | $24.990/mes |
| Incluye | Banco de alternativas, ruta, repaso espaciado, plan diario, rachas | Procurador + 7 h al mes de interrogación oral con IA + simulacro de comisión mensual | Procurador + 15 h al mes de interrogación oral con IA + simulacro de comisión semanal + informe de brechas por cédula |
| Cuándo | Al activar Flow | Con la interrogación oral | Con la interrogación oral |

- Todos con 14 días de prueba gratis (`BILLING_TRIAL_DAYS`).
- Pase «Hasta tu examen» solo para Procurador: 6 meses por $37.990. En los planes con interrogación, un descuento bajaría el margen de los $5.000.
- Invita a tu dupla: ambos reciben 7 días gratis más (sin horas extra, que tienen costo de IA).
- Las horas de interrogación reemplazan la cuota única de 5 simulaciones al día y 100 al mes.
- Planes en Flow: `APRUEBA-MENSUAL` ($9.990) ya existe y no calza con estos precios; hay que crear `PROCURADOR-MENSUAL` ($7.990) y desactivar el anterior.

## Margen por suscriptor al mes

Comisión de Flow verificada en su simulador: 2,89 % + IVA (3,44 % total) con abono al tercer día hábil.

| | Procurador | Litigante | Toga |
|---|---|---|---|
| Ingreso sin IVA | $6.714 | $12.597 | $21.000 |
| Comisión de Flow | $275 | $516 | $860 |
| IA si usa todo el cupo (a US$1 la hora) | $0 | $7.000 | $15.000 |
| **Margen mínimo** | **$6.439** | **$5.081** | **$5.140** |
| IA con uso típico (60 %) | $0 | $3.990 | $8.550 |
| **Margen esperado** | **$6.439** | **$8.091** | **$11.590** |

## Resultado mensual estimado

Mezcla supuesta: 50 % Procurador, 40 % Litigante, 10 % Toga. Gastos fijos: $80.000 de infraestructura y $300.000 de marketing. El trabajo del equipo (incluido el abogado) no está valorizado.

| Suscriptores | Ventas con IVA | Ingreso sin IVA | Flow | IA | Fijos | Resultado |
|---|---|---|---|---|---|---|
| 60 | $749.400 | $629.748 | $25.779 | $147.060 | $380.000 | $76.909 |
| 150 | $1.873.500 | $1.574.370 | $64.448 | $367.650 | $380.000 | $762.271 |
| 400 | $4.996.000 | $4.198.319 | $171.862 | $980.400 | $380.000 | $2.666.057 |

Punto de equilibrio: unos 50 suscriptores. Resultado antes de impuesto a la renta; IVA incluido en el precio, pendiente de confirmar con un contador (pendiente 7 del README).

## Proveedores de IA (pendiente 3 del README)

- **Evaluación:** Claude Sonnet 5.5 (Anthropic), con caché de la rúbrica.
- **Transcripción y embeddings:** OpenAI (`gpt-4o-transcribe` y `text-embedding-3-small`).
- **Voz sintetizada:** no en el MVP; la pregunta se muestra en pantalla y solo habla el estudiante.
- **Umbral para lanzar:** con 30 respuestas reales corregidas por el abogado del equipo, la nota del modelo queda a 0,5 puntos o menos de la suya en al menos el 80 % de los casos, y la transcripción no cambia el sentido jurídico de ninguna. Si Sonnet no lo cumple, se prueba Claude Opus 5.5 y se recalculan los topes de horas para mantener los $5.000.

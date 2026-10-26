# Planes, precios y proveedores de IA

Decisión de producto del 2026-10-25, delegada por el usuario («piénsalo tú, eres CEO»). Cifras en pesos chilenos con IVA incluido; los costos de IA están en dólares convertidos a ~$950 por dólar y deben recalcularse con datos reales de uso.

## Principio

Solo se cobra por lo que existe. Hoy la aplicación ofrece práctica de alternativas, ruta, repaso de errores y plan diario; la interrogación oral aún no está construida. Por eso se lanza un solo plan y los otros dos se habilitan cuando la interrogación oral pase la prueba de calidad.

## Planes

| Plan | Precio | Incluye | Cuándo |
|---|---|---|---|
| **Procurador** | $7.000/mes | Banco de alternativas, ruta, repaso espaciado, plan diario y rachas | Al activar Flow |
| **Litigante** | $9.990/mes | Procurador + 4 interrogaciones orales de 1 hora al mes (una por semana) | Con la interrogación oral |
| **Toga** | $14.990/mes | Litigante + 4 interrogaciones más (8 al mes) y 1 simulacro de examen completo al mes | Con la interrogación oral |

- Todos con 14 días de prueba gratis (`BILLING_TRIAL_DAYS`).
- Quien se suscriba a Procurador antes del lanzamiento de la interrogación oral conserva ese precio mientras siga suscrito («precio fundador»).
- El plan de Flow `APRUEBA-MENSUAL` ($9.990) queda para Litigante; hay que crear `PROCURADOR-MENSUAL` ($7.000) y, más adelante, `TOGA-MENSUAL` ($14.990).
- Las interrogaciones son cupos mensuales, no ilimitadas. Reemplazan la cuota única de 5 simulaciones al día y 100 al mes cuando existan los planes con interrogación.

## Márgenes estimados por estudiante al mes

| | Procurador | Litigante | Toga |
|---|---|---|---|
| Precio sin IVA | $5.882 | $8.395 | $12.597 |
| Comisión de Flow (~4 %, por confirmar) | ~$240 | ~$340 | ~$510 |
| IA si usa todo su cupo | $0 | ~$4.100 | ~$8.200 |
| Margen si usa todo | ~$5.640 | ~$3.950 | ~$3.900 |

Costo de IA por hora de interrogación (~20 preguntas): ~US$1. Los gastos fijos de infraestructura (~$50.000 a $80.000 al mes) se cubren con 10 a 15 suscriptores de Procurador.

## Proveedores de IA (pendiente 3 del README)

- **Evaluación:** Claude Sonnet 5.5 (Anthropic), con caché de la rúbrica.
- **Transcripción y embeddings:** OpenAI (`gpt-4o-transcribe` y `text-embedding-3-small`).
- **Voz sintetizada:** no en el MVP; las preguntas y la retroalimentación se muestran en pantalla y solo el estudiante habla. Ahorra ~30 % del costo por hora.
- Dos proveedores en total, ambos detrás de las interfaces existentes.
- **Umbral de calidad para lanzar:** con 30 respuestas reales corregidas por un abogado, la nota del modelo debe quedar a 0,5 puntos o menos de la del abogado en al menos el 80 % de las respuestas, y la transcripción no debe cambiar el sentido jurídico de ninguna. Si Sonnet no lo cumple, se prueba Claude Opus 5.5 y se recalcula el precio de Toga.

## Fidelización (para la etapa con interrogación oral)

1. **Estrellas Apruvi:** 30 días seguidos de racha dan 1 interrogación extra.
2. **Invita a tu dupla:** quien invita y quien llega ganan 1 interrogación extra al suscribirse el invitado.

Más adelante, según los datos: recarga de horas sueltas, acumulación de horas no usadas y pago único «hasta tu examen». Ninguna promoción puede prometer la aprobación del examen.

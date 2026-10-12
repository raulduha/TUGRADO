# AGENTS.md — Reglas para agentes de desarrollo

## Fuente de verdad

- Las especificaciones de `specs/` y los controles de `harness/` son la fuente de verdad funcional.
- Antes de implementar, lee los documentos relevantes, identifica ambigüedades y propone cambios a las especificaciones si una regla es incompleta.
- No inventes requisitos para resolver decisiones pendientes. Registra la pregunta como pendiente y evita codificar una suposición irreversible.

## Stack y límites

- Frontend: Next.js + TypeScript.
- Backend: FastAPI + Python 3.12 (uv). Base de datos: PostgreSQL con SQLAlchemy y Alembic; RAG con pgvector. Autenticación propia en el backend. Observabilidad con OpenTelemetry. Entorno local con Docker. Frontend en Vercel, base de datos en Neon, archivos en Vercel Blob y cola en PostgreSQL.
- El backend es la fuente de verdad para permisos, estados de sesión, temporizadores, extensiones, resultados y publicación.
- Mantén proveedores de IA, transcripción, embeddings y síntesis detrás de interfaces intercambiables.
- La interfaz debe ser responsive desde la primera versión.

## Reglas de negocio obligatorias

- La jurisdicción es configurable; cada materia puede tener su propia estructura de subtemas.
- Los roles mínimos son `student` y `administrator`.
- Solo contenido aprobado en una versión exacta puede publicarse y utilizarse en sesiones ordinarias.
- La retroalimentación oral se configura antes de iniciar la sesión: después de cada pregunta o al final.
- La simulación tiene límites total e individual. Al agotarse el tiempo total, no se inician nuevas preguntas; la pregunta activa puede finalizar dentro de su límite individual y extensiones válidas.
- La extensión individual es de 60 segundos, se solicita dentro de 15 segundos tras expirar el tiempo individual y se permite 1 por pregunta. Estos valores son configuración (`max_extensions_per_question`, ventana de oferta), no constantes en el código.
- Ante una desconexión (30 s sin latido; latido cada 10 s), pausa el tiempo retroactivamente desde el último latido y permite reanudar desde el último estado guardado con el tiempo restante dentro de 30 minutos (`recovery_window`). Pasado ese plazo, la sesión queda `expired`.
- Pausa voluntaria: solo entre preguntas, hasta 30 segundos, una vez por simulación.
- Una simulación contiene un solo tipo de pregunta. Quien crea o modifica una versión no puede aprobarla ni publicarla. Las correcciones de resultados exigen un reporte vinculado.
- Cuotas iniciales: 5 simulaciones orales por día y 100 por mes por usuario. Eliminación a solicitud en un máximo de 30 días. Contraseñas: mínimo 12 caracteres con Argon2id. Escala 1 a 7: conversión lineal ponderada con un decimal.
- La lista única de decisiones abiertas está en `README.md`. Si una tarea depende de una de ellas, regístrala como pendiente y no la resuelvas por suposición.
- El plan de estudio conserva una línea base original y genera revisiones adaptativas sin borrar el plan inicial.
- En el MVP, la voz funciona por turnos. No implementes conversación en tiempo real como requisito inicial; conserva una arquitectura que permita incorporarla después.
- No persistas el audio original por defecto; conserva transcripciones y resultados 12 meses. Elimina el audio temporal al terminar la transcripción.
- RAG debe usar fuentes recuperadas y trazables. No inventes citas jurídicas ni afirmes vigencia sin soporte.
- El estudiante puede reportar preguntas y evaluaciones, pero no editar directamente su resultado.
- Las correcciones administrativas deben preservar resultado original, resultado corregido, motivo, responsable y fecha.
- No garantices que el estudiante aprobará el examen.

## Flujo de trabajo

1. Lee los requisitos, el modelo de dominio, la arquitectura y criterios de aceptación relacionados.
2. Identifica reglas ambiguas o contradictorias antes de programar.
3. Propón una tarea pequeña y su plan de pruebas.
4. Implementa solo el alcance aprobado.
5. Añade pruebas unitarias, integración o end-to-end según corresponda.
6. Ejecuta los controles de `harness/quality-gates.md`.
7. Informa exactamente qué cambió, qué pruebas se ejecutaron y qué quedó pendiente.

## Restricciones

- No permitas que el frontend sea la autoridad sobre el tiempo o los permisos.
- No publiques contenido no revisado.
- No sobrescribas silenciosamente versiones de preguntas, rúbricas, fuentes o resultados.
- No conviertas una falla técnica en una nota académica negativa.
- No guardes audio original de forma persistente por defecto.
- No afirmes que las pruebas pasaron si no fueron ejecutadas.
- No amplíes el alcance sin actualizar especificaciones y criterios de aceptación.

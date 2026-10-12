# Modelo de dominio conceptual

Este modelo es lógico y no prescribe todavía un motor de base de datos.

## Entidades

- **User**: identidad, estado y datos de perfil mínimos.
- **Role / UserRole**: roles `student` y `administrator`. La autorización efectiva se valida en backend.
- **Jurisdiction**: jurisdicción jurídica configurable.
- **StudyProgram**: programa de examen, versión, jurisdicción y fecha de referencia.
- **Subject**: materia asociada a un programa o ámbito académico.
- **Subtopic**: subtema perteneciente a una materia; cada materia puede tener su propia jerarquía.
- **LegalSource**: fuente jurídica o académica, jurisdicción, tipo, referencia, versión, fechas de vigencia y metadatos de verificación cuando correspondan. Requiere revisión y aprobación antes de usarse en RAG.
- **ContentDocument**: documento fuente importado, estado de procesamiento, estado de aprobación y referencia a la fuente original. Solo documentos aprobados se indexan para RAG.
- **ContentChunk**: fragmento indexado para recuperación RAG, con metadatos y vínculo al documento fuente.
- **ContentImport**: ejecución de importación, estado, errores y resultados propuestos.
- **Question**: identidad estable de una pregunta.
- **QuestionVersion**: contenido inmutable versionado de una pregunta, tipo (`multiple_choice` u `oral`), ámbito, dificultad, respuesta correcta o referencia, explicación, fuentes y, para preguntas orales, referencia a la `EvaluationRubricVersion` aplicable. Estado de publicación: `draft`, `in_review`, `approved`, `published`, `retired`. Solo `published` es elegible en sesiones ordinarias.
- **AnswerOption**: alternativas asociadas a una versión de pregunta.
- **ContentReview**: revisión de una versión concreta (de pregunta, rúbrica, fuente o documento), revisor, estado (`pending`, `approved`, `rejected`, `changes_requested`), comentarios y fechas. Aprobar no publica: la publicación es una acción auditada posterior.
- **EvaluationRubricVersion**: criterios y pesos de evaluación versionados e inmutables; sujetos a `ContentReview`.
- **PracticeAttempt**: respuesta a una pregunta de alternativas fuera de una simulación (usuario, versión presentada, alcance, respuesta, resultado, fecha). La retroalimentación es inmediata.
- **SimulationConfiguration**: cantidad y alcance de preguntas, límite total, límite individual, modo de retroalimentación, reglas de selección y configuración de evaluación.
- **SimulationSession**: usuario, configuración congelada, estado, fecha de inicio, tiempo límite total, marcas de pausa/reanudación, estado al que se vuelve al reanudar (`resume_state`), expiración, progreso y fecha de cierre.
- **QuestionAttempt**: pregunta y versión presentada, orden, estado, hora de inicio, límite individual, extensiones concedidas, respuesta y resultado.
- **OralResponse**: transcripción, estado de transcripción, marcas de tiempo y metadatos técnicos. No contiene un audio persistente por defecto.
- **OralAssessment**: intento, versión de rúbrica, versión de respuesta de referencia, puntuaciones, justificación, confianza/limitaciones y estado.
- **SessionEvent**: evento auditable de sesión, por ejemplo pausa por desconexión, reanudación, extensión, cierre o error.
- **ContentReport**: estudiante, objeto reportado (`question`, `explanation` o `assessment`), versión de pregunta, intento y evaluación (`OralAssessment`) opcionales, motivo, estado, fechas y resolución.
- **AssessmentCorrection**: resultado original, resultado corregido, motivo, administrador, fecha y reporte de origen. Registro inmutable o de solo adición.
- **StudyPlan**: estudiante, programa, fecha de examen, disponibilidad, fecha de generación y versión del plan original.
- **StudyPlanRevision**: revisión adaptativa, fecha, factores considerados y cambios respecto del plan original.
- **StudyTask**: actividad planificada, materia/subtema, fecha, estado, prioridad y sesión vinculada cuando corresponda.
- **AIUsageRecord**: función, proveedor/modelo, consumo medible, usuario/sesión cuando corresponda, fecha y estimación de costo si está disponible.

## Estados sugeridos

### SimulationSession
`created`, `in_progress`, `paused_disconnected`, `awaiting_current_question_completion`, `completed`, `expired`, `abandoned`.

Los estados exactos y sus transiciones se deben implementar como una máquina de estados explícita. `paused_disconnected` conserva el tiempo restante y registra el estado previo (`resume_state`, por ejemplo `in_progress` o `awaiting_current_question_completion`) al que se vuelve al reanudar. Tras agotarse el tiempo total y terminar la pregunta activa, la sesión pasa a `completed`. `expired` se reserva para sesiones desconectadas que no se reanudan dentro de la ventana de recuperación (30 minutos). La pausa voluntaria (entre preguntas, hasta 30 s, una vez) se registra como evento y no usa `paused_disconnected`. `abandoned` se alcanza cuando el estudiante cierra voluntariamente la sesión sin terminar; las respuestas ya evaluadas se conservan y las pendientes no puntúan. Al agotarse el tiempo total, no se permiten nuevas preguntas; una pregunta ya activa puede terminar dentro de su límite individual y de extensiones válidas.

### QuestionAttempt
`not_started`, `in_progress`, `awaiting_extension`, `submitted`, `evaluating`, `evaluated`, `timed_out`, `cancelled`.

La solicitud de extensión concede 60 segundos únicamente si el backend la acepta. Debe evitarse que solicitudes simultáneas concedan extensiones duplicadas.

### ContentReport
`pending`, `under_review`, `resolved`, `rejected`.

### StudyTask
`scheduled`, `in_progress`, `completed`, `overdue`, `skipped`.

## Reglas de integridad

1. Solo una versión de pregunta aprobada y publicada puede usarse en sesiones ordinarias.
2. La aprobación se aplica a una versión exacta; cambiar el contenido requiere una nueva versión y revisión. Lo mismo rige para rúbricas, fuentes y documentos.
3. Una sesión guarda una copia lógica de su configuración al comenzar; cambiar preferencias después no altera esa sesión.
4. El estudiante puede seleccionar múltiples materias y subtemas, pero las preguntas deben respetar el alcance configurado.
5. El backend decide validez de respuestas, temporizadores, extensiones y transiciones.
6. Al perder conexión, el tiempo se pausa y la sesión se reanuda con el tiempo restante persistido. La desconexión se reconoce tras 30 s sin latido (latido cada 10 s) y la recuperación máxima es de 30 minutos.
7. El límite total impide iniciar nuevas preguntas. Una pregunta activa puede completarse según el límite individual y extensiones válidas.
8. La extensión individual es de 60 segundos por concesión. El máximo es 1 concesión por pregunta y la ventana para solicitarla es de 15 s. El nuevo límite es la hora de concesión + 60 s.
9. El modo `at_simulation_end` impide mostrar retroalimentación académica antes del cierre de la sesión.
10. Las transcripciones y evaluaciones se conservan 12 meses; el audio original no se persiste y el audio temporal se elimina al terminar la transcripción.
11. Los resultados no pueden editarse directamente por el estudiante. Las correcciones administrativas mantienen el resultado original y trazabilidad.
12. El plan adaptativo no sobrescribe el plan original; genera revisiones identificables.
13. El índice RAG debe permitir reconstruir qué documentos y fragmentos se utilizaron para una evaluación o explicación relevante.
14. Los registros de uso de IA no deben incluir audio original ni datos personales innecesarios.

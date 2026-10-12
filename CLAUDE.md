# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Estado del repositorio

Por ahora el repositorio contiene solo especificaciones. Todavía no hay código, gestor de paquetes ni comandos de build, lint o pruebas. Cuando exista el scaffolding (Next.js + TypeScript, FastAPI + Python, Docker para PostgreSQL y backend), añade aquí los comandos reales, incluido cómo ejecutar una sola prueba. No los inventes antes de que existan.

Toda la documentación está en español. Mantén ese idioma en specs, commits y textos de interfaz.

## Mapa de especificaciones

Las reglas de un mismo tema están repartidas entre varios archivos. Crúzalos antes de implementar:

- `README.md`: decisiones confirmadas (con los valores concretos de tiempo, cuotas, retención, escala, cuentas e infraestructura) y la **lista única de pendientes**. Hoy quedan tres: hosting del backend, proveedor de correo y proveedores de IA.
- `specs/01-functional-requirements.md`: requisitos `FR-xxx`.
- `specs/02-domain-model.md`: entidades, máquinas de estado (`SimulationSession`, `QuestionAttempt`, `ContentReport`, `StudyTask`) y reglas de integridad numeradas.
- `specs/03-architecture.md`: componentes, temporizadores, extensión, desconexión, voz por turnos, RAG y costos.
- `specs/05-acceptance-criteria.md`: criterios `AC-001`–`AC-035`. Cada tarea debe corresponder a alguno.
- `specs/06-voice-study-planning-rag.md`: detalle de voz, plan de estudio, RAG y responsive.
- `harness/quality-gates.md`: Gates 1–12 aplicables según el alcance (sesión = Gate 3, voz/privacidad = Gate 5, RAG = Gate 6, etc.).
- `docs/correcciones.md`: registro de correcciones y de las rondas de decisiones. `docs/index.html` es una vista HTML de las specs; si cambias una spec, revisa si también debe actualizarse.
- No existe `specs/04-*.md`. Si aparece uno, revísalo contra las decisiones confirmadas.

Si cambias una decisión, actualiza a la vez el README, `AGENTS.md`, las specs afectadas, los criterios de aceptación y `docs/correcciones.md`. Esos documentos repiten los mismos valores.

## Conceptos de arquitectura que cruzan varios documentos

- **Valores decididos como configuración, no constantes**: extensiones (60 s, oferta de 15 s que consume tiempo total, máximo 1), latido (10 s / caída a 30 s), `recovery_window` (30 min), pausa voluntaria, retención, cuotas. Se cargan desde configuración con el valor confirmado. Para pendientes sin valor, la configuración es obligatoria y sin valor por defecto.
- **Reloj de sesión en backend**:
  - La desconexión pausa el reloj de forma retroactiva desde el último latido.
  - El reloj de la pregunta se detiene cuando el backend recibe la respuesta, así que transcripción y evaluación no consumen tiempo.
  - `paused_disconnected` guarda `resume_state`.
  - Extensiones, respuestas y evaluaciones deben ser idempotentes ante solicitudes duplicadas o concurrentes.
  - La configuración se congela al iniciar.
  - Estados finales: `completed`, `expired` (no reanudada a tiempo) y `abandoned` (cierre voluntario).
- **Contenido versionado inmutable**: aprobar y publicar son actos distintos; publicar es una acción auditada. Quien crea o modifica una versión no puede aprobarla ni publicarla (AC-029). Solo versiones `published` entran en sesiones ordinarias, y solo documentos aprobados se indexan en pgvector.
- **Correcciones solo por adición**: `AssessmentCorrection` exige un reporte vinculado y conserva el resultado original. Los agregados se derivan del resultado vigente.
- **Evaluación oral**: cada criterio se puntúa de 0 a 100, se pondera según la rúbrica versionada y se convierte linealmente a 1,0–7,0 con un decimal (AC-034). Una falla técnica nunca se convierte en nota.
- **Proveedores detrás de interfaces**: LLM, transcripción, embeddings, síntesis de voz, correo y cola de tareas (tabla en PostgreSQL). Hasta la prueba de concepto se usan implementaciones falsas; la lógica de dominio no importa SDKs de proveedores. Se recomienda generar los tipos TypeScript del frontend desde el OpenAPI de FastAPI.
- **Plan de estudio determinista**: la prioridad es el peso de la materia × la brecha de desempeño reciente. Las revisiones adaptativas nunca sobrescriben el plan original.

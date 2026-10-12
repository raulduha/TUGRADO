# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Estado del repositorio

Hay especificaciones, el entorno Docker y el scaffolding del backend (FastAPI + Python 3.12 con uv) con un endpoint de salud. Todavía no hay frontend ni modelos de dominio. Cuando exista el frontend, añade aquí sus comandos; no los inventes antes.

## Entorno local (Docker)

```sh
cp .env.example .env                 # una vez; el compose falla si faltan variables
docker compose up -d --build         # db (PostgreSQL 17 + pgvector) y backend con recarga en caliente
docker compose exec db psql -U tugrado -d tugrado
docker compose down                  # conserva datos; `down -v` borra el volumen
```

- Backend: http://127.0.0.1:8000 (`/health`, `/health/db`, `/docs`). El código de `backend/app` se monta en el contenedor.
- `docker/postgres/init/` solo se ejecuta al crear el volumen por primera vez (hoy crea la extensión `vector`). El esquema se gestionará con Alembic, no con esos scripts.
- En Windows usa `127.0.0.1`, no `localhost`, en `DATABASE_URL`: `localhost` intenta IPv6 primero y la conexión tarda minutos.

## Backend (`backend/`)

Ejecutar desde `backend/`. Las pruebas y la app leen `DATABASE_URL` del `.env` de la raíz.

```sh
uv sync                                           # instala dependencias en backend/.venv
uv run pytest                                     # todas las pruebas (las integration necesitan la db arriba)
uv run pytest -m "not integration"                # sin PostgreSQL
uv run pytest tests/test_health.py::test_health   # una sola prueba
uv run ruff check . && uv run ruff format --check .
uv run uvicorn app.main:app --reload              # sin Docker
```

- `app/config.py` (`Settings`, pydantic-settings) es el único punto de entrada de configuración. Los campos sin valor por defecto son obligatorios y `create_app()` falla al arrancar si faltan. Los parámetros de negocio decididos (extensiones, latido, `recovery_window`, cuotas…) van aquí como campos obligatorios, con su valor confirmado en `.env.example`, no como constantes en el código.
- Las dependencias externas (por ejemplo, `get_engine`) se inyectan con `Depends`, para poder reemplazarlas en pruebas con `app.dependency_overrides`.
- Las pruebas que requieren PostgreSQL llevan `@pytest.mark.integration`.

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

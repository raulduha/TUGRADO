# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

## Estado del repositorio

Hay especificaciones, backend (FastAPI + Python 3.12 con uv: autenticación, suscripción, comentarios, dominio y persistencia de la simulación) y frontend (Next.js 16), desplegados en apruebatuexamen.cl. Producción, variables y despliegue: `docs/despliegue.md`. La simulación todavía no tiene endpoints ni pantallas.

## Entorno local (Docker)

```sh
cp .env.example .env                 # una vez; el compose falla si faltan variables
docker compose up -d --build         # db (PostgreSQL 18 + pgvector, igual que Neon) y backend con recarga en caliente
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
uv run alembic upgrade head                       # aplica migraciones (en Docker: docker compose exec backend alembic upgrade head)
uv run alembic revision --autogenerate -m "..."   # nueva migración; revísala antes de commitear
uv run alembic check                              # falla si los modelos y las migraciones divergen
```

Crear o promover un administrador (no hay registro público de administradores): `uv run python -m app.cli create-admin --email admin@ejemplo.cl`, o dentro de Docker `docker compose exec backend python -m app.cli create-admin --email …`. La contraseña se pide por consola o se lee de `ADMIN_PASSWORD`. Acceso sin suscripción para cuentas de prueba (FR-032): `python -m app.cli grant-access --email … --reason … --by …` y `revoke-access --email …`. En desarrollo los correos (verificación y recuperación) no se envían: aparecen en `docker compose logs backend`.

Las pruebas `integration` usan `TEST_DATABASE_URL` (base `tugrado_test`). La crean y migran solas, y vacían las tablas después de cada prueba.

- `app/config.py` (`Settings`, pydantic-settings) es el único punto de entrada de configuración. Los campos sin valor por defecto son obligatorios y `create_app()` falla al arrancar si faltan. Los parámetros de negocio decididos (extensiones, latido, `recovery_window`, cuotas…) van aquí como campos obligatorios, con su valor confirmado en `.env.example`, no como constantes en el código.
- Las dependencias externas (por ejemplo, `get_engine`) se inyectan con `Depends`, para poder reemplazarlas en pruebas con `app.dependency_overrides`.
- Las pruebas que requieren PostgreSQL llevan `@pytest.mark.integration`.

### Dominio de la simulación (`app/domain/simulation/`)

Lógica pura sin base de datos ni HTTP; `session.py` documenta las convenciones en su docstring. Lo que no es obvio:
- Cada operación recibe la hora del servidor (`at`, con zona horaria) y deben llegar en orden. Las pruebas usan `at(segundos)` y `keep_alive()` de `tests/domain/conftest.py`. Sin latidos durante 30 s, la sesión se pausa sola, así que en las pruebas hay que mantenerla viva.
- Todos los plazos son exclusivos: en el instante exacto del vencimiento la regla ya aplicó.
- Las transiciones por tiempo solo se consolidan hasta la última señal del cliente (latido o comando). Por eso la pausa por desconexión puede ser retroactiva sin deshacer nada. `sweep()` solo detecta desconexiones y vence recuperaciones; no avanza los demás temporizadores.
- `_sync_clocks()` es la única regla que decide qué relojes corren. El total se detiene en pausas, durante el procesamiento de la respuesta y tras agotarse.
- Los comandos del cliente llevan `request_id` para ser idempotentes.

### Persistencia (`app/persistence/`)

- Toda operación sobre una sesión pasa por `run_locked()`, que bloquea la fila con `SELECT … FOR UPDATE`, toma la hora **después** del bloqueo (así el dominio recibe las operaciones en orden), aplica el dominio y guarda.
- Si el dominio rechaza con `SessionRuleError`, igual se guardan las transiciones aplicadas antes del rechazo (por ejemplo, una pausa detectada). Con cualquier otra excepción se hace rollback.
- `session_event` es de solo adición, con `(session_id, seq)` único. `session_request` guarda el resultado de cada `request_id`.
- Las restricciones CHECK de los enums se declaran con `enum_column()` y `enum_check()` (`app/persistence/base.py`), no con `Enum(create_constraint=True)`: esta última opción hace que Alembic las duplique.

### Autenticación (`app/auth/`, `app/api/auth.py`, `app/api/deps.py`)

- Los errores de negocio heredan de `AppError` (`app/errors.py`) y se traducen a HTTP en un solo lugar (`app/api/errors.py`, tabla `STATUS_BY_CODE`). No captures errores en cada endpoint.
- Para proteger un endpoint, usa las anotaciones `CurrentUser` o `AdminUser`, o `Depends(require_role(...))`, de `app/api/deps.py`. No hay otra forma de autorizar.
- Sesión en la cookie HttpOnly `tugrado_session`. En la base de datos solo se guarda el hash SHA-256 del token, igual que en los enlaces de correo.
- `app/api/origin.py` rechaza con 403 las operaciones que modifican datos si el encabezado `Origin` no es el de `FRONTEND_BASE_URL`. Los clientes de prueba envían ese `Origin`.
- `AuthService` confirma sus propias transacciones (un intento fallido debe guardarse aunque se responda con error) y envía los correos **después** del commit.
- Las respuestas de registro, inicio de sesión y recuperación no revelan si un correo existe (AC-036): mantén ese contrato al agregar endpoints.
- En pruebas, el reloj (`get_clock`), el correo (`get_email_sender`) y la base (`get_engine`) se reemplazan con los fixtures `api`, `clock` y `outbox` de `tests/conftest.py`.
- `app/auth/data/common_passwords.txt` se generó a partir de SecLists; su origen está en el README de esa carpeta.

Toda la documentación está en español. Mantén ese idioma en specs, commits y textos de interfaz.

## Frontend (`frontend/`)

Next.js 16.4 con `cacheComponents` y `partialPrefetching`. **Lee `frontend/AGENTS.md` y la documentación incluida en `node_modules/next/dist/docs/` antes de escribir código**: esta versión cambia APIs que quizá conozcas de otra forma.

```sh
cp .env.example .env.local    # BACKEND_URL obligatoria (next.config.ts falla sin ella)
pnpm install
pnpm dev                      # http://localhost:3000; el backend debe estar arriba (Docker)
pnpm lint && pnpm typecheck   # typecheck corre next typegen (genera LayoutProps, etc.)
pnpm build
pnpm e2e                      # Playwright con el Chrome instalado; requiere la app levantada en :3000
pnpm e2e --project=movil e2e/responsive.spec.ts   # un proyecto o archivo
```

- El navegador solo habla con el frontend: `next.config.ts` reenvía `/api/*` a `BACKEND_URL`. Así la cookie de sesión es de primera parte y el backend ve `Origin: http://localhost:3000`. Abre la app en `localhost:3000`: con otra dirección (por ejemplo, la IP de red) el backend rechaza las operaciones por origen, y `next dev` bloquea sus recursos internos.
- Las llamadas pasan por `src/lib/api.ts`, que devuelve `{ok, status, data | error{code, message}}` con los códigos de error del backend.
- Las pantallas que leen `?token=` o `?next=` usan `useSearchParams` dentro de `<Suspense>` (exigido por Cache Components). `?next=` pasa por `safeNext()` para evitar redirecciones abiertas.
- **Cache Components conserva hasta 3 páginas visitadas con su estado** (React `<Activity>`; ver `docs/01-app/02-guides/preserving-ui-state.md`). No redirijas desde un `useEffect` según un estado de "éxito": al volver a la página el efecto se repite (eso causó un bucle entre login y panel). Navega dentro del envío y limpia los datos del usuario al cerrar sesión.
- Los formularios usan `useActionState` en componentes de cliente. El backend es la autoridad: las páginas con sesión usan `useRequireUser()` (`src/lib/use-user.ts`), que consulta `/api/auth/me` y redirige a `/iniciar-sesion` si responde 401, y el encabezado compartido `AppHeader`.
- Suscripción: sin acceso, el panel lleva a `/suscripcion` (el estudio exige suscripción, cortesía o rol de administrador). Páginas: `/suscripcion`, `/suscripcion/retorno` (consulta el estado real con `/billing/subscription/sync`) y `/suscripcion/simulador`, que reemplaza a Mercado Pago solo con `BILLING_PROVIDER=fake`.
- Botones: `buttonStyles` y `ButtonLink` de `src/components/button.tsx`; no repitas clases de botón.
- Tema claro único: los colores son tokens en `src/app/globals.css` (`bg-brand`, `text-muted`, `bg-brand-soft`…). Las ilustraciones e íconos son SVG propios en `src/components/illustrations.tsx`.
- El panel no muestra cifras inventadas: el progreso sin datos se muestra como estado vacío.
- Gate 10: `e2e/responsive.spec.ts` recorre las pantallas públicas en 390, 768 y 1280 px y falla si hay desplazamiento horizontal. `e2e/student.spec.ts` hace el recorrido real de un estudiante: el token de verificación se lee del log del backend (`docker compose logs`) y las cuentas `e2e-*@ejemplo.cl` se borran al terminar.

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

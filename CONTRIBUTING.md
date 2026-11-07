# Cómo trabajamos

Guía corta para colaborar en Aprueba tu examen. Las reglas de negocio están en `AGENTS.md` y
`specs/`; los comandos y la arquitectura, en `CLAUDE.md`. Aquí va el día a día.

## Ramas

```
feat/…, fix/…, docs/…  ──PR──▶  development  ──PR (release)──▶  main  ──▶  producción
```

| Rama | Para qué | Quién escribe |
| --- | --- | --- |
| `main` | Lo que está en producción. Render (backend) y Vercel (frontend) despliegan solos cada commit que entra aquí. | Solo PRs desde `development`. |
| `development` | Integración: lo terminado y revisado que aún no sale a producción. Rama base de todo PR. | Solo PRs desde ramas de trabajo. |
| `feat/…`, `fix/…`, `docs/…`, `refactor/…`, `chore/…` | Una tarea chica. Se borra al mergear. | Quien hace la tarea. |

- **Nombre de la rama:** tipo + qué hace, en español y con guiones: `feat/rosco-legal`,
  `fix/prueba-gratis-fecha`, `refactor/alias-db-reloj`.
- **Una rama, un tema.** Si un PR mezcla dos cosas, se separa en dos.
- **Salir a producción:** PR de `development` a `main` con título `Release AAAA-MM-DD` y la
  lista de PRs que incluye. Las migraciones de Alembic se aplican solas al desplegar Render.
- **Arreglo urgente en producción:** rama `fix/…` desde `main`, PR a `main` y después el
  mismo cambio a `development` (merge de `main` en `development`).

## Commits y PRs

- Commits en español, en imperativo y con el porqué cuando no es obvio: «Cobrar la suscripción
  con Flow», «Pedir el correo de la cuenta de Mercado Pago al suscribirse».
- El PR usa la plantilla (`.github/pull_request_template.md`): qué cambia, cómo revisarlo,
  pruebas y specs.
- Se mergea con *merge commit* (no squash) y se borra la rama.

## Antes de mergear: los controles

GitHub Actions no corre solo (la cuenta no paga minutos): los controles se corren en local.

```sh
docker compose up -d db        # la base de datos de desarrollo
scripts/verificar.sh           # backend (ruff, migraciones, pytest) y frontend (lint, tipos, build)
```

Si el cambio toca algo que el estudiante o el administrador ven, corre también las e2e:

```sh
docker compose up -d --build backend
cd frontend && pnpm build && pnpm start      # en otra terminal
pnpm e2e --workers=1
```

## Cómo revisar un PR

1. Lee la descripción y el requisito (`FR-…`/`AC-…`) que cita.
2. Empieza por las pruebas: dicen qué comportamiento se espera.
3. Revisa que el backend sea la autoridad (permisos, tiempo, resultados) y que no se publique
   contenido sin revisión de otra persona.
4. Pide cambios con comentarios concretos; aprueba cuando los controles pasan.

## Datos y secretos

- Los secretos van en `.env` (local) y en Render/Vercel (producción). Nunca en el repositorio:
  es público.
- Producción usa Neon. No se borran ni modifican datos de producción sin acordarlo antes.

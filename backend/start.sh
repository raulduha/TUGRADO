#!/bin/sh
# Arranque en producción (Render): aplica las migraciones y luego inicia la API.
# Las migraciones de Alembic son idempotentes: si no hay cambios, no hacen nada.
set -e
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --proxy-headers --forwarded-allow-ips='*'

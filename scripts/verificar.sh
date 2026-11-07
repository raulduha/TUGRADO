#!/usr/bin/env bash
# Controles locales antes de mergear un PR: los mismos que .github/workflows/ci.yml, que solo
# se corre a mano para no gastar minutos de GitHub Actions. Requiere la base de Docker arriba:
#   docker compose up -d db
#
# Uso (desde la raíz del repo):
#   scripts/verificar.sh            # backend y frontend
#   scripts/verificar.sh backend    # solo uno de los dos
#   scripts/verificar.sh frontend
#
# Las pruebas e2e van aparte porque necesitan la app levantada (ver CONTRIBUTING.md).

set -euo pipefail
cd "$(dirname "$0")/.."

que="${1:-todo}"

paso() { printf '\n\033[1m▶ %s\033[0m\n' "$*"; }

if [[ "$que" == "todo" || "$que" == "backend" ]]; then
  paso "Backend: dependencias, estilo, migraciones y pruebas"
  (
    cd backend
    uv sync --locked
    uv run ruff check .
    uv run ruff format --check .
    uv run alembic upgrade head
    uv run alembic check
    uv run pytest -q
  )
fi

if [[ "$que" == "todo" || "$que" == "frontend" ]]; then
  paso "Frontend: dependencias, lint, tipos y build"
  (
    cd frontend
    pnpm install --frozen-lockfile
    pnpm lint
    pnpm typecheck
    BACKEND_URL=http://127.0.0.1:8000 pnpm build
  )
fi

paso "Todo en orden ✔"

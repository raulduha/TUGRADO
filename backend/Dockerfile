FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.8 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Dependencias primero, para aprovechar la caché de capas.
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked

RUN useradd --create-home --uid 1000 app
USER app

EXPOSE 8000
# Producción: start.sh aplica las migraciones y arranca la API en $PORT (8000 en local).
# En desarrollo, docker-compose reemplaza este comando por uvicorn con recarga.
CMD ["sh", "start.sh"]

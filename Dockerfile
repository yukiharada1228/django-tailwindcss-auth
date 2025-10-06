FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-trixie-slim

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "gunicorn", "config.asgi:application", "-k", "uvicorn_worker.UvicornWorker"] 
FROM node:20-alpine AS frontend-builder

WORKDIR /app

COPY package.json package-lock.json ./
COPY tailwind.config.js ./tailwind.config.js
COPY static/css ./static/css
COPY templates ./templates

RUN npm ci --no-audit --no-fund
RUN npm run build

FROM ghcr.io/astral-sh/uv:0.8.22-python3.12-trixie-slim

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# アプリケーションコードをコピー
COPY . .

# Tailwind のビルド成果物を取り込み
COPY --from=frontend-builder /app/static/css/output.css ./static/css/output.css

CMD ["sh", "-c", "uv run python manage.py migrate --noinput && uv run python manage.py collectstatic --noinput && uv run gunicorn config.asgi:application -k uvicorn_worker.UvicornWorker --bind 0.0.0.0:8000"] 
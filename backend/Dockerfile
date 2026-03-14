FROM python:3.12-slim

# uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# install dependencies first (for caching)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

COPY . .

# run migrations and start the app
# NB: In production, you'd usually run migrations in a separate CI/CD step
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn main:app --host 0.0.0.0 --port 8000"]
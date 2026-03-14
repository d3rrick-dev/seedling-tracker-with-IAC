.PHONY: dev build down logs clean migrate

# Start everything
dev:
	docker compose up --build

# Stop everything
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Run migrations manually if needed
migrate:
	docker compose exec app uv run alembic revision --autogenerate -m "new_migration"
	docker compose exec app uv run alembic upgrade head

# Clean up volumes (Warning: deletes data)
clean:
	docker compose down -v
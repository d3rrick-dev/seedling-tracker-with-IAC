.PHONY: dev build migrate-local tf-apply-docker

# Build the image from root
build:
	docker build -t seedling-api:latest .

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

run-local:
	uv run uvicorn app.main:app --reload

# Clean up volumes (Warning: deletes data)
clean:
	docker compose down -v

# Terraform
tf-init:
	cd ../infra/docker-local && terraform init

tf-apply:
	cd ../infra/docker-local && terraform apply
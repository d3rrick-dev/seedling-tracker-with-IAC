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


# --- K8s variables
CLUSTER_NAME=seedling-cluster
IMAGE_NAME=seedling-api:latest
K8S_DIR=infra/k8s-kind
BACKEND_DIR=backend

# Rebuilding image and pushes it into the Kind node
k8s-build-load:
	docker build -t $(IMAGE_NAME) ./$(BACKEND_DIR)
	kind load docker-image $(IMAGE_NAME) --name $(CLUSTER_NAME)

# run terraform to update the cluster
k8s-apply:
	cd $(K8S_DIR) && terraform apply -auto-approve -lock=false

# fukll pipeline
k8s-up: k8s-build-load k8s-apply
	@echo "Deployment complete. Port-forwarding now..."
	kubectl port-forward svc/api-service 8080:80 -n farming-platform

# stop the API pods
stop:
	kubectl scale deployment seedling-api --replicas=0 -n farming-platform

# starts 2 replicas of the API (inline with replicas in app.tf)
start:
	kubectl scale deployment seedling-api --replicas=2 -n farming-platform

delete:
	kubectl delete deployment seedling-api -n farming-platform

# Stops the whole stack
stop-all:
	kubectl scale deployment seedling-api --replicas=0 -n farming-platform
	kubectl scale deployment db-deployment --replicas=0 -n farming-platform

# --- AWS / LocalStack Targets ---

aws-init:
	cd infra/aws && terraform init

aws-apply:
	cd infra/aws && terraform apply -auto-approve
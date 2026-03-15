
## Architecture & System Design

The Seedling Management System is built using a **Cloud-Native, Event-Driven Architecture**. It leverages FastAPI for the core logic, SQLAlchemy for persistence, and LocalStack to emulate AWS services locally.

### Component Overview
* **API Layer:** FastAPI provides a RESTful interface for seedling lifecycle management and buyer searches.
* **Service Layer:** Contains business logic, maturity calculations, and interacts with S3/SQS.
* **Data Layer:** PostgreSQL (via SQLAlchemy/Alembic) stores seedling metadata and status.
* **Infrastructure:** * **LocalStack:** Emulates AWS S3 (Image storage) and SQS (Background processing).
    * **KinD (Kubernetes in Docker):** Orchestrates the containerized application.
* **Testing:** Behave (BDD) executes End-to-End scenarios against the live `TestClient`.

---

## End-to-End (E2E) Flow

The following flow represents the lifecycle of a seedling during a BDD test run:

### 1. Seedling Creation (POST)
* **User Action:** Sends a POST request to `/seedlings/` with crop type and quantity.
* **System Action:** FastAPI validates the payload, generates a unique ID (auto-incrementing), and saves the metadata to the PostgreSQL database.
* **Result:** Returns `200 OK` with the new Seedling ID.

### 2. Media Upload & Processing (POST)
* **User Action:** Sends a multipart file upload to `/seedlings/{id}/upload-photo/`.
* **System Action:** * The service mocks/uploads the raw image to an **S3 Bucket**.
    * A message is sent to **SQS** to trigger background thumbnail generation.
* **Result:** Returns status `Uploaded & Processing`.

### 3. Verification & Search (GET)
* **User Action:** The BDD engine performs a "Search" via `/buyers/search?query_date=...`.
* **System Action:** * The test overrides the service mock to ensure the "Auto-Incremented" ID from step 1 matches the search results.
    * The API queries the database for seedlings matching the planting date and status.
* **Validation:** The BDD `Then` step confirms the image URLs contain the correct S3 paths and the seedling status is "Growing".

---

## Testing Strategy

Following the **Testing Pyramid** approach with a heavy emphasis on **Behavioral Testing**:

1.  **Unit Tests (Pytest):** Validate isolated functions like date calculations and data parsing.
2.  **BDD Tests (Behave):** Validate the "Business Value" by simulating real user interactions across multiple API endpoints.
3.  **Mocking Strategy:** We use `unittest.mock.patch` to isolate external dependencies (AWS) during CI, while maintaining the integrity of the Database and Routing layers.

### Terraform
`providers.tf` - Defines which cloud/tooling you are using (Docker, Kubernetes, etc.) and the required versions.

`main.tf` -  The "orchestrator." This is where you define your primary resources (Containers, Networks, Volumes).

`variables.tf` -  Defines input variables (e.g., db_password, app_port). This keeps your code flexible without hardcoding values.

`outputs.tf` -  Defines what information to show you after deployment (e.g., Swagger UI docs).

`terraform.tfvars` -  for storing the actual values for your variables.

### Build image
``` bash
docker build -t seedling-api:latest .
```

### Terraform Init & Apply
``` bash
cd terraform
terraform init
terraform apply

#incase you updated the .tf values
terraform init
terraform plan

```

### testing App
```bash 
# create data
curl --location 'http://localhost:8000/seedlings' \
--header 'Content-Type: application/json' \
--data '{
     "crop_type":"Mangoes",
     "quantity": 100,
     "location": "Embu",
     "planting_date": "2026-02-14"
}'

# get crops data
curl --location 'http://localhost:8000/buyers/search?query_date=2026-02-14'

```

### Cons
State Management -  a `terraform.tfstate` file. For tracking infra changes.

Provider Ecosystem - Swappable infras' "Docker" provider for "AWS" or "Azure" with minimal changes to the logic.

Separation of Concerns - Treating your DB and App as resources rather than just "scripts."


### Adding NGINX
```bash
#Update endpoint
http://localhost/seedlings
http://localhost/buyers/search
http://localhost/docs
```


# Command Reference

This guide contains the common commands used for development, testing, infrastructure, and deployment.

---

## Dependency & Environment (uv)
Used for fast Python package management and virtual environments.

| Command | Description |
| :--- | :--- |
| `uv sync --all-extras --dev` | Install all dependencies and dev tools |
| `uv add <package>` | Add a new production package |
| `uv add --dev behave` | Add a development-only package |
| `uv run <command>` | Run a command (e.g., `uv run main.py`) inside the environment |
| `uv lock` | Update the `uv.lock` file |
| `uv cache clean` | Clear the global uv cache |

---

## Database & Migrations (Alembic)
Used to manage the SQLAlchemy schema and PostgreSQL migrations.

| Command | Description |
| :--- | :--- |
| `uv run alembic init alembic` | Initialize the migrations folder |
| `uv run alembic revision --autogenerate -m "msg"` | Generate a new migration script |
| `uv run alembic upgrade head` | Apply all pending migrations to the DB |
| `uv run alembic downgrade -1` | Revert the last applied migration |
| `uv run alembic current` | Show the current migration revision |

---

## Testing & Troubleshooting
Commands for running the BDD scenarios and unit tests.

| Command | Description |
| :--- | :--- |
| `uv run behave` | Run all Gherkin/BDD tests |
| `uv run behave --no-capture` | Run BDD tests with live print output |
| `uv run behave features/file.feature` | Run a specific feature file |
| `uv run pytest` | Run all standard unit and integration tests |
| `uv run pytest --cov=app` | Run tests with a code coverage report |

---

## Infrastructure (Terraform & LocalStack)
Used to provision AWS-like resources (S3, SQS) locally.

| Command | Description |
| :--- | :--- |
| `terraform init` | Initialize Terraform providers and state |
| `terraform plan` | Preview infrastructure changes |
| `terraform apply -auto-approve` | Create S3 buckets and SQS queues |
| `terraform destroy` | Tear down all local infrastructure |
| `aws --endpoint-url=http://localhost:4566 s3 ls` | List S3 buckets in LocalStack |

---

## Local Kubernetes (KinD)
Used for creating and managing the local Kubernetes cluster.

| Command | Description |
| :--- | :--- |
| `kind create cluster --name seedling-cluster --config kind-config.yaml` | Spin up the cluster |
| `kind delete cluster --name seedling-cluster` | Destroy the cluster |
| `kind load docker-image seedling-app:latest --name seedling-cluster` | Sideload a local image into KinD |
| `kind get clusters` | List all active KinD clusters |

---

## Orchestration (kubectl)
Used to manage resources inside the Kubernetes cluster.

| Command | Description |
| :--- | :--- |
| `kubectl apply -f k8s/` | Deploy all manifests in the k8s folder |
| `kubectl get pods` | View status of all running pods |
| `kubectl logs -f <pod_name>` | Stream logs from a specific pod |
| `kubectl describe pod <pod_name>` | Debug a pod (check events/errors) |
| `kubectl port-forward service/seedling-service 8080:80` | Access the API locally at localhost:8080 |
| `kubectl get secret` | View available secrets in the namespace |

---

## Nuclear Reset
If you need to wipe everything and start fresh:
```bash
# Delete the cluster, destroy infra, and wipe local test DB
kind delete cluster --name seedling-cluster && terraform destroy -auto-approve && rm test.db



### Future Scaling (AWS Roadmap)
While the current version uses LocalStack, the architecture is designed to port directly to AWS:

1. **Compute:** Migrate FastAPI from KinD to **AWS ECS Fargate** for serverless container orchestration.
2. **Storage:** Transition S3 mocks to a production **Amazon S3** bucket with Lifecycle Policies for old media.
3. **Database:** Move from local PostgreSQL to **Amazon RDS** with Multi-AZ deployment for high availability.
4. **Security:** Implement **AWS IAM Roles** for service-to-service communication, eliminating the need for local credentials.
5. **Monitoring:** Integrate **AWS CloudWatch** for centralized logging and performance metrics.
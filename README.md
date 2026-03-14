

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

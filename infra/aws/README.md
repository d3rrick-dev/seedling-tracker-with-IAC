

```bash

terraform init
terraform apply -auto-approve


# restarting localstack
localstack stop; localstack start -d

$ awslocal rds describe-db-instances
{
    "DBInstances": [
        {
            "DBInstanceIdentifier": "terraform-20260314223132611500000001",
            "DBInstanceClass": "db.t3.micro",
            "Engine": "postgres",
            "DBInstanceStatus": "available",
            "MasterUsername": "postgres",
            "DBName": "seedling_db",
            "Endpoint": {
                "Address": "localhost.localstack.cloud",
                "Port": 4510
            },

```
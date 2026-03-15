from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    s3_endpoint: str = "http://host.docker.internal:4566"
    s3_bucket: str = "seedling-assets"
    sqs_url: str = "http://host.docker.internal:4566/000000000000/plant-photo-processing"
    aws_region: str = "us-east-1"
    aws_access_key: str = "test"
    aws_secret_key: str = "test"
    # database_url: str = "postgresql://postgres:password@host.docker.internal:4510/seedling_db"
    database_url: str = "postgresql://admin:supersecret@localhost:5432/farming_db"

settings = Settings()
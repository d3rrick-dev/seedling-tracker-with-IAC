import json
import boto3
from ..core.config import settings

def get_sqs_client():
    return boto3.client(
        'sqs',
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=settings.aws_region
    )

def notify_worker(seedling_id: int, filename: str):
    client = get_sqs_client()
    message = {
        "seedling_id": seedling_id,
        "filename": filename
    }
    client.send_message(
        QueueUrl=settings.sqs_url,
        MessageBody=json.dumps(message)
    )
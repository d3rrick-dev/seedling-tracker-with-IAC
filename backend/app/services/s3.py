import boto3
from botocore.client import Config
from ..core.config import settings

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
        region_name=settings.aws_region,
        config=Config(s3={'addressing_style': 'path'}),
        use_ssl=False,
        verify=False
    )

def upload_to_s3(file_obj, filename, content_type):
    client = get_s3_client()
    client.upload_fileobj(
        file_obj, 
        settings.s3_bucket, 
        filename,
        ExtraArgs={"ContentType": content_type}
    )
    return f"{settings.s3_endpoint}/{settings.s3_bucket}/{filename}"
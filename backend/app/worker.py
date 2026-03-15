import io
import json
import logging
from PIL import Image

from .core.config import settings
from .database import SessionLocal
from .repositories.seedling_repo import SeedlingRepository
from .services.s3 import get_s3_client
from .services.sqs import get_sqs_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

s3_client = get_s3_client()
sqs_client = get_sqs_client()

def process_image(filename: str, seedling_id: int):
    db = SessionLocal()
    repo = SeedlingRepository(db)
    
    try:
        response = s3_client.get_object(Bucket=settings.s3_bucket, Key=filename)
        
        with Image.open(io.BytesIO(response['Body'].read())) as img:
            img_format = img.format 
            img.thumbnail((128, 128))
            
            buf = io.BytesIO()
            img.save(buf, format=img_format)
            buf.seek(0)
            
            thumb_key = f"thumbnails/{filename}"
            s3_client.put_object(
                Bucket=settings.s3_bucket, 
                Key=thumb_key, 
                Body=buf, 
                ContentType=response['ContentType']
            )
            
            thumb_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{thumb_key}"
            updated = repo.update_image_urls(seedling_id, thumb_url=thumb_url)
            
            if updated:
                logger.info(f"Success: Thumbnail updated for Seedling {seedling_id}")
                return True
            else:
                logger.warning(f"Seedling {seedling_id} not found in DB")
                return False
            
    except Exception as e:
        logger.error(f"Error processing {filename}: {e}")
        return False
    finally:
        db.close()

def run_worker():
    logger.info("Worker started. Polling SQS...")
    while True:
        resp = sqs_client.receive_message(
            QueueUrl=settings.sqs_url, 
            MaxNumberOfMessages=1, 
            WaitTimeSeconds=10
        )
        
        for msg in resp.get("Messages", []):
            try:
                body = json.loads(msg["Body"])
                if process_image(body.get('filename'), body.get('seedling_id')):
                    sqs_client.delete_message(
                        QueueUrl=settings.sqs_url, 
                        ReceiptHandle=msg["ReceiptHandle"]
                    )
            except Exception as e:
                logger.error(f"Worker loop error: {e}")

if __name__ == "__main__":
    run_worker()
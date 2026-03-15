from sqlalchemy.orm import Session
from .s3 import upload_to_s3
from .sqs import notify_worker
from ..repositories.seedling_repo import SeedlingRepository
from datetime import timedelta
from datetime import date

class SeedlingService:
    def __init__(self, db: Session):
        self.repo = SeedlingRepository(db)

    def register_new_seedling(self, seedling_data):
        return self.repo.create(seedling_data)

    def handle_photo_upload(self, seedling_id: int, file):
        seedling = self.repo.get_by_id(seedling_id)
        if not seedling:
            return None

        file_url = upload_to_s3(file.file, file.filename, file.content_type)
        self.repo.update_image_urls(seedling_id, image_url=file_url)
        notify_worker(seedling_id, file.filename)
        return file_url

    def get_seedlings_with_status(self, query_date: date):
        seedlings = self.repo.get_all()
        
        for s in seedlings:
            ready_date = s.planting_date + timedelta(days=s.maturity_days)
            days_remaining = (ready_date - query_date).days
            s.ready_date = ready_date
            s.days_remaining = max(0, days_remaining)
            s.status = "Ready" if days_remaining <= 0 else "Growing"
            
        return seedlings
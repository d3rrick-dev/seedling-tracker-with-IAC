from sqlalchemy.orm import Session
from .. import schemas
from ..models import plant
class SeedlingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, seedling_id: int):
        return self.db.query(plant.Seedling).filter(plant.Seedling.id == seedling_id).first()

    def create(self, seedling_data: schemas.SeedlingCreate):
        db_seedling = plant.Seedling(**seedling_data.model_dump())
        self.db.add(db_seedling)
        self.db.commit()
        self.db.refresh(db_seedling)
        return db_seedling

    def update_image_urls(self, seedling_id: int, image_url: str = None, thumb_url: str = None):
        seedling = self.get_by_id(seedling_id)
        if image_url:
            seedling.image_url = image_url
        if thumb_url:
            seedling.thumbnail_url = thumb_url
        self.db.commit()
        return seedling

    def get_all(self):
        return self.db.query(plant.Seedling).all()
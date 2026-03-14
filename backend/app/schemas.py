from pydantic import BaseModel
from datetime import date

class SeedlingBase(BaseModel):
    crop_type: str
    quantity: int
    location: str
    planting_date: date

class SeedlingCreate(SeedlingBase):
    pass

class SeedlingOut(SeedlingBase):
    id: int
    class Config:
        from_attributes = True
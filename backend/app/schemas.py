from pydantic import BaseModel
from pydantic import ConfigDict, BaseModel
from datetime import date
from typing import Optional

class SeedlingBase(BaseModel):
    crop_type: str
    quantity: int
    location: str
    planting_date: date

class SeedlingCreate(SeedlingBase):
    pass

class SeedlingOut(SeedlingBase):
    id: int
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class SeedlingSearchOut(SeedlingOut):
    ready_date: date
    days_remaining: int
    status: str
    model_config = ConfigDict(from_attributes=True)
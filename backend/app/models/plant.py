from sqlalchemy import Column, Integer, String, Date
from ..database import Base
import datetime

class Seedling(Base):
    __tablename__ = "seedlings"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String)
    quantity = Column(Integer)
    location = Column(String)
    planting_date = Column(Date, default=datetime.date.today)
    image_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)

    @property
    def maturity_days(self):
        return 150 if self.crop_type.lower() == "avocado" else 90
from sqlalchemy import Column, Integer, String, Date, Float
from .database import Base
import datetime

class Seedling(Base):
    __tablename__ = "seedlings"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String)
    quantity = Column(Integer)
    location = Column(String) #consider a proper geo-data
    planting_date = Column(Date, default=datetime.date.today)

    @property
    def maturity_days(self):
        # Avocado 150 days (5 months), Mango 90 days (3 months)
        return 150 if self.crop_type.lower() == "avocado" else 90
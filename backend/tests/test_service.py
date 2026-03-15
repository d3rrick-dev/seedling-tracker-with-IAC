from app.services.seedling_service import SeedlingService
from app.schemas import SeedlingCreate
from datetime import date
from unittest.mock import MagicMock

def test_register_new_seedling_calls_repo(mock_repo):

    service = SeedlingService(db=MagicMock())
    service.repo = mock_repo
    
    data = SeedlingCreate(
        crop_type="Tomato", quantity=50, location="Limuru", 
        planting_date=date(2024, 1, 1), maturity_days=60
    )

    service.register_new_seedling(data)
    mock_repo.create.assert_called_once_with(data)
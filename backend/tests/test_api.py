from app.main import app
from app.database import get_db
from unittest.mock import MagicMock

def override_get_db():
    try:
        yield MagicMock()
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

def test_create_seedling_behavior(client, mocker):
    mock_seedling_response = {
        "id": 99,
        "crop_type": "Kale",
        "quantity": 100,
        "location": "Eldoret",
        "planting_date": "2024-02-20",
        "maturity_days": 45,
        "image_url": None,
        "thumbnail_url": None
    }

    mocker.patch(
        "app.services.seedling_service.SeedlingService.register_new_seedling", 
        return_value=mock_seedling_response
    )

    payload = {
        "crop_type": "Kale",
        "quantity": 100,
        "location": "Eldoret",
        "planting_date": "2024-02-20",
        "maturity_days": 45
    }

    response = client.post("/seedlings/", json=payload)

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 99
    assert data["crop_type"] == "Kale"
    assert data["location"] == "Eldoret"


def test_search_seedlings_logic(client):
    response = client.get("/buyers/search/?query_date=2024-08-17")
    
    assert response.status_code == 200
    results = response.json()
    
    if len(results) > 0:
        assert "days_remaining" in results[0]
        assert "status" in results[0]
        assert results[0]["status"] in ["Growing", "Ready"]
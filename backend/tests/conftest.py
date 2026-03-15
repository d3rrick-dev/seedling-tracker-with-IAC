import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def mock_repo():
    """Mocks the SeedlingRepository."""
    return MagicMock()

@pytest.fixture
def client():
    """FastAPI TestClient for behavioral tests."""
    return TestClient(app)
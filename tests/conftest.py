import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_item():
    return {
        "id": 1,
        "name": "Test Item",
        "price": 10.0,
        "is_offer": False
    }
    
@pytest.fixture
def sample_product():
    return {
        "id": 1,
        "name": "Test Product",
        "price": 10.0,
        "is_offer": False
    }

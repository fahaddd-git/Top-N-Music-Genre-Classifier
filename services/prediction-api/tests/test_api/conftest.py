import pytest
from fastapi.testclient import TestClient
from prediction_api.app import app


@pytest.fixture
def client() -> TestClient:
    """Mock client"""
    return TestClient(app)

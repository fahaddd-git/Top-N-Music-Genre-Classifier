import pytest
from fastapi.testclient import TestClient
from prediction_api.app import app


@pytest.fixture
def client() -> TestClient:
    """Mock client"""
    with TestClient(app) as test_client:
        yield test_client

import pytest
from fastapi.testclient import TestClient
from prediction_api.app import app


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """Mock FastAPI client, see: https://fastapi.tiangolo.com/tutorial/testing"""
    with TestClient(app) as test_client:
        yield test_client

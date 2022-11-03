import pytest
from fastapi.testclient import TestClient
from prediction_api.app import _Settings, app, get_settings
from prediction_api.config import ENVIRONMENT


@pytest.fixture
def client() -> TestClient:
    """Mock client"""

    def override_dependency():
        _Settings.environment = ENVIRONMENT.DEVELOPMENT
        return _Settings

    app.dependency_overrides[get_settings] = override_dependency
    with TestClient(app) as test_client:
        yield test_client

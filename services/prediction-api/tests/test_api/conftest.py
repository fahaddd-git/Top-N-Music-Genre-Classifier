from unittest.mock import MagicMock

import numpy as np
import pytest
from fastapi.testclient import TestClient
from prediction_api.app import app

DEPENDENCY_MODULE_PATH = "prediction_api.dependencies"


@pytest.fixture()
def patch_dependencies(monkeypatch):
    random_probabilities = [
        [0.0927, 0.2683, 0.1282, 0.0623, 0.0345, 0.0043, 0.2325, 0.0697, 0.0009, 0.1065],
        [0.4735, 0.0282, 0.0713, 0.1054, 0.0514, 0.0306, 0.0952, 0.0064, 0.0370, 0.1009],
    ]
    mock_tensorflow_model = MagicMock(predict=lambda: np.array(random_probabilities))

    labels_to_str = {
        0: "disco",
        1: "country",
        2: "rock",
        3: "pop",
        4: "jazz",
        5: "metal",
        6: "blues",
        7: "reggae",
        8: "classical",
        9: "hiphop",
    }
    monkeypatch.setattr("prediction_api.dependencies", "get_model", mock_tensorflow_model)
    monkeypatch.setattr("prediction_api.dependencies", "get_label_map", lambda: labels_to_str)


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    """Mock FastAPI client, see: https://fastapi.tiangolo.com/tutorial/testing"""
    with TestClient(app) as test_client:
        yield test_client

from fastapi import status
from fastapi.testclient import TestClient


def test_content_header_missing_returns_411(test_client: TestClient):
    response = test_client.post("/api/predict-genres", headers={"content-length": ""})
    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert response.json() == {"detail": "Missing content-length header."}


def test_content_too_large_returns_413(test_client: TestClient):
    response = test_client.post("/api/predict-genres", headers={"content-length": str(1024**5)})
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert response.json() == {"detail": "Content too large."}

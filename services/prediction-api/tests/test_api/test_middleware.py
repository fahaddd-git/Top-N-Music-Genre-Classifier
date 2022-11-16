from fastapi import status
from fastapi.testclient import TestClient

# The tests in this file follow the formatting suggested by FastAPI. Adapted from:
#  URL: https://fastapi.tiangolo.com/tutorial/testing
#  Date: 11/16/22


def test_content_header_missing_returns_411(test_client: TestClient):
    response = test_client.post("/api/predict-genres", headers={"content-length": ""})
    assert response.status_code == status.HTTP_411_LENGTH_REQUIRED
    assert response.json() == {"detail": "Missing content-length header."}


def test_content_too_large_returns_413(test_client: TestClient):
    response = test_client.post("/api/predict-genres", headers={"content-length": str(1024**5)})
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert response.json() == {"detail": "Content too large."}

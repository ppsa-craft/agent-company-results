import pytest
from fastapi.testclient import TestClient
from services.data_ingest.src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "data-ingest"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "vnstock Data Ingest Service"}
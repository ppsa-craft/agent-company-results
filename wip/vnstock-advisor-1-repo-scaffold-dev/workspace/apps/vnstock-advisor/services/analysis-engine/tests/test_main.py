import pytest
from fastapi.testclient import TestClient
from services.analysis_engine.src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "analysis-engine"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "vnstock Analysis Engine Service"}
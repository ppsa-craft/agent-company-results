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


def test_analyze_endpoint_placeholder():
    """Test the /analyze endpoint with placeholder response"""
    response = client.post("/analyze", json={
        "symbol": "VNM",
        "timeframe": "1D",
        "open": 100.0,
        "high": 105.0,
        "low": 99.0,
        "close": 102.0,
        "volume": 1000000,
        "source": "manual"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "VNM"
    assert data["timeframe"] == "1D"
    assert "analysis" in data
    assert data["analysis"]["ma_20"] == 100.0
    assert data["analysis"]["ma_50"] == 95.0
    assert data["analysis"]["rsi"] == 50.0
    assert data["analysis"]["signal"] == "neutral"
    assert "note" in data


def test_analysis_engine_health_status():
    """Test that the service returns proper health status"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "analysis-engine"
    assert data["status"] == "healthy"


def test_analysis_engine_service_info():
    """Test service information endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "vnstock Analysis Engine Service" in data["message"]
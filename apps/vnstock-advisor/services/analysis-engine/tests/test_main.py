import pytest
from fastapi.testclient import TestClient

# Fix import path for the app
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from main import app

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
    assert "vnstock Analysis Engine Service" in response.json()["message"]


def test_analyze_endpoint_placeholder():
    """Test the /analyze endpoint with real indicator computation"""
    import datetime
    response = client.post("/analyze", json={
        "symbol": "VNM",
        "timeframe": "1D",
        "open": "100.0",
        "high": "105.0",
        "low": "99.0",
        "close": "102.0",
        "volume": 1000000,
        "source": "manual",
        "time": datetime.datetime.now().isoformat()
    })
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "VNM"
    assert data["timeframe"] == "1D"
    assert "indicators" in data
    assert "warnings" in data
    # With only 1 data point, most indicators will be None (insufficient data)
    # but the response structure should be correct
    indicators = data["indicators"]
    assert "sma20" in indicators
    assert "sma50" in indicators
    assert "rsi14" in indicators
    assert "macd" in indicators
    assert "vwap" in indicators
    assert "volume_sma" in indicators
    assert "volume_ratio" in indicators
    assert "roc10" in indicators
    assert "atr14" in indicators
    assert "obv" in indicators


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


def test_analyze_invalid_payload():
    """Test that invalid payloads return clean validation error"""
    response = client.post("/analyze", json={
        "symbol": "VNM",
        # missing required fields
    })
    assert response.status_code == 422  # Pydantic validation error
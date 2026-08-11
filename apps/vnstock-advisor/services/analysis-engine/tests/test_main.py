import json
import pytest
from fastapi.testclient import TestClient
from pathlib import Path

# Fix import path for the app (C7 package layout: modules live in analysis_engine/)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src'))
from analysis_engine.main import app

client = TestClient(app)


def _load_fixture_bars():
    """Load normal-trading fixture and group bars by symbol (ascending, 250/symbol)."""
    path = Path(__file__).parent / "fixtures" / "normal-trading.json"
    bars = json.loads(path.read_text())
    series = {}
    for b in bars:
        series.setdefault(b["symbol"], []).append(b)
    return series


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


def test_analyze_single_bar_returns_insufficient_history():
    """A lone bar (no `bars` series) cannot produce indicators — 422 INSUFFICIENT_HISTORY (C2)."""
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
    assert response.status_code == 422
    body = response.json()
    # RFC 7807: the problem detail is wrapped under `detail`; the problem code
    # lives in the `type` URL (no top-level `code` field).
    assert "detail" in body
    assert "INSUFFICIENT_HISTORY" in body["detail"]["type"]


def test_analyze_with_series_returns_real_indicators():
    """POST /analyze with a full OHLCV series returns actual indicator values (C2)."""
    series = _load_fixture_bars()
    bars = series["VNM"]
    response = client.post("/analyze", json={
        "symbol": "VNM",
        "timeframe": "1D",
        "time": bars[0]["time"],
        "bars": bars,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "VNM"
    assert data["timeframe"] == "1D"
    analysis = data["analysis"]
    assert "signals" in analysis
    assert "trend" in analysis
    assert "strength" in analysis
    indicators = analysis["indicators"]
    assert "ma_20" in indicators
    assert "ma_50" in indicators
    assert "rsi" in indicators
    assert "macd" in indicators
    assert "vwap" in indicators
    # 250 bars: SMA50/RSI/MACD are all computable — must be non-None
    assert indicators["rsi"] is not None
    assert indicators["ma_50"] is not None


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


def test_rank_endpoint_happy_path():
    """POST /rank with the frozen C3/C6 contract returns ranked symbols (real computation)."""
    series = _load_fixture_bars()
    symbols = ["VNM", "FPT", "HPG"]
    response = client.post("/rank", json={
        "symbols": symbols,
        "as_of_date": "2026-08-10",
        "algorithm_version": "v1.0",
        "series": {sym: series[sym] for sym in symbols},
    })
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm_version"] == "v1.0"
    assert data["as_of_date"] == "2026-08-10"
    assert "ranked_at" in data
    assert set(data["weights_used"]) == {"momentum", "trend", "volume", "volatility"}
    ranked = data["ranked"]
    assert len(ranked) == 3  # 250 bars each — all rankable (valid_bars >= 200)
    # Ranks are sequential 1..n and composite scores are non-increasing
    assert [r["rank"] for r in ranked] == [1, 2, 3]
    scores = [r["composite_score"] for r in ranked]
    assert scores == sorted(scores, reverse=True)
    for r in ranked:
        assert r["symbol"] in symbols
        assert isinstance(r["components"], dict)
        assert set(r["components"]) == {"momentum", "trend", "volume", "volatility"}
        assert "sub_components" in r
        assert isinstance(r["reasoning"], list) and r["reasoning"]
    assert data["excluded"] == []


def test_rank_empty_symbols_returns_422():
    """Empty symbols list is rejected by Pydantic min_length=1 — clean 422 (no 500)."""
    response = client.post("/rank", json={
        "symbols": [],
        "as_of_date": "2026-08-10",
        "algorithm_version": "v1.0",
    })
    assert response.status_code == 422  # Pydantic validation error


def test_rank_missing_symbols_returns_422():
    """Missing symbols field is a Pydantic validation error."""
    response = client.post("/rank", json={
        "as_of_date": "2026-08-10",
    })
    assert response.status_code == 422  # Pydantic validation error
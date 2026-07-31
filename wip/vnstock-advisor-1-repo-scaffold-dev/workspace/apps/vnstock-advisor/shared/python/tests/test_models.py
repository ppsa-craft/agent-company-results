import pytest
from vnstock_shared.models import MarketDataCreate, SuggestionCreate, HealthCheck
from datetime import datetime
from decimal import Decimal


def test_market_data_create():
    data = MarketDataCreate(
        time=datetime.now(),
        symbol="VCB",
        open=Decimal("100.0"),
        high=Decimal("105.0"),
        low=Decimal("99.0"),
        close=Decimal("103.0"),
        volume=1000000,
        source="vnstock",
    )
    assert data.symbol == "VCB"
    assert data.volume == 1000000


def test_suggestion_create():
    suggestion = SuggestionCreate(
        symbol="VCB",
        action="BUY",
        confidence=0.85,
        reasoning="Strong uptrend with high volume",
        target_price=Decimal("110.0"),
        stop_loss=Decimal("98.0"),
        timeframe="1W",
    )
    assert suggestion.action == "BUY"
    assert suggestion.confidence == 0.85


def test_health_check():
    health = HealthCheck(
        status="healthy",
        service="test-service",
        version="1.0.0",
        timestamp=datetime.now(),
    )
    assert health.status == "healthy"
    assert health.service == "test-service"
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timezone
from decimal import Decimal
from fastapi.testclient import TestClient

from data_ingest.main import app
from data_ingest.models import OHLCV, IngestResult
from data_ingest.ingest_service import (
    fetch_from_cafef,
    fetch_from_vndirect,
    is_trading_day,
    run_ingestion_job,
)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["service"] == "data-ingest"
    assert "checks" in data
    assert isinstance(data["checks"], list)
    # Check that database check exists in the list
    db_check = next((c for c in data["checks"] if c.get("name") == "database"), None)
    assert db_check is not None
    assert "status" in db_check


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "vnstock Data Ingest Service"}


def test_ingest_run_endpoint_validation():
    """Test that /ingest/run validates input correctly."""
    # Test invalid date format
    response = client.post("/ingest/run", json={"date": "invalid-date"})
    assert response.status_code == 400
    
    # Test valid date format
    with patch("data_ingest.main.run_ingestion_job", new_callable=AsyncMock) as mock_job:
        mock_job.return_value = ([], {"total": 0, "success": 0, "failed": 0, "duplicates_skipped": 0})
        response = client.post("/ingest/run", json={"date": "2024-01-15"})
        # Should not fail with 400 for date format (Monday is trading day)
        assert response.status_code != 400 or "trading day" in response.text.lower()


def test_is_trading_day_weekend():
    """Test that weekends are not trading days."""
    saturday = datetime(2024, 1, 6, tzinfo=timezone.utc)  # Saturday
    sunday = datetime(2024, 1, 7, tzinfo=timezone.utc)   # Sunday
    assert is_trading_day(saturday) is False
    assert is_trading_day(sunday) is False


def test_is_trading_day_weekday():
    """Test that weekdays are trading days (excluding holidays)."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)  # Monday (not a holiday)
    assert is_trading_day(monday) is True


def test_is_trading_day_holiday():
    """Test that Vietnam holidays are not trading days."""
    new_year = datetime(2024, 1, 1, tzinfo=timezone.utc)  # New Year's Day
    assert is_trading_day(new_year) is False


@pytest.mark.asyncio
async def test_scheduled_ingest_runs_on_trading_day():
    """Test scheduled ingestion job runs on trading day."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)  # Monday (not a holiday)
    
    with patch("data_ingest.ingest_service.create_async_engine") as mock_engine:
        mock_engine_instance = AsyncMock()
        mock_engine.return_value = mock_engine_instance
        mock_session = AsyncMock()
        mock_engine_instance.__aenter__.return_value = mock_engine_instance
        mock_engine_instance.dispose = AsyncMock()
        
        with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = OHLCV(
                time=datetime(2024, 1, 8, tzinfo=timezone.utc),
                symbol="VNM",
                open=Decimal("100000"),
                high=Decimal("105000"),
                low=Decimal("99000"),
                close=Decimal("102000"),
                volume=1000000,
                source="CAFEF",
                raw_data={}
            )
            
            results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
            
            assert len(results) == 1
            assert results[0].status == "success"
            assert results[0].source == "CAFEF"
            assert summary["success"] == 1
            assert summary["failed"] == 0


@pytest.mark.asyncio
async def test_fetch_from_cafef_success():
    """Test successful CAFEF fetch with mocked response."""
    mock_session = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "s": "ok",
        "t": [1704067200],  # 2024-01-01 00:00:00 UTC
        "o": [100000],
        "h": [105000],
        "l": [99000],
        "c": [102000],
        "v": [1000000],
    }
    mock_session.get.return_value = mock_response
    
    date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = await fetch_from_cafef(mock_session, date, "VNM")
    
    assert result is not None
    assert result.symbol == "VNM"
    assert result.source == "CAFEF"
    assert result.open == Decimal("100000")
    assert result.close == Decimal("102000")


@pytest.mark.asyncio
async def test_fetch_from_cafef_failure():
    """Test CAFEF fetch failure handling."""
    mock_session = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_session.get.return_value = mock_response
    
    date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = await fetch_from_cafef(mock_session, date, "VNM")
    
    assert result is None


@pytest.mark.asyncio
async def test_fetch_from_vndirect_success():
    """Test successful VNDIRECT fetch with mocked response."""
    mock_session = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "s": "ok",
        "t": [1704067200],
        "o": [100000],
        "h": [105000],
        "l": [99000],
        "c": [102000],
        "v": [1000000],
    }
    mock_session.get.return_value = mock_response
    
    date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = await fetch_from_vndirect(mock_session, date, "VNM")
    
    assert result is not None
    assert result.symbol == "VNM"
    assert result.source == "VNDIRECT"


@pytest.mark.asyncio
async def test_ohlcv_normalize():
    """Test OHLCV normalization to MarketDataCreate."""
    ohlcv = OHLCV(
        time=datetime(2024, 1, 1, tzinfo=timezone.utc),
        symbol="VNM",
        open=Decimal("100000"),
        high=Decimal("105000"),
        low=Decimal("99000"),
        close=Decimal("102000"),
        volume=1000000,
        source="CAFEF",
    )
    
    normalized = ohlcv.normalize()
    
    assert normalized.symbol == "VNM"
    assert normalized.open == Decimal("100000")
    assert normalized.source == "CAFEF"


def test_ingest_result_model():
    """Test IngestResult model creation."""
    result = IngestResult(
        symbol="VNM",
        status="success",
        source="CAFEF",
        rows_upserted=1,
    )
    
    assert result.symbol == "VNM"
    assert result.status == "success"
    assert result.duplicate_skipped is False


@pytest.mark.asyncio
async def test_run_ingestion_job_non_trading_day():
    """Test that run_ingestion_job skips non-trading days."""
    # Sunday
    sunday = datetime(2024, 1, 7, tzinfo=timezone.utc)
    
    with patch("data_ingest.ingest_service.create_async_engine") as mock_engine:
        results, summary = await run_ingestion_job("postgresql://test", ["VNM"], sunday)
        
        assert results == []
        assert summary["total"] == 1
        assert summary["success"] == 0
        assert summary["failed"] == 0
        # Engine should not be created for non-trading day
        mock_engine.assert_not_called()


@pytest.mark.asyncio
async def test_run_ingestion_job_weekday():
    """Test run_ingestion_job on a trading day with mocked sources."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)
    
    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = None  # Simulate CAFEF failure
        
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_fallback:
            mock_fallback.return_value = None  # Simulate VNDIRECT failure too
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine:
                mock_engine_instance = AsyncMock()
                mock_engine.return_value = mock_engine_instance
                mock_session = AsyncMock()
                mock_engine_instance.__aenter__.return_value = mock_engine_instance
                mock_engine_instance.dispose = AsyncMock()
                
                results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                
                assert len(results) == 1
                assert results[0].status == "failed"
                assert results[0].error == "Both primary and fallback sources failed"
                assert summary["failed"] == 1


# Edge case tests
@pytest.mark.asyncio
async def test_fetch_from_cafef_network_error():
    """Test CAFEF fetch handles network errors."""
    mock_session = AsyncMock()
    mock_session.get.side_effect = Exception("Network error")
    
    date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = await fetch_from_cafef(mock_session, date, "VNM")
    
    assert result is None


@pytest.mark.asyncio
async def test_fetch_from_cafef_malformed_response():
    """Test CAFEF fetch handles malformed JSON response."""
    mock_session = AsyncMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invalid": "format"}
    mock_session.get.return_value = mock_response
    
    date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    result = await fetch_from_cafef(mock_session, date, "VNM")
    
    assert result is None


@pytest.mark.asyncio
async def test_ingest_status_endpoint():
    """Test /ingest/status endpoint."""
    response = client.get("/ingest/status")
    assert response.status_code == 200
    data = response.json()
    assert "scheduler_running" in data
    assert "default_symbols" in data
    assert isinstance(data["default_symbols"], list)


@pytest.mark.asyncio
async def test_primary_source_failure_triggers_fallback():
    """Test that primary source failure triggers fallback to secondary source."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)
    
    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_cafef:
        mock_cafef.return_value = None  # Primary source fails
        
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_vndirect:
            mock_vndirect.return_value = OHLCV(
                time=datetime(2024, 1, 8, tzinfo=timezone.utc),
                symbol="VNM",
                open=Decimal("100000"),
                high=Decimal("105000"),
                low=Decimal("99000"),
                close=Decimal("102000"),
                volume=1000000,
                source="VNDIRECT",
                raw_data={}
            )
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine:
                mock_engine_instance = AsyncMock()
                mock_engine.return_value = mock_engine_instance
                mock_session = AsyncMock()
                mock_engine_instance.__aenter__.return_value = mock_engine_instance
                mock_engine_instance.dispose = AsyncMock()
                
                results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                
                assert len(results) == 1
                assert results[0].status == "success"
                assert results[0].source == "VNDIRECT"
                assert summary["success"] == 1
                assert summary["failed"] == 0


@pytest.mark.asyncio
async def test_both_sources_fail():
    """Test that when both primary and fallback sources fail, ingestion fails gracefully."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)
    
    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_cafef:
        mock_cafef.return_value = None  # Primary source fails
        
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_vndirect:
            mock_vndirect.return_value = None  # Fallback also fails
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine:
                mock_engine_instance = AsyncMock()
                mock_engine.return_value = mock_engine_instance
                mock_session = AsyncMock()
                mock_engine_instance.__aenter__.return_value = mock_engine_instance
                mock_engine_instance.dispose = AsyncMock()
                
                results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                
                assert len(results) == 1
                assert results[0].status == "failed"
                assert results[0].error == "Both primary and fallback sources failed"
                assert summary["success"] == 0
                assert summary["failed"] == 1
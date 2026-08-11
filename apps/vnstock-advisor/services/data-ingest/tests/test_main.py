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


class AsyncContextManagerMock:
    """Mock async context manager for testing."""
    def __init__(self, return_value):
        self._return_value = return_value
    
    async def __aenter__(self):
        return self._return_value
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


def make_async_context_manager(return_value):
    """Create an async context manager mock that returns the given value on __aenter__."""
    return AsyncContextManagerMock(return_value)


def assert_meta_disclaimer(data):
    """Assert that a response body includes meta.disclaimer for both locales."""
    assert "meta" in data
    assert "disclaimer" in data["meta"]
    assert "vi-VN" in data["meta"]["disclaimer"]
    assert "en-US" in data["meta"]["disclaimer"]


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
    assert_meta_disclaimer(data)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "vnstock Data Ingest Service"
    assert_meta_disclaimer(data)


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
        # When a run completes successfully its response body must include the disclaimer
        if response.status_code == 200:
            assert_meta_disclaimer(response.json())


def test_ingest_run_rejects_invalid_symbols():
    """Test that /ingest/run rejects invalid ticker symbols (C4 bound)."""
    response = client.post(
        "/ingest/run",
        json={"date": "2024-01-15", "symbols": ["vnm"]},
    )
    assert response.status_code == 422


def test_ingest_run_rejects_unknown_source():
    """Test that /ingest/run rejects a source outside CAFEF/VNDIRECT (C4)."""
    response = client.post(
        "/ingest/run",
        json={"date": "2024-01-15", "source": "OTHER"},
    )
    assert response.status_code == 422


def test_ingest_run_passes_source_override():
    """Test that /ingest/run forwards a forced source to the ingestion job (C4)."""
    with patch("data_ingest.main.run_ingestion_job", new_callable=AsyncMock) as mock_job:
        mock_job.return_value = ([], {"total": 0, "success": 0, "failed": 0, "duplicates_skipped": 0})
        response = client.post(
            "/ingest/run",
            json={"date": "2024-01-15", "source": "VNDIRECT"},
        )
        assert response.status_code == 200
        mock_job.assert_awaited_once()
        _, kwargs = mock_job.call_args
        assert kwargs.get("source") == "VNDIRECT"


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
    
    mock_conn = AsyncMock()
    mock_session = AsyncMock()
    
    # Mock engine.begin() to return an async context manager yielding mock_conn
    mock_engine = MagicMock()
    mock_engine.begin = lambda: make_async_context_manager(mock_conn)
    
    with patch("data_ingest.ingest_service.create_async_engine") as mock_engine_factory:
        mock_engine_factory.return_value = mock_engine
        
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
            
            # Mock the sessionmaker
            with patch("data_ingest.ingest_service.sessionmaker") as mock_sessionmaker:
                mock_sessionmaker.return_value.return_value = mock_session
                mock_session.add = AsyncMock()
                mock_session.commit = AsyncMock()
                mock_session.rollback = AsyncMock()
                
                results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                
                assert len(results) == 1
                assert results[0].status == "success"
                assert results[0].source == "CAFEF"
                assert summary["success"] == 1
                assert summary["failed"] == 0


@pytest.mark.asyncio
async def test_fetch_from_cafef_success():
    """Test successful CAFEF fetch with mocked response."""
    from unittest.mock import AsyncMock
    import httpx
    
    mock_session = AsyncMock(spec=httpx.AsyncClient)
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Use the correct format for CAFEF response (based on the actual data)
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
    from unittest.mock import AsyncMock
    import httpx
    
    mock_session = AsyncMock(spec=httpx.AsyncClient)
    mock_response = MagicMock()
    mock_response.status_code = 200
    # Use simple format with proper time field
    mock_response.json.return_value = {
        "t": "2024-01-01 00:00:00",
        "symbol": "VNM",
        "o": 100000,
        "h": 105000,
        "l": 99000,
        "c": 102000,
        "v": 1000000,
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
    
    normalized = ohlcv.normalize("1D")
    
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
    
    mock_conn = AsyncMock()
    mock_session = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin = lambda: make_async_context_manager(mock_conn)
    
    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = None  # Simulate CAFEF failure
        
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_fallback:
            mock_fallback.return_value = None  # Simulate VNDIRECT failure too
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine_factory:
                mock_engine_factory.return_value = mock_engine
                mock_session = AsyncMock()
                
                with patch("data_ingest.ingest_service.sessionmaker") as mock_sessionmaker:
                    mock_sessionmaker.return_value.return_value = mock_session
                    mock_session.add = AsyncMock()
                    mock_session.commit = AsyncMock()
                    mock_session.rollback = AsyncMock()
                    
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
    assert_meta_disclaimer(data)


@pytest.mark.asyncio
async def test_primary_source_failure_triggers_fallback():
    """Test that primary source failure triggers fallback to secondary source."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)
    
    mock_conn = AsyncMock()
    mock_session = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin = lambda: make_async_context_manager(mock_conn)
    
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
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine_factory:
                mock_engine_factory.return_value = mock_engine
                
                with patch("data_ingest.ingest_service.sessionmaker") as mock_sessionmaker:
                    mock_sessionmaker.return_value.return_value = mock_session
                    mock_session.add = AsyncMock()
                    mock_session.commit = AsyncMock()
                    mock_session.rollback = AsyncMock()
                    
                    results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                    
                    assert len(results) == 1
                    assert results[0].status == "success"
                    assert results[0].source == "VNDIRECT"
                    assert summary["success"] == 1
                    assert summary["failed"] == 0


@pytest.mark.asyncio
async def test_forced_source_skips_fallback():
    """Test that a forced source bypasses the fallback logic (C4)."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)

    mock_conn = AsyncMock()
    mock_session = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin = lambda: make_async_context_manager(mock_conn)

    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_cafef:
        mock_cafef.return_value = OHLCV(
            time=datetime(2024, 1, 8, tzinfo=timezone.utc),
            symbol="VNM",
            open=Decimal("100000"),
            high=Decimal("105000"),
            low=Decimal("99000"),
            close=Decimal("102000"),
            volume=1000000,
            source="CAFEF",
            raw_data={},
        )
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_vndirect:
            mock_vndirect.return_value = OHLCV(
                time=datetime(2024, 1, 8, tzinfo=timezone.utc),
                symbol="VNM",
                open=Decimal("101000"),
                high=Decimal("106000"),
                low=Decimal("99000"),
                close=Decimal("103000"),
                volume=1200000,
                source="VNDIRECT",
                raw_data={},
            )
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine_factory:
                mock_engine_factory.return_value = mock_engine
                with patch("data_ingest.ingest_service.sessionmaker") as mock_sessionmaker:
                    mock_sessionmaker.return_value.return_value = mock_session
                    mock_session.add = AsyncMock()
                    mock_session.commit = AsyncMock()
                    mock_session.rollback = AsyncMock()

                    results, summary = await run_ingestion_job(
                        "postgresql://test", ["VNM"], monday, source="VNDIRECT"
                    )

                    assert len(results) == 1
                    assert results[0].status == "success"
                    assert results[0].source == "VNDIRECT"
                    assert summary["success"] == 1
                    mock_cafef.assert_not_awaited()


@pytest.mark.asyncio
async def test_forced_source_failure_does_not_fallback():
    """Test that a forced source failure does not fall back (C4)."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)

    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_cafef:
        mock_cafef.return_value = None
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_vndirect:
            mock_vndirect.return_value = OHLCV(
                time=datetime(2024, 1, 8, tzinfo=timezone.utc),
                symbol="VNM",
                open=Decimal("101000"),
                high=Decimal("106000"),
                low=Decimal("99000"),
                close=Decimal("103000"),
                volume=1200000,
                source="VNDIRECT",
                raw_data={},
            )
            with patch("data_ingest.ingest_service.create_async_engine"):
                results, summary = await run_ingestion_job(
                    "postgresql://test", ["VNM"], monday, source="CAFEF"
                )

                assert len(results) == 1
                assert results[0].status == "failed"
                assert results[0].error == "Forced source CAFEF failed"
                assert summary["failed"] == 1
                mock_vndirect.assert_not_awaited()


@pytest.mark.asyncio
async def test_both_sources_fail():
    """Test that when both primary and fallback sources fail, ingestion fails gracefully."""
    monday = datetime(2024, 1, 8, tzinfo=timezone.utc)
    
    mock_conn = AsyncMock()
    mock_session = AsyncMock()
    mock_engine = MagicMock()
    mock_engine.begin = lambda: make_async_context_manager(mock_conn)
    
    with patch("data_ingest.ingest_service.fetch_from_cafef", new_callable=AsyncMock) as mock_cafef:
        mock_cafef.return_value = None  # Primary source fails
        
        with patch("data_ingest.ingest_service.fetch_from_vndirect", new_callable=AsyncMock) as mock_vndirect:
            mock_vndirect.return_value = None  # Fallback also fails
            
            with patch("data_ingest.ingest_service.create_async_engine") as mock_engine_factory:
                mock_engine_factory.return_value = mock_engine
                
                with patch("data_ingest.ingest_service.sessionmaker") as mock_sessionmaker:
                    mock_sessionmaker.return_value.return_value = mock_session
                    mock_session.add = AsyncMock()
                    mock_session.commit = AsyncMock()
                    mock_session.rollback = AsyncMock()
                    
                    results, summary = await run_ingestion_job("postgresql://test", ["VNM"], monday)
                    
                    assert len(results) == 1
                    assert results[0].status == "failed"
                    assert results[0].error == "Both primary and fallback sources failed"
                    assert summary["success"] == 0
                    assert summary["failed"] == 1


def test_ingest_run_db_unreachable_returns_clean_error():
    """Worst-flow: DB unreachable at connection time → clean RFC-7807 503, no stack trace.

    Reproduces TESTER defect 4: live /ingest/run on a trading day with no reachable
    Postgres previously returned HTTP 500 with a raw asyncpg ConnectionRefusedError
    stack trace leaking from run_ingestion_job's engine.begin() (outside the
    per-symbol try/except). The endpoint must instead return a clean RFC-7807
    problem+json body with no raw driver exception / traceback leakage.
    """
    class RaisingAsyncContextManager:
        """Async context manager whose __aenter__ raises — simulates a DB connection failure."""

        def __init__(self, exc):
            self._exc = exc

        async def __aenter__(self):
            raise self._exc

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            return None

    mock_engine = MagicMock()
    mock_engine.begin = lambda: RaisingAsyncContextManager(
        ConnectionRefusedError("[Errno 111] Connection refused")
    )

    with patch("data_ingest.ingest_service.create_async_engine", return_value=mock_engine):
        response = client.post("/ingest/run", json={"date": "2024-01-15", "symbols": ["VNM"]})

    # Clean RFC-7807 problem+json error body — 5xx, no stack trace / raw driver error
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    data = response.json()
    assert data["type"] == "about:blank"
    assert data["title"] == "Database unavailable"
    assert data["status"] == 503
    assert data["detail"]
    body = response.text.lower()
    assert "traceback" not in body
    assert "connectionrefused" not in body
    assert "asyncpg" not in body
# Task T-126-05: S2 Indicators Engine (Service S2)

## Overview
Implement the S2 Indicators Engine service for the VN Stock Suggestion system. This service provides technical indicators computation using TA-Lib/Pandas, cached via Redis, exposed via FastAPI endpoints.

## Architecture Context
- **Service**: S2 - Indicators Engine
- **Location**: `workspace/apps/vn-stock-suggestion/src/services/indicators/`
- **Stack**: Python/FastAPI, Pandas/TA-Lib, Redis cache
- **Architecture**: S2 Indicators layer (disjoint from S1 Data Ingestion, S3 Signals, S4 Recommendations)
- **Contracts**: `techlead-interface-contracts.md` (S2 interfaces)

## Implementation Plan (Ordered Subtasks)

### 1. Project Structure Setup
- [ ] Create `workspace/apps/vn-stock-suggestion/src/services/indicators/` directory structure
- [ ] Create `pyproject.toml` with dependencies (fastapi, pandas, ta-lib, redis, pydantic, pydantic-settings, pytest, pytest-asyncio, httpx)
- [ ] Create `config.py` with Pydantic Settings (Redis URL, TA-Lib config, cache TTL)
- [ ] Create `__init__.py` exports

### 2. Domain Models (Pydantic Models)
- [ ] Create `models/indicators.py` with Pydantic models:
  - `IndicatorRequest` (symbol, timeframe, indicators list, lookback)
  - `IndicatorResponse` (symbol, timeframe, indicators dict, timestamp, cache_hit)
  - `IndicatorConfig` (name, params dict)
  - `IndicatorResult` (name, values list[float], timestamps list[datetime])
  - `HealthResponse` (status, redis_connected, talib_version)
  - `IndicatorMetadata` (name, description, parameters, output_type)

### 3. TA-Lib Indicators Engine
- [ ] Create `engine/indicators_engine.py` with `IndicatorsEngine` class:
  - `compute_indicators(df: pd.DataFrame, indicators: List[IndicatorConfig]) -> Dict[str, IndicatorResult]`
  - Support indicators: SMA, EMA, RSI, MACD, BBANDS, ATR, STOCH, ADX, OBV, ROC, CCI, WILLR, MOM
  - Each indicator: validate params, call TA-Lib, handle NaN, return `IndicatorResult`
  - Handle NaN padding, align timestamps, handle insufficient data

### 4. Redis Cache Layer
- [ ] Create `cache/redis_cache.py` with `RedisCache` class:
  - `get(key: str) -> Optional[IndicatorResponse]`
  - `set(key: str, value: IndicatorResponse, ttl: int) -> bool`
  - `health_check() -> bool`
  - Key format: `indicators:{symbol}:{timeframe}:{indicators_hash}:{lookback}`
  - TTL from config (default 300s)
  - Connection pooling, retry logic, health check

### 5. FastAPI Application
- [ ] Create `main.py` with FastAPI app:
  - `POST /indicators/compute` - Compute indicators (with cache)
  - `GET /indicators/metadata` - List supported indicators with metadata
  - `GET /health` - Health check (Redis, TA-Lib version)
  - `GET /indicators/{symbol}/{timeframe}` - Quick compute with defaults
  - Dependency injection for engine and cache
  - Request/response validation with Pydantic
  - Error handling (400, 500, 503)

### 6. Data Adapter (S1 Integration)
- [ ] Create `adapters/data_adapter.py` with `DataAdapter` class:
  - `fetch_ohlcv(symbol: str, timeframe: str, lookback: int) -> pd.DataFrame`
  - HTTP client to S1 Data Ingestion service (configurable base URL)
  - Timeout, retry, error handling
  - Convert S1 response to pandas DataFrame with OHLCV columns

### 7. Unit Tests (pytest + pytest-asyncio)
- [ ] `tests/test_indicators_engine.py` - Test each TA-Lib indicator computation
- [ ] `tests/test_redis_cache.py` - Test cache get/set/health, mock Redis
- [ ] `tests/test_data_adapter.py` - Test S1 adapter with mocked HTTP
- [ ] `tests/test_api_endpoints.py` - Test FastAPI endpoints with TestClient
- [ ] `tests/conftest.py` - Fixtures (sample OHLCV DataFrame, mock Redis, mock S1)
- [ ] `tests/conftest.py` - Sample OHLCV DataFrame fixture with realistic VN stock data

### 8. Integration Test
- [ ] `tests/test_integration.py` - Full flow: S1 mock -> Engine -> Cache -> API

### 9. Documentation & Config
- [ ] Update `workspace/apps/vn-stock-suggestion/README.md` with S2 run steps
- [ ] Create `workspace/apps/vn-stock-suggestion/src/services/indicators/README.md` with API docs
- [ ] Create `.env.example` with all config variables
- [ ] Update `workspace/apps/vn-stock-suggestion/analytics-plan.md` with S2 metrics

### 10. Analytics Plan Update
- [ ] Update `workspace/apps/vn-stock-suggestion/analytics-plan.md` with S2 metrics:
  - Indicator computation latency (p50, p95, p99)
  - Cache hit rate
  - TA-Lib computation errors
  - Cache hit/miss ratio
  - S1 adapter latency/errors

## Test Plan (for TESTER-1 parallel execution)

### Unit Tests
- [ ] `test_sma_computation` - SMA with various periods, verify values match TA-Lib reference
- [ ] `test_ema_computation` - EMA with various periods
- [ ] `test_rsi_computation` - RSI with period 14, verify 0-100 range
- [ ] `test_macd_computation` - MACD (12,26,9), verify signal/histogram
- [ ] `test_bbands_computation` - BBANDS (20,2), verify upper/middle/lower
- [ ] `test_atr_computation` - ATR (14), verify positive values
- [ ] `test_stoch_computation` - STOCH (14,3), verify 0-100 range
- [ ] `test_adx_computation` - ADX (14), verify 0-100 range
- [ ] `test_obv_computation` - OBV, verify cumulative volume
- [ ] `test_roc_computation` - ROC (10), verify percentage change
- [ ] `test_cci_computation` - CCI (20), verify typical range
- [ ] `test_willr_computation` - WILLR (14), verify -100 to 0 range
- [ ] `test_mom_computation` - MOM (10), verify momentum values
- [ ] `test_insufficient_data_handling` - Fewer rows than period returns NaN-padded results
- [ ] `test_nan_handling` - NaN in input handled gracefully
- [ ] `test_cache_get_set` - Cache round-trip with TTL
- [ ] `test_cache_miss` - Cache miss returns None
- [ ] `test_cache_health_check` - Health check returns True/False
- [ ] `test_data_adapter_fetch` - Mock S1 response -> DataFrame conversion
- [ ] `test_data_adapter_timeout` - Timeout handling
- [ ] `test_data_adapter_retry` - Retry logic on 5xx
- [ ] `test_api_compute_endpoint` - POST /indicators/compute returns valid response
- [ ] `test_api_metadata_endpoint` - GET /indicators/metadata returns all indicators
- [ ] `test_api_health_endpoint` - GET /health returns healthy status
- [ ] `test_api_quick_compute` - GET /indicators/{symbol}/{timeframe} works
- [ ] `test_api_cache_hit` - Second request returns cache_hit=true
- [ ] `test_api_validation_error` - Invalid symbol returns 400
- [ ] `test_api_s1_unavailable` - S1 unavailable returns 503

### Integration Test
- [ ] `test_full_flow` - Mock S1 -> Engine -> Cache -> API -> Response (cache_hit=false then true)

## Acceptance Criteria (Tier 1 - Full Artifacts)
- All unit tests pass (pytest -v)
- Integration test passes
- FastAPI app starts and serves endpoints
- Redis cache works (hit/miss/TTL)
- TA-Lib computes all 13 indicators correctly
- S1 adapter handles timeout/retry gracefully
- README.md has working run steps
- analytics-plan.md updated with S2 metrics
- Service runs on port 8002 (configurable)
- Redis connection pooling works
- TA-Lib version reported in health check

## Branch
Branch: `task/T-126-05-dev-1` (created from milestone branch)

## Dependencies
- S1 Data Ingestion service must be running (or mocked in tests)
- Redis server running on configured URL
- TA-Lib system library installed (ta-lib system package)
- Python 3.11+, Python 3.11+

## Deliverables
All files under `workspace/apps/vn-stock-suggestion/src/services/indicators/` + tests + docs + analytics update
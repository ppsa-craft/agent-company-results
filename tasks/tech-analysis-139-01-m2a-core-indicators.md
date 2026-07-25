# Task T-139-01: M2A Core Indicators

## Goal
Implement core technical analysis indicators (SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic) as a standalone service (m2-indicators) with clean API contracts for M2B Data Pipeline and M3A Alert Rules consumption.

## Acceptance Criteria (Traceable to Use Cases)
- [ ] **UC-M2A-01**: Calculate SMA/EMA for any period (5-200) on OHLCV input — returns array aligned to input length
- [ ] **UC-M2A-02**: Calculate RSI (14 default, configurable period) — returns 0-100 values, handles edge cases (flat prices, NaN)
- [ ] **UC-M2A-03**: Calculate MACD (12,26,9 default) — returns MACD line, signal line, histogram
- [ ] **UC-M2A-04**: Calculate Bollinger Bands (20,2 default) — returns upper, middle, lower bands
- [ ] **UC-M2A-05**: Calculate ATR (14 default) — handles true range calculation correctly
- [ ] **UC-M2A-06**: Calculate Stochastic (%K, %D) — handles %K smoothing
- [ ] **UC-M2A-07**: All indicators handle NaN/insufficient data gracefully (return NaN for warmup period)
- [ ] **UC-M2A-08**: REST API `/indicators/calculate` accepts batch requests (multiple symbols, multiple indicators, single call)
- [ ] **UC-M2A-09**: Response time < 50ms p99 for single symbol, 10 indicators, 500 bars
- [ ] **UC-M2A-10**: OpenAPI contract published at `/contracts/m2-indicators.yaml` — consumed by M2B and M3A

## Estimated Effort
- **Effort**: 3 cycles (Cycle 139-141)
- **DoD Tier**: Tier 2 (Feature: use cases + tests + docs + analytics update)

## Assigned Agent
- **Role**: DEV
- **Agent**: dev-1
- **Cycle**: 139
- **Status**: READY

## File Ownership (Disjoint Boundary: `services/m2-indicators/`)
```
workspace/apps/tech-analysis/services/m2-indicators/
├── src/
│   ├── indicators/
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base class, NaN handling
│   │   ├── moving_averages.py   # SMA, EMA
│   │   ├── momentum.py          # RSI, Stochastic
│   │   ├── trend.py             # MACD
│   │   ├── volatility.py        # Bollinger Bands, ATR
│   │   └── registry.py          # Indicator registry, batch calculation
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py            # FastAPI routes
│   │   ├── schemas.py           # Pydantic request/response models
│   │   └── dependencies.py      # Dependency injection
│   ├── main.py                  # FastAPI app entrypoint
│   └── config.py                # Settings, indicator defaults
├── tests/
│   ├── unit/
│   │   ├── test_moving_averages.py
│   │   ├── test_momentum.py
│   │   ├── test_trend.py
│   │   ├── test_volatility.py
│   │   └── test_edge_cases.py   # NaN, flat prices, insufficient data
│   ├── contract/
│   │   └── test_openapi_contract.py
│   ├── integration/
│   │   └── test_api_performance.py
│   └── fixtures/
│       └── sample_ohlcv.json
├── contracts/
│   └── m2-indicators.yaml       # OpenAPI 3.1 spec
├── pyproject.toml
├── README.md
└── Dockerfile
```

## Implementation Plan (for DEV)

**Architecture Seam**: `services/m2-indicators/` — disjoint from `m2-pipeline` (T-139-02) and `m3-alerts` (T-139-06/07). Communicates ONLY via OpenAPI contract at `contracts/m2-indicators.yaml`.

**Tech Stack** (per `tasks/stack-tech-analysis.md`):
- Python 3.11, FastAPI, Pydantic v2, NumPy/Pandas for calculations
- Pytest + pytest-asyncio for tests
- Docker multi-stage build

**Ordered Subtask Checklist**:
1. [ ] Scaffold service structure (pyproject.toml, Dockerfile, config, main.py)
2. [ ] Implement `base.py` — `IndicatorBase` abstract class with `calculate()`, `validate_input()`, NaN handling
3. [ ] Implement `moving_averages.py` — SMA (rolling window), EMA (recursive, Wilder's smoothing)
4. [ ] Implement `momentum.py` — RSI (Wilder's), Stochastic (%K/%D with smoothing)
5. [ ] Implement `trend.py` — MACD (EMA12, EMA26, signal EMA9, histogram)
6. [ ] Implement `volatility.py` — Bollinger Bands (SMA ± k*std), ATR (True Range + Wilder's smoothing)
7. [ ] Implement `registry.py` — `IndicatorRegistry` for batch calculation, indicator discovery
8. [ ] Implement API layer: schemas (BatchRequest, BatchResponse, IndicatorResult), routes (`POST /indicators/calculate`, `GET /indicators`, `GET /health`)
9. [ ] Write OpenAPI contract `contracts/m2-indicators.yaml` (source of truth for M2B/M3A)
10. [ ] Unit tests: each indicator class, edge cases (NaN, flat, insufficient data, single bar)
11. [ ] Contract test: validate OpenAPI spec against implementation
12. [ ] Performance test: benchmark 500 bars × 10 indicators × 10 symbols < 50ms p99
13. [ ] Write README.md with run instructions, API examples, indicator formulas reference
14. [ ] Update analytics plan (tracking: indicator latency, error rates, symbol coverage)
15. [ ] Docker build test, verify health endpoint

**Dependencies**: None (starts M2A→M3A chain). T-139-06 (M3A Alert Rules) depends on OpenAPI contract from this task.

## Test Plan (for TESTER)

**Happy Path Scenarios**:
1. **Single indicator, single symbol**: POST `/indicators/calculate` with `{symbol: "AAPL", indicators: ["sma_20"], ohlcv: [...]}` → returns aligned SMA array
2. **Batch multi-indicator, multi-symbol**: 10 symbols × 6 indicators × 500 bars → returns structured response per symbol/indicator
3. **Configurable parameters**: RSI period=21, MACD (8,21,5), BB (50, 2.5) — params respected in output
4. **Health check**: GET `/health` → `{"status": "healthy", "indicators": 7}`

**Edge Cases**:
1. **Insufficient data**: 10 bars requested for SMA_20 → returns array of 10 NaN
2. **Flat prices**: 100 bars all $100.00 → RSI returns 50 (or NaN for first 14), ATR returns 0
3. **NaN in input**: OHLCV with some NaN → indicators handle gracefully, propagate NaN appropriately
4. **Empty request**: `indicators: []` → 400 error with clear message
5. **Unknown indicator**: `indicators: ["foo"]` → 400 error listing available indicators
6. **Large batch**: 100 symbols × 500 bars × 7 indicators → completes < 500ms, no OOM

**Restart Behavior**:
1. Cold start: service starts < 3s, health endpoint ready
2. Warm restart: in-memory caches cleared, no state corruption

**Expected Results**: All scenarios return 200 with correct JSON schema matching OpenAPI contract. Edge cases return 400/422 with structured error (field, message, code). Performance test passes p99 < 50ms.

## DoD Tier 2 Checklist
- [ ] All 10 UCs implemented and tested
- [ ] Unit test coverage ≥ 90% per indicator module
- [ ] Contract test passes (OpenAPI spec matches implementation)
- [ ] Performance test passes p99 < 50ms
- [ ] README.md with run instructions (docker compose up, curl examples)
- [ ] OpenAPI contract published at `contracts/m2-indicators.yaml`
- [ ] Analytics events defined (indicator_calculated, calculation_error, batch_latency_ms)
- [ ] Code review approved by TECHLEAD
- [ ] Security gate passed (QA)
- [ ] Changelog entry in CHANGELOG.md
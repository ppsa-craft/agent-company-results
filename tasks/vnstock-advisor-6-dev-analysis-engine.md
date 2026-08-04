# Task: vnstock-advisor-5-dev-analysis-engine

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: analysis-engine service)
**Status:** claimed:DEV-2

---

## Goal

Implement `analysis-engine` service: compute indicators, screen symbols, rank by composite score, expose `/rank` endpoint.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Service runs in `workspace/apps/vnstock-advisor/services/analysis-engine/`
- [ ] Reads `market_data` from PostgreSQL (via SQLAlchemy)
- [ ] Computes indicators per BA spec: SMA(20/50), EMA(12/26), RSI(14), MACD(12,26,9), volume profile (20-day avg)
- [ ] Screens symbols: price > SMA20, RSI < 70, volume > 1.5x avg
- [ ] Ranks by composite score (weights configurable via env): momentum 40%, trend 30%, volume 20%, volatility 10%
- [ ] Endpoint: `GET /rank?symbols=&strategy=default` → `{symbol, score, indicators[], reasoning[]}`
- [ ] Handles insufficient data gracefully (returns partial with warning)
- [ ] Timeout guard on computation (max 30s per request)
- [ ] Unit tests: each indicator, screening, ranking (against fixture data)
- [ ] Integration test: `/rank` against test DB with fixture data
- [ ] Security: SAST clean, SCA clean, secret-scan clean, input validation (Pydantic on query params), rate-limit per tenant
- [ ] README with local run instructions

---

## Implementation Plan (for DEV)

**Architecture seam:** Owns `analysis-engine` service only. Interfaces: reads `market_data`, exposes `/rank`. Depends on `data-ingest` contract (OpenAPI + DB schema) — can build in parallel once contract frozen.

1. Set up FastAPI project in `services/analysis-engine/`
2. Implement SQLAlchemy models for `market_data` (from shared/python)
3. Implement indicator calculations (pandas + pandas-ta or ta-lib)
4. Implement screening logic (vectorized pandas)
5. Implement ranking algorithm (configurable weights via Pydantic Settings)
6. Implement `/rank` endpoint with Pydantic request/response
7. Add timeout guard (asyncio.wait_for)
8. Add rate-limiting (slowapi or custom middleware)
9. Write tests against BA fixture data
10. Verify CI passes

---

## Test Plan (for TESTER)

**Scenario 1: Indicator accuracy**
- Steps: Feed fixture data, compare indicator outputs to expected values
- Expected: Matches BA spec within floating-point tolerance

**Scenario 2: Screening correctness**
- Steps: Feed fixture data with known pass/fail symbols
- Expected: Only passing symbols returned

**Scenario 3: Ranking determinism**
- Steps: Call `/rank` twice with same input
- Expected: Identical output (same scores, same order)

**Scenario 4: Insufficient data handling**
- Steps: Request symbols with < 20 data points
- Expected: Returns available with warning in reasoning, no crash

**Scenario 5: Timeout guard**
- Steps: Request ranking for 1000 symbols
- Expected: Completes within 30s or returns partial with timeout notice

**Scenario 6: Security gate**
- Steps: Run Semgrep, Snyk, Gitleaks
- Expected: No high/critical findings

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (monorepo, shared/python)
- `vnstock-advisor-3-ba-analysis-engine` (specs, fixtures)
- `vnstock-advisor-4-dev-data-ingest` (contract: DB schema + OpenAPI) — **parallelizable once contract published**
- Blocks: `vnstock-advisor-7-dev-suggestion-api` (needs `/rank` contract)
# TECHLEAD Analysis Record: vnstock-advisor Analysis Engine (M2)

**Product:** vnstock-advisor  
**Component:** analysis-engine (M2)  
**Date:** 2026-08-02  
**Analyst:** CTO (acting as TECHLEAD reviewer)  
**Review Type:** Architecture + Contract Alignment + Security Gate Readiness  

---

## 1. Current Implementation State

### data-ingest (M1) — **DONE**
- **Endpoints:** `/health`, `/ingest/run`, `/ingest/status`, `/`
- **Status:** Working endpoints, tests passing, security controls in place
- **Security Gate:** Ready for QA — SAST/secret-scan/SCA configured in stack record
- **Contract:** Produces `MarketDataCreate` via shared models; scheduled at 6 AM ICT daily

### analysis-engine (M2) — **IN-PROGRESS (Placeholder Only)**
- **Endpoints:** `/health`, `/`, `/analyze` (placeholder)
- **Implementation:** Single file `services/analysis-engine/src/main.py` — 57 lines, placeholder response
- **Dependencies:** `fastapi`, `uvicorn`, `pandas`, `numpy`, `ta-lib`, `vnstock-shared-python`
- **Tests:** 5 tests covering health, root, and placeholder `/analyze` endpoint only
- **Missing:** All indicator computation, screening, ranking logic per BA specs

### suggestion-api (M3) — **Scaffolded**
- **Endpoints:** `/health`, `/` (Fastify with helmet, cors, rate-limit, JWT)
- **Contract:** Consumes `AnalysisResult` from analysis-engine
- **Status:** Awaiting analysis-engine contract stabilization

---

## 2. Dependency Graph Analysis

```
data-ingest (producer) → analysis-engine (consumer + processor) → suggestion-api (consumer)
       │                         │                                    │
       │  MarketDataCreate       │  AnalysisResult                    │  SuggestionCreate
       │  (shared/python)        │  (shared/python + typescript)      │  (shared)
       ▼                         ▼                                    ▼
  PostgreSQL                 Computation                          REST API
  TimescaleDB                (pandas/ta-lib)                      (Fastify)
```

**Contract Alignment — CRITICAL FINDINGS:**

| Contract | Current State | Required by Spec | Gap |
|----------|---------------|------------------|-----|
| `/analyze` (placeholder) | Accepts `MarketDataCreate`, returns hardcoded dummy | `POST /indicators/compute`, `POST /screen`, `POST /rank` | **Complete redesign needed** — placeholder doesn't match any UC |
| `MarketDataCreate` → analysis-engine | Not yet consumed | Read from DB `market_data` table | DB read layer missing |
| `AnalysisResult` schema | Defined in shared (both Python + TS) | Matches `indicators.md` + `screening-ranking.md` output | Schema exists but engine doesn't produce it |
| Versioning | Not implemented | `criteria_version: "v1.0"`, `algorithm_version: "v1.0"` | Version headers/params missing |

**Parallelization Assessment:** ✅ **Clean seams confirmed**
- `data-ingest` and `analysis-engine` share only `vnstock-shared-python` (models) and DB schema — **no code coupling**
- `analysis-engine` and `suggestion-api` share only `AnalysisResult` contract — **no code coupling**
- M2 (analysis-engine) can be built in parallel with M3 BA work

---

## 3. Architecture Assessment

### Strengths
- Monorepo with isolated service boundaries (per stack decision)
- Shared contracts via `vnstock-shared-python` and `shared/typescript` — versioned, typed
- FastAPI + Pydantic for input validation (security baseline)
- Structured logging with `structlog` + PII disclaimer injection
- CI matrix with service-level gates defined in stack record

### Gaps for M2 Completion
| Area | Current | Required | Effort |
|------|---------|----------|--------|
| Indicator computation | Placeholder only | SMA, EMA, RSI, MACD, Volume Profile, ROC, ATR, OBV | High (8 indicators + edge cases) |
| Screening endpoint | Missing | `POST /screen` with v1.0 criteria | Medium |
| Ranking endpoint | Missing | `POST /rank` with 4-factor composite + reasoning | High |
| DB read layer | Missing | Query `market_data` TimescaleDB hypertable | Medium |
| Fixtures & golden outputs | Specs exist, files not created | 8 fixture sets + 3 golden outputs | Medium |
| Versioning | None | Header/query param for `v1.0` | Low |
| Security gates | CI configured, no code to scan | Secret-scan, SAST, SCA on implementation | Medium |

---

## 4. Security Gate Readiness (§7.2.1)

### Attack Surface: analysis-engine
| Surface | OWASP Risks | Controls Required | Status |
|---------|-------------|-------------------|--------|
| API (`/indicators/compute`, `/screen`, `/rank`) | Injection, DoS, data exposure | Pydantic validation, rate limiting, timeouts, input size caps | ⚠️ Endpoints missing |
| Computation (pandas/ta-lib/numba) | DoS via large inputs, resource exhaustion | Max rows limit, computation timeout, memory caps | ❌ Not implemented |
| DB read (`market_data`) | SQL injection | SQLAlchemy parameterized queries (already used in shared) | ✅ Ready |
| Dependencies (ta-lib, pandas, numpy) | Supply chain | Snyk SCA + SBOM, pip-audit | ✅ CI configured |
| Secrets (JWT keys, DB URL) | Leakage | Environment variables only, Gitleaks pre-commit + CI | ✅ CI configured |

### Required Security Controls for Implementation
1. **Input Validation:** Pydantic models for all request bodies (reuse `MarketDataCreate`, add `IndicatorComputeRequest`, `ScreenRequest`, `RankRequest`)
2. **Rate Limiting:** FastAPI middleware (e.g., `slowapi`) — 10 req/min for compute, 30 req/min for screen/rank
3. **Computation Guards:** 
   - Max symbols per request: 100
   - Max date range: 500 bars
   - Timeout: 30s per request
   - Memory limit: process-level cap via container
4. **Output Encoding:** JSON responses only (no HTML/template rendering)
5. **Secret Management:** All config via `Settings` (pydantic-settings) — already established
6. **SAST Rules:** Custom Semgrep for:
   - No raw SQL concatenation (enforced by SQLAlchemy usage)
   - No `eval`/`exec` on user input
   - No unpickling untrusted data
7. **Secret Scan:** Gitleaks with baseline (already in CI)
8. **SCA:** Snyk scan on `pyproject.toml` + `pip-audit` (already in CI)

---

## 5. Implementation Plan for DEV-2 (TECHLEAD Plan)

### Phase 1: Core Indicator Library (Days 1-3)
```
services/analysis-engine/
├── src/
│   ├── main.py                 # API endpoints (extend existing)
│   ├── indicators.py           # SMA, EMA, RSI, MACD, Volume Profile, ROC, ATR, OBV
│   ├── screening.py            # v1.0 screening logic (3 criteria)
│   ├── ranking.py              # v1.0 ranking (4 factors + reasoning)
│   ├── db.py                   # DB read layer for market_data
│   ├── models.py               # Request/Response Pydantic models
│   └── versioning.py           # Version header/param validation
├── tests/
│   ├── fixtures/               # 8 JSON fixture files from docs/testing/fixtures.md
│   ├── test_indicators.py      # Unit tests per indicator (accuracy + edge cases)
│   ├── test_screening.py       # Screening tests (pass/fail + edge cases)
│   ├── test_ranking.py         # Ranking tests (determinism, weights, reasoning)
│   └── test_integration.py     # End-to-end API tests
├── pyproject.toml              # Add slowapi, update deps
└── README.md                   # Exact run steps
```

### Phase 2: API Endpoints (Days 3-4)
- `POST /indicators/compute` — Accept `IndicatorComputeRequest`, return `AnalysisResult`
- `POST /screen` — Accept `ScreenRequest`, return screened symbols with evaluations
- `POST /rank` — Accept `RankRequest`, return ranked list with composite + reasoning
- All endpoints: version validation, rate limiting, input size caps, timeout

### Phase 3: DB Integration (Day 4-5)
- `db.py`: Async SQLAlchemy read from `market_data` hypertable
- Query by symbol list + date range, return `MarketDataCreate` list
- Handle gaps, ordering, pagination

### Phase 4: Fixtures & Golden Outputs (Day 5)
- Create `tests/fixtures/` with 8 JSON files
- Run engine once → generate 3 golden output files
- Commit golden files for regression testing

### Phase 5: Security Hardening & Gates (Day 5-6)
- Add `slowapi` rate limiting
- Add computation timeout wrapper
- Add max symbols/date-range validation
- Run `gitleaks detect`, `semgrep --config auto`, `snyk test`, `pip-audit`
- Fix all high/critical findings

### Phase 6: Tests & README (Day 6-7)
- All unit + integration tests passing
- README with verbatim clean-checkout steps
- Coverage ≥ 80% on indicator/screening/ranking modules

---

## 6. Parallelization Opportunities (for PM)

| Task | Can Run Parallel With | Reason |
|------|----------------------|--------|
| Indicator library (`indicators.py`) | Screening (`screening.py`) | Pure functions, no shared state |
| Screening (`screening.py`) | Ranking (`ranking.py`) | Different modules, shared only `indicators.py` |
| DB read layer (`db.py`) | API endpoints | Independent — DB layer used by endpoints |
| Fixture creation | All implementation | Test data prep independent |
| Security hardening | Implementation | Can be applied incrementally per file |

**Recommendation:** Assign DEV-2 to indicators → screening → ranking sequentially (dependencies), but DEV-3 (if available) can take DB layer + API endpoints in parallel once indicator interfaces are defined.

---

## 7. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `ta-lib` build failures on CI | Medium | High | Pre-build wheel in Docker; fallback to pure-Python implementations |
| Floating-point precision drift vs fixtures | Medium | Medium | Use `decimal.Decimal` for financial math; round per spec (4dp prices, 2dp RSI) |
| `ta-lib` vs custom RSI/MACD mismatch | Medium | High | **Do not use `ta-lib` for core indicators** — implement per spec exactly; `ta-lib` only for validation |
| Insufficient data edge cases | High | Medium | Exhaustive fixture coverage (8 sets); test each edge case explicitly |
| Ranking determinism failure | Low | High | Fixed percentile algorithm; sort by symbol ASC on tie; golden file regression |
| Security gate failures | Low | High | Run security tools locally before push; pre-commit hooks |

---

## 8. Verdicts

| Item | Verdict | Notes |
|------|---------|-------|
| **Architecture seams** | ✅ PASS | Clean service boundaries; ready for parallel build |
| **Contract alignment** | ❌ FAIL | Placeholder `/analyze` must be replaced with 3 real endpoints per spec |
| **Security gate readiness** | ⚠️ CONDITIONAL | CI configured; implementation must add rate limiting, timeouts, input caps |
| **Parallelization potential** | ✅ HIGH | 3-4 independent workstreams identified |
| **M2 completion estimate** | **7-10 days** | With 1 DEV; 4-5 days with 2 DEVs in parallel |

---

## 9. TECHLEAD Directives for DEV-2

1. **Do not use `ta-lib` for core indicator computation** — implement exact formulas from `indicators.md` in pure Python/NumPy. Use `ta-lib` only as a cross-check in tests.
2. **Decimal for prices** — Use `decimal.Decimal` for all price calculations; round to 4dp per spec.
3. **Version every request** — Require `criteria_version` and `algorithm_version` headers; reject unknown versions.
4. **Golden file workflow** — Generate once, commit, then test against committed goldens.
5. **Security first** — Add rate limiting and input validation **before** business logic.
6. **No shared state** — All modules pure functions; no global caches or mutable state.

---

*End of TECHLEAD Analysis Record*
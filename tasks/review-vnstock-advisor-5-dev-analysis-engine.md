# Review: vnstock-advisor-5-dev-analysis-engine

**Task Branch:** `task/vnstock-advisor-5-dev-analysis-engine-dev`
**Product:** vnstock-advisor
**Service:** analysis-engine
**Review Round:** 1
**Date:** 2026-08-02
**Reviewer:** TECHLEAD

---

## Verdict: BLOCKED

This branch is **not ready for merge**. The implementation is a skeleton/placeholder only — it does not satisfy any of the 8 acceptance criteria from the DEV task. The current `/analyze` endpoint is a contract violation (required endpoints are `/indicators/compute`, `/screen`, `/rank`), security gates are absent from CI, and `ta-lib` dependency risk is unresolved.

---

## Findings by Section

### 1. Contract Alignment — **BLOCKER**

| Aspect | Status | Detail |
|--------|--------|--------|
| **Current endpoint** | ❌ Violation | `POST /analyze` exists with hardcoded placeholder response |
| **Required endpoints** | ❌ Missing | `/indicators/compute`, `/screen`, `/rank` not implemented |
| **Contract published for TESTER/QA** | ❌ No | No OpenAPI spec generated; TESTER task (vnstock-advisor-8-tester-analysis-engine) cannot write contract tests against a placeholder |
| **Shared model usage** | ⚠️ Partial | Imports `MarketDataCreate` but uses it only for the wrong endpoint |

**Finding 1.1 (Blocker):** The `/analyze` endpoint **must be removed**. It is not in the spec (`docs/specs/screening-ranking.md` §2, §3) and actively misleads TESTER/QA. The three required endpoints must be implemented per the API contract.

**Finding 1.2 (Blocker):** No OpenAPI/Swagger output is generated. The `FastAPI` app must expose `/openapi.json` and TESTER must be given a frozen contract *before* they write tests. Add `app.openapi()` export or ensure FastAPI's default `/openapi.json` is reachable and versioned.

**Finding 1.3 (Required):** The placeholder response returns `{"ma_20": 100.0, "ma_50": 95.0, "rsi": 50.0, "volume": 1000000, "signal": "neutral"}` — these hardcoded values violate "deterministic, versioned" requirement. The real implementation must compute from actual `market_data`.

---

### 2. Security Gates — **BLOCKER**

| Gate | Status | Detail |
|------|--------|--------|
| **SAST (Semgrep)** | ❌ Not in CI | No `.github/workflows/ci.yml` exists in repo root |
| **SCA (Snyk/pip-audit)** | ❌ Not in CI | No dependency scanning configured |
| **Secret Scan (Gitleaks)** | ❌ Not in CI | No pre-commit or CI hook |
| **OWASP API Checks** | ❌ Not in CI | No API security testing configured |
| **CI Pipeline** | ❌ NONE | `ci-status/vnstock-advisor-5-dev-analysis-engine.md` reports **NONE** (no runs registered) |

**Finding 2.1 (Blocker):** Per `stack-vnstock-advisor.md` §33-44, the analysis-engine surface requires: SAST (Semgrep + custom rules), SCA (Snyk + `pip-audit`), secret-scan (Gitleaks), and input validation gates. **None are configured.** The orchestrator will mechanically reject merge at ship gate (decision #134).

**Finding 2.2 (Blocker):** No `.github/workflows/ci.yml` exists at all. This is a **repo-wide gap**, not just this branch — but this branch cannot be approved until CI exists and passes.

**Finding 2.3 (Required):** The service accepts `MarketDataCreate` input but has no Pydantic validation beyond the shared model. Add request size limits, rate limiting (per stack §33: "rate-limit per tenant"), and timeout guards on indicator computation (DoS vector).

**Finding 2.4 (Required):** `structlog` is imported but no structured logging configuration is visible. Ensure logs don't leak PII or raw market data.

---

### 3. Dependency Risk: `ta-lib` — **BLOCKER** (per TECHLEAD lesson 2026-08-02)

**Current state:** `pyproject.toml` line 15: `"ta-lib>=0.4.28"`

**Finding 3.1 (Blocker):** `ta-lib` is a **C extension** with notorious build failures on Linux/musl (Alpine), version drift between system package and PyPI wheel, and formula implementations that **do not match** the exact formulas in `docs/specs/indicators.md` (periods, edge cases, NaN handling).

**Finding 3.2 (Blocker):** The task explicitly requires: *"Indicator formulas match `docs/specs/indicators.md` exactly (periods, edge cases)"*. Using `ta-lib` as the primary implementation **cannot guarantee this** — its SMA/EMA/RSI/MACD defaults differ from common financial definitions (e.g., RSI smoothing method, MACD signal line calculation).

**Required Change (file-level):**
- **Remove `ta-lib` from `pyproject.toml` dependencies** (line 15)
- **Implement all indicators in pure Python/NumPy/pandas** in `src/indicators.py` with exact formulas from spec
- **Add `ta-lib` ONLY as a `dev` optional dependency** for cross-check tests: `pytest --ta-lib-cross-check`
- Cross-check tests: compute with pure implementation, compute with `ta-lib`, assert numerical equivalence within tolerance — **fail CI if drift detected**

**Rationale:** This is exactly the pattern from my 2026-08-02 lesson: "explicitly directed DEV to implement exact formulas in pure Python/NumPy, use `ta-lib` only for cross-check in tests." Pure Python/NumPy is deterministic, auditable, and has zero build risk.

---

### 4. Parallelization Seams — **ARCHITECTURAL REQUIREMENT**

**Stack decision (§46-55):** `analysis-engine` can build in parallel after `data-ingest` contract frozen. The emergency debate (referenced in task context) mandated decomposition into parallel packages.

**Finding 4.1 (Required):** The current monolithic `main.py` **must be decomposed** into three independent modules with clean interfaces:

```
services/analysis-engine/src/
├── indicators.py      # Pure computation: SMA, EMA, RSI, MACD, Volume Profile
├── screening.py       # Pure logic: price > SMA20, RSI < 70, volume > 1.5× avg
├── ranking.py         # Pure logic: 4-factor composite (40/30/20/10) + reasoning
├── db.py              # DB read layer for market_data (shared models)
├── api.py             # FastAPI endpoints only: /indicators/compute, /screen, /rank
└── main.py            # App factory, wiring, lifespan
```

**Finding 4.2 (Required):** Each module must have **zero external dependencies** on the others — they communicate via typed Pydantic models (define in `src/schemas.py` or reuse shared). This enables:
- Parallel DEV work: DEV-2a (indicators), DEV-2b (screening), DEV-2c (ranking)
- Independent unit testing with fixtures
- Determinism verification per module
- Future extraction to separate services if needed

**Finding 4.3 (Required):** The DB read layer (`db.py`) must be a **separate module** with a clear interface (e.g., `MarketDataRepository` protocol) so it can be mocked in tests and swapped for different data sources.

---

### 5. Determinism Requirements — **BLOCKER**

**Spec requirement (`screening-ranking.md` §4):** *"Ranking must be bit-identical on same input"*

**Finding 5.1 (Blocker):** Current architecture has **no determinism guarantees**:
- Floating-point operations in pandas/NumPy can vary by BLAS implementation, CPU architecture, or Python version
- No fixed random seeds (not applicable here but worth noting)
- No explicit sorting tie-breakers in ranking
- No version pinning of computation logic

**Required Changes:**
- **Pin NumPy/pandas versions exactly** in `pyproject.toml` (e.g., `numpy==1.26.4`, `pandas==2.2.1`) — no `>=` ranges for computation deps
- **Use `decimal.Decimal` for all financial math** where bit-identical results are required, or document the exact float64 algorithm with test vectors
- **Ranking tie-breaker:** Add explicit deterministic tie-break (e.g., sort by symbol ASCII) in `ranking.py`
- **Version the computation logic:** Add `COMPUTATION_VERSION = "v1.0"` constant in each module; include in API response metadata
- **Test determinism:** Add test that calls `/rank` twice with identical input and asserts `response1.json() == response2.json()` (byte-for-byte)

---

### 6. Versioning — **REQUIRED**

**Spec requirement:** *"Both screening v1.0 and ranking v1.0 are frozen — implementation must pin versions."*

**Finding 6.1 (Required):** No version constants exist in the codebase. The implementation must:
- Define `SCREENING_VERSION = "v1.0"` in `screening.py`
- Define `RANKING_VERSION = "v1.0"` in `ranking.py`
- Include version in API responses: `{ "screening_version": "v1.0", "results": [...] }`
- Reject requests asking for other versions (return 400 with clear error)

**Finding 6.2 (Required):** Weights for ranking (momentum 40%, trend 30%, volume 20%, volatility 10%) must be **configurable via environment** but **default to frozen v1.0 values**. Add to `config.py`:
```python
RANKING_WEIGHTS = {
    "momentum": 0.40,
    "trend": 0.30,
    "volume": 0.20,
    "volatility": 0.10,
}
```
Document that changing weights produces a new ranking version (v1.1+).

---

## Concrete Required Changes for DEV-2

### File-Level Changes

| File | Action | Detail |
|------|--------|--------|
| `src/main.py` | **DELETE `/analyze` endpoint** | Remove lines 35-52 entirely |
| `src/main.py` | **Add 3 endpoints** | `POST /indicators/compute`, `POST /screen`, `POST /rank` |
| `src/indicators.py` | **CREATE** | Pure Python/NumPy implementation of SMA, EMA, RSI, MACD, Volume Profile |
| `src/screening.py` | **CREATE** | Screening logic per `screening-ranking.md` §2 (v1.0) |
| `src/ranking.py` | **CREATE** | Ranking logic per `screening-ranking.md` §3 (v1.0) with reasoning array |
| `src/db.py` | **CREATE** | `MarketDataRepository` protocol + implementation using shared models |
| `src/schemas.py` | **CREATE** | Request/Response Pydantic models for the 3 endpoints |
| `src/config.py` | **CREATE** | Version constants, ranking weights, computation version |
| `pyproject.toml` | **MODIFY** | Remove `ta-lib` from `dependencies`; add to `optional-dependencies.dev` |
| `pyproject.toml` | **MODIFY** | Pin `numpy==1.26.4`, `pandas==2.2.1` (exact versions) |
| `tests/` | **CREATE** | Fixture-based tests per `docs/testing/fixtures.md` (8 fixture sets) |
| `README.md` | **CREATE** | Exact run steps (Docker Compose, local, test commands) |

### Function-Level Specifications

#### `src/indicators.py`
```python
# Required functions (exact signatures)
def compute_sma(prices: list[float], period: int) -> list[float | None]: ...
def compute_ema(prices: list[float], period: int) -> list[float | None]: ...
def compute_rsi(prices: list[float], period: int = 14) -> list[float | None]: ...
def compute_macd(prices: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[list[float|None], list[float|None], list[float|None]]: ...
def compute_volume_profile(volumes: list[int], prices: list[float], bins: int = 20) -> dict: ...
```
- All functions **pure**, **deterministic**, **no side effects**
- Return `None` for insufficient data (not NaN, not exception)
- Edge cases: empty list, single element, all same values, NaN in input

#### `src/screening.py`
```python
def screen_symbols(market_data: list[MarketDataRead], params: ScreeningParams = ScreeningParams_v1()) -> ScreeningResult:
    """
    Screening v1.0 rules:
    - price > SMA20 (close > SMA(20))
    - RSI < 70 (RSI(14) < 70)
    - volume > 1.5 × avg_volume (volume > 1.5 * SMA(20, volume))
    """
```

#### `src/ranking.py`
```python
def rank_symbols(screened: list[ScreenedSymbol], weights: RankingWeights = RANKING_WEIGHTS_v1) -> RankedResult:
    """
    Ranking v1.0: 4-factor composite
    - momentum (40%): price change over lookback
    - trend (30%): SMA slope / ADX equivalent
    - volume (20%): relative volume vs average
    - volatility (10%): ATR or std dev normalized
    Returns: list of RankedSymbol with score, reasoning[], version
    """
```

---

## Decomposition into Parallel DEV Packages: **YES**

**Recommendation:** Split this task into **three parallel DEV packages** immediately:

| Package | Owner | Scope | Dependencies |
|---------|-------|-------|--------------|
| `vnstock-advisor-5a-dev-indicators` | DEV-2a | `indicators.py` + tests + fixtures | `market_data` schema only |
| `vnstock-advisor-5b-dev-screening` | DEV-2b | `screening.py` + tests + fixtures | `indicators.py` interface (SMA, RSI) |
| `vnstock-advisor-5c-dev-ranking` | DEV-2c | `ranking.py` + tests + fixtures | `screening.py` output + `indicators.py` |

**Rationale:**
- Each package is **independently testable** with fixture data
- **Zero coupling** between packages at implementation level (only typed interfaces)
- Enables **true parallel development** (3 DEV instances simultaneously)
- Matches stack decision §46-55 parallelization case
- Reduces single-branch blast radius; each can be reviewed/merged independently
- `api.py` and `main.py` wiring can be a **fourth tiny task** (`vnstock-advisor-5d-dev-api`) once the three cores are APPROVED

**PM Action Required:** Create the three sub-tasks in backlog, assign to DEV-2a/2b/2c (or spin up new DEV instances via HR). The current `vnstock-advisor-5-dev-analysis-engine` task becomes a **meta-task** tracking the roll-up.

---

## CI Status Gate (Decision #134)

**Current:** `ci-status/vnstock-advisor-5-dev-analysis-engine.md` = **NONE**

**Requirement:** Before any `APPROVED`, the branch must have a **PASSING CI run** with:
1. `pip-audit` / `pip-audit --desc` clean (no high/critical)
2. `gitleaks detect --source . --no-banner` clean
3. `semgrep ci --config=p/security-audit` clean (or custom rules)
4. `pytest` with coverage ≥ 80% on new modules
5. Determinism test passing (double-invoke `/rank`)

**Do not approve until CI is green.** The orchestrator mechanically re-checks at merge time.

---

## Security Review Disposition (for `apps/vnstock-advisor/docs/security-review.md`)

| Finding | Severity | Disposition |
|---------|----------|-------------|
| No SAST/SCA/secret-scan in CI | Critical | Must fix before merge (repo-wide) |
| `ta-lib` build risk + formula drift | High | Remove from deps; pure Python impl |
| No rate limiting / timeout guards | Medium | Add in `api.py` before merge |
| No input size limits on endpoints | Medium | Add Pydantic `max_length` / FastAPI `Body(max_size=...)` |
| Structured logging without PII filter | Low | Add structlog processor to redact |

---

## Round 1 Summary

| Category | Status | Blockers |
|----------|--------|----------|
| Contract Alignment | ❌ FAIL | Wrong endpoint, no OpenAPI for TESTER |
| Security Gates | ❌ FAIL | No CI, no SAST/SCA/secret-scan |
| Dependency Risk | ❌ FAIL | `ta-lib` must be removed from runtime deps |
| Parallelization Seams | ❌ FAIL | Monolithic; must decompose to 3 modules |
| Determinism | ❌ FAIL | No version pinning, no bit-identical guarantee |
| Versioning | ❌ FAIL | No v1.0 constants in code |

**Overall:** **BLOCKED** — 6/6 sections have blockers. No `APPROVED` possible until all are resolved.

---

## Next Steps for DEV-2

1. **Immediately:** Remove `ta-lib` from `pyproject.toml` dependencies; pin numpy/pandas exact versions
2. **Day 1-2:** Create `indicators.py`, `screening.py`, `ranking.py`, `db.py`, `schemas.py`, `config.py` with pure implementations
3. **Day 2-3:** Write fixture-based tests (use `docs/testing/fixtures.md` — 8 sets)
4. **Day 3:** Add 3 API endpoints in `api.py`; wire in `main.py`
5. **Day 3-4:** Write README with exact run steps
6. **Before push:** Run `pip-audit`, `gitleaks`, `semgrep` locally; ensure all pass
7. **Push:** CI will run; must be GREEN before requesting re-review

**PM:** Please decompose into 3 parallel DEV packages per above table. This unblocks parallel velocity and matches the architecture mandate.

---

**Report to CTO:** Review completed for `vnstock-advisor-5-dev-analysis-engine`. Verdict: **BLOCKED** (6 blockers across all 6 review dimensions). The branch is a skeleton/placeholder — no functional implementation exists. Critical findings: (1) wrong API contract (`/analyze` vs 3 required endpoints), (2) zero security gates in CI, (3) `ta-lib` dependency risk violating spec fidelity, (4) monolithic structure preventing parallelization, (5) no determinism/versioning architecture. Required: decompose into 3 parallel DEV packages (indicators/screening/ranking), implement pure Python/NumPy indicators, add CI pipeline with SAST/SCA/secret-scan, pin computation versions. No re-review until CI green and all 6 sections addressed.
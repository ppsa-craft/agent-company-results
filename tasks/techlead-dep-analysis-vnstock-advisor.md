# TECHLEAD Dependency Graph Analysis — vnstock-advisor

**Date:** 2026-08-02  
**Stack Record:** `tasks/stack-vnstock-advisor.md` (2026-07-31)  
**Codebase Root:** `workspace/apps/vnstock-advisor/`  
**Analysis Scope:** Four services (`data-ingest`, `analysis-engine`, `suggestion-api`, `web-ui`) + shared contracts

---

## 1. Service Contract Inventory

| Service | Language | Published Contract | Data Schemas Consumed/Produced | Implementation Status |
|---------|----------|-------------------|--------------------------------|----------------------|
| **data-ingest** | Python 3.11+ / FastAPI | ✅ **Functional** — OpenAPI via FastAPI at `/openapi.json` | **Consumes:** External (CAFEF, VNDIRECT) HTTP JSON<br>**Produces:** `MarketDataCreate` (shared/python) → PostgreSQL `market_data` hypertable + `IngestRunResponse` / `HealthCheck` | **Functional** — Full ingestion pipeline with fallback, scheduler, health checks, comprehensive tests (350 lines) |
| **analysis-engine** | Python 3.11+ / FastAPI | ⚠️ **Partial** — Only `/analyze` placeholder exists; **missing `/rank`** required by suggestion-api | **Consumes:** `MarketDataCreate` (shared/python) from `market_data` table<br>**Produces:** Placeholder `AnalysisResultBase` dict (not validated against shared model) | **Placeholder** — Only `/health` and `/analyze` (hardcoded response). No technical indicators, screening, or ranking logic. Tests only verify placeholder behavior. |
| **suggestion-api** | Node.js 20+ / Fastify | ❌ **Missing** — Only `/health` endpoint; **no `/suggestions`** or `/rank` client | **Consumes:** Should call `analysis-engine` `/rank` (not implemented)<br>**Produces:** Should return `SuggestionSchema` (shared/typescript) array | **Skeleton** — Fastify + security plugins (helmet, cors, rate-limit, jwt) registered. JWT uses **HS256 dev secret** (violates stack record §41). No business endpoints. |
| **web-ui** | React 18 / Vite / TypeScript | ❌ **Missing** — Static SPA; calls `/api/health` only | **Consumes:** Should call `suggestion-api` `/suggestions` (not implemented)<br>**Produces:** N/A (frontend) | **Static** — Single `App.tsx` fetching health. No routing, no suggestion display, no chart integration. Tests only mock health fetch. |

### Shared Contract Packages
| Package | Location | Schemas Defined | Validation |
|---------|----------|-----------------|------------|
| `vnstock-shared-python` | `shared/python/src/vnstock_shared/models/__init__.py` | `MarketDataCreate`, `MarketDataRead`, `MarketDataBatch`, `SuggestionBase`, `SuggestionCreate`, `SuggestionRead`, `AnalysisResultBase`, `AnalysisResultCreate`, `AnalysisResultRead`, `HealthCheck` | Pydantic v2 + SQLAlchemy ORM |
| `@vnstock/shared-typescript` | `shared/typescript/src/index.ts` | `MarketDataSchema`, `SuggestionSchema`, `AnalysisResultSchema`, `HealthCheckSchema`, `ApiResponseSchema`, `PaginatedResponseSchema` | Zod v3 |

---

## 2. Dependency Graph (Actual Code-Level)

```
┌─────────────────┐     market_data table      ┌──────────────────────┐
│   data-ingest   │ ─────────────────────────► │  analysis-engine     │
│  (Python/FastAPI)│  (TimescaleDB hypertable)  │  (Python/FastAPI)    │
└────────┬────────┘                            └──────────┬───────────┘
         │                                                │
         │ /ingest/health                                 │ /analyze (placeholder)
         │ /ingest/run                                    │ ❌ /rank (MISSING)
         │                                                │
         │                                                ▼
         │                                       ┌──────────────────────┐
         │                                       │   suggestion-api     │
         │                                       │  (Node.js/Fastify)   │
         │                                       └──────────┬───────────┘
         │                                                  │
         │                                                  │ ❌ /suggestions (MISSING)
         │                                                  │ calls analysis-engine /rank
         │                                                  ▼
         │                                        ┌──────────────────────┐
         │                                        │      web-ui          │
         │                                        │ (React/Vite/TypeScript)│
         │                                        └──────────────────────┘
         │                                                  ▲
         │                                                  │ calls /suggestions
         └──────────────────────────────────────────────────┘
```

### Contractual Dependencies (from stack record §46-55)

| Dependency | Required Contract | Current Status | Blocker |
|------------|-------------------|----------------|---------|
| `data-ingest` → `analysis-engine` | `market_data` table schema + `MarketDataCreate` | ✅ Table exists (init-db.sql), Python model aligned | **Frozen** — data-ingest contract stable |
| `analysis-engine` → `suggestion-api` | OpenAPI spec with `/rank` endpoint returning `AnalysisResultSchema` | ❌ **Missing `/rank`**; only `/analyze` placeholder | **BLOCKER** — suggestion-api cannot proceed |
| `suggestion-api` → `web-ui` | OpenAPI spec with `/suggestions` endpoint returning `SuggestionSchema[]` | ❌ **Missing `/suggestions`** endpoint entirely | **BLOCKER** — web-ui cannot integrate |

---

## 3. Contract Gaps & Blockers

### 3.1 Missing `/rank` Endpoint on analysis-engine (CRITICAL)

**Stack Record §51-52:** `analysis-engine` must expose `/rank` for `suggestion-api` to call.

**Current Code** (`services/analysis-engine/src/main.py:36-52`):
```python
@app.post("/analyze")
async def analyze_data(data: MarketDataCreate):
    # Placeholder: returns hardcoded dict, NOT AnalysisResultBase
    return {
        "symbol": data.symbol,
        "timeframe": data.timeframe,
        "analysis": { "ma_20": 100.0, "ma_50": 95.0, "rsi": 50.0, ... },
        "note": "This is a placeholder response..."
    }
```

**Required Contract** (per shared models):
```python
# Python: shared/python/src/vnstock_shared/models/__init__.py:85-99
class AnalysisResultBase(BaseModel):
    symbol: str
    indicators: dict[str, float]
    signals: list[str]  # pattern: BUY|SELL|NEUTRAL
    trend: str          # pattern: BULLISH|BEARISH|SIDEWAYS
    strength: float     # 0.0-1.0
    timestamp: datetime
```

**Gap:** No `/rank` endpoint exists. The `/analyze` placeholder:
- Returns a non-conforming dict (extra `timeframe`, `analysis` wrapper, `note`)
- Does not validate against `AnalysisResultBase`
- Has no technical indicator computation (ta-lib, pandas-ta not used)

### 3.2 Missing `/suggestions` Endpoint on suggestion-api (CRITICAL)

**Stack Record §52-53:** `suggestion-api` must expose `/suggestions` for `web-ui`.

**Current Code** (`services/suggestion-api/src/index.ts:18-30`):
```typescript
// Only health endpoint exists
app.get('/health', async () => { ... });
app.get('/', async () => { return { message: 'vnstock Suggestion API' }; });
```

**Required Contract** (per shared types):
```typescript
// shared/typescript/src/index.ts:20-32
export const SuggestionSchema = z.object({
  id: z.string().uuid(),
  symbol: z.string().min(1).max(20),
  action: z.enum(['BUY', 'SELL', 'HOLD']),
  confidence: z.number().min(0).max(1),
  reasoning: z.string().min(1).max(500),
  targetPrice: z.number().positive().optional(),
  stopLoss: z.number().positive().optional(),
  timeframe: z.enum(['1D', '1W', '1M', '3M']),
  createdAt: z.string().datetime(),
});
```

**Gap:** No `/suggestions` route, no client for `analysis-engine` `/rank`, no ranking/aggregation logic.

### 3.3 Shared Model Drift: MarketData (Python vs TypeScript)

| Field | Python `MarketDataCreate` | TypeScript `MarketDataSchema` | Alignment |
|-------|---------------------------|-------------------------------|-----------|
| `time` | `datetime` (tz-aware) | `z.string().datetime()` | ✅ ISO 8601 string ↔ datetime |
| `symbol` | `str` (1-20) | `z.string().min(1).max(20)` | ✅ |
| `open` | `Decimal` (gt=0) | `z.number().positive()` | ⚠️ **Decimal vs float** — precision loss risk |
| `high` | `Decimal` (gt=0) | `z.number().positive()` | ⚠️ Same |
| `low` | `Decimal` (gt=0) | `z.number().positive()` | ⚠️ Same |
| `close` | `Decimal` (gt=0) | `z.number().positive()` | ⚠️ Same |
| `volume` | `int` (ge=0) | `z.number().int().nonnegative()` | ✅ |
| `source` | `str` (1-50) | `z.string().min(1).max(50)` | ✅ |

**Risk:** Financial prices as `Decimal` in Python but `number` (IEEE 754 float) in TypeScript. For VN stocks (prices ~1,000–100,000 VND), float53 precision is adequate but **not guaranteed** for sub-pip calculations. Recommendation: Use string serialization for prices in JSON contracts, or document acceptable precision loss.

### 3.4 Shared Model Drift: AnalysisResult (Python vs TypeScript)

| Field | Python `AnalysisResultBase` | TypeScript `AnalysisResultSchema` | Alignment |
|-------|----------------------------|-----------------------------------|-----------|
| `symbol` | `str` (1-20) | `z.string().min(1).max(20)` | ✅ |
| `indicators` | `dict[str, float]` | `z.record(z.string(), z.number())` | ✅ |
| `signals` | `list[str]` (pattern: BUY\|SELL\|NEUTRAL) | `z.array(z.enum(['BUY','SELL','NEUTRAL']))` | ✅ **Stricter in TS** (good) |
| `trend` | `str` (pattern: BULLISH\|BEARISH\|SIDEWAYS) | `z.enum(['BULLISH','BEARISH','SIDEWAYS'])` | ✅ **Stricter in TS** (good) |
| `strength` | `float` (0.0-1.0) | `z.number().min(0).max(1)` | ✅ |
| `timestamp` | `datetime` | `z.string().datetime()` | ✅ |

**Verdict:** AnalysisResult schemas are **well-aligned**. TypeScript version is stricter (enums vs regex patterns), which is safer.

### 3.5 Shared Model Drift: Suggestion (Python vs TypeScript)

| Field | Python `SuggestionBase` | TypeScript `SuggestionSchema` | Alignment |
|-------|------------------------|-------------------------------|-----------|
| `symbol` | `str` (1-20) | `z.string().min(1).max(20)` | ✅ |
| `action` | `str` (pattern: BUY\|SELL\|HOLD) | `z.enum(['BUY','SELL','HOLD'])` | ✅ **Stricter in TS** |
| `confidence` | `float` (0.0-1.0) | `z.number().min(0).max(1)` | ✅ |
| `reasoning` | `str` (1-500) | `z.string().min(1).max(500)` | ✅ |
| `target_price` | `Optional[Decimal]` (gt=0) | `z.number().positive().optional()` | ⚠️ **Decimal vs float** |
| `stop_loss` | `Optional[Decimal]` (gt=0) | `z.number().positive().optional()` | ⚠️ **Decimal vs float** |
| `timeframe` | `str` (pattern: 1D\|1W\|1M\|3M) | `z.enum(['1D','1W','1M','3M'])` | ✅ **Stricter in TS** |
| `created_at` | `datetime` (on Read) | `z.string().datetime()` (required) | ⚠️ **Python has separate Create/Read; TS requires always** |

**Risk:** Python separates `SuggestionCreate` (no `id`, `created_at`) from `SuggestionRead`; TypeScript `SuggestionSchema` requires all fields including `id` and `createdAt`. This will cause validation failures when Python creates suggestions without those fields.

---

## 4. Parallelization Readiness (per Stack Record §46-55)

| Service Pair | Can Build in Parallel? | Contract Frozen? | Fixture Data / Spec Required |
|--------------|------------------------|------------------|------------------------------|
| **data-ingest** + **analysis-engine** | ⚠️ **Conditional YES** | data-ingest: **YES** (table + models stable)<br>analysis-engine: **NO** (missing `/rank`) | analysis-engine needs:<br>1. `market_data` table schema (✅ exists in init-db.sql)<br>2. Sample OHLCV rows for indicator testing<br>3. `MarketDataCreate` model (✅ shared) |
| **analysis-engine** + **suggestion-api** | ❌ **NO** | analysis-engine `/rank`: **MISSING** | suggestion-api needs:<br>1. OpenAPI spec for `analysis-engine` `/rank` (request/response)<br>2. Contract test fixtures for `AnalysisResultSchema`<br>3. Network connectivity (service discovery) |
| **suggestion-api** + **web-ui** | ❌ **NO** | suggestion-api `/suggestions`: **MISSING** | web-ui needs:<br>1. OpenAPI spec for `suggestion-api` `/suggestions`<br>2. Auth token flow (JWT RS256)<br>3. Error response format (Problem Details RFC 7807) |

### Recommendation (Stack Record §55)
> Start `data-ingest` + `analysis-engine` in parallel (DEV-1 + DEV-2) once `data-ingest` contract is published.

**Current Reality:** `data-ingest` contract **is** published and functional. `analysis-engine` can start **implementation** (not just planning) in parallel because:
- Database schema is frozen (`init-db.sql`)
- `MarketDataCreate` model is stable
- Only the **output contract** (`/rank` → `AnalysisResultSchema`) needs to be agreed before `suggestion-api` starts

**Action:** TECHLEAD should approve `analysis-engine` `/rank` endpoint contract **now** (as an ADR or OpenAPI fragment) so `suggestion-api` DEV can begin stubbing the client.

---

## 5. Security Gate Readiness (per Stack Record §33-45)

### 5.1 CI/CD Security Tooling Status

| Tool | Configured? | Location | Status |
|------|-------------|----------|--------|
| **GitHub Actions CI** | ❌ **NO** | `.github/workflows/` empty | **BLOCKER** — No automated gates |
| **Semgrep (SAST)** | ❌ **NO** | No config | Required per stack record §44 |
| **Gitleaks (Secret Scan)** | ❌ **NO** | No config/pre-commit | Required per stack record §44 |
| **Snyk (SCA + SBOM)** | ❌ **NO** | No config | Required per stack record §44 |
| **pip-audit / npm audit** | ❌ **NO** | Not in CI | Required per stack record §31 |
| **OWASP API Top 10 Tests** | ❌ **NO** | No test files | Required for suggestion-api §39 |
| **XSS/CSP Tests (web-ui)** | ❌ **NO** | No test files | Required for web-ui §40 |

**Critical Finding:** The `README.md` §161-169 **claims** CI runs all these checks, but **no workflow files exist**. This is a documentation-reality gap that will fail QA ship gate.

### 5.2 Per-Service Security Posture

| Service | Surface | Required Controls (Stack §35-41) | Implemented | Gaps |
|---------|---------|----------------------------------|-------------|------|
| **data-ingest** | External HTTP → DB | Allowlist URLs, Pydantic validation, parameterized SQL, pip-audit | ✅ httpx with hardcoded URLs<br>✅ Pydantic models<br>✅ SQLAlchemy ORM<br>❌ pip-audit in CI | No CI, no allowlist config (URLs hardcoded), no Semgrep rules |
| **analysis-engine** | Internal API | Rate-limit, Pydantic query validation, timeout guards, input sanitization | ❌ No rate-limit<br>❌ No timeout guards<br>✅ Pydantic on `/analyze` | Placeholder only; no real attack surface yet |
| **suggestion-api** | Public REST (OWASP API Top 10) | Helmet, CORS, rate-limit, JWT RS256, Zod validation, Problem Details | ✅ Helmet/CORS/rate-limit<br>✅ Zod (shared types)<br>❌ **JWT uses HS256 dev secret** (violates §41)<br>❌ No Problem Details errors<br>❌ No auth/z tests | **CRITICAL:** HS256 dev secret in production code path |
| **web-ui** | Browser (XSS, CSP, CSRF) | React auto-escape, strict CSP, SameSite=Strict, helmet, no dangerouslySetInnerHTML | ✅ React JSX auto-escape<br>✅ Tailwind (no dangerouslySetInnerHTML)<br>❌ No CSP header (no server)<br>❌ No SameSite cookies (no auth)<br>❌ No XSS tests | Static SPA served by Vite dev server — production CSP requires nginx/Cloudflare config |
| **auth (JWT)** | Token signing | RS256 only, short access + refresh rotation, JWKS endpoint | ❌ **HS256 dev secret** in suggestion-api<br>❌ No JWKS endpoint<br>❌ No refresh rotation | **CRITICAL:** Stack record §41 mandates RS256 only |

### 5.3 Immediate Security Fixes Required

1. **suggestion-api JWT:** Replace `secret: process.env.JWT_PRIVATE_KEY || 'dev-secret-change-in-production'` with RS256 asymmetric keys per `shared/python/config/__init__.py:28-32` (already expects `jwt_private_key`/`jwt_public_key`).
2. **CI Pipeline:** Create `.github/workflows/ci.yml` with:
   - Semgrep (Python + TypeScript rulesets)
   - Gitleaks (pre-commit + CI)
   - Snyk (SCA + CycloneDX SBOM)
   - `pip-audit` / `npm audit`
   - Contract test execution
3. **Problem Details:** Implement RFC 7807 error responses in suggestion-api (Fastify `setErrorHandler`).
4. **CSP Header:** Add `helmet.contentSecurityPolicy` config to suggestion-api; document web-ui production CSP requirements.

---

## 6. Recommended Next Steps for TECHLEAD Reviews

### 6.1 Review Priority Queue (When PRs Land)

| Priority | Service | Reason | Review Criteria (code-review-and-quality skill) |
|----------|---------|--------|-------------------------------------------------|
| **1** | `data-ingest` | **Functional, tested, contract frozen** — first merge candidate | • Correctness: ingestion pipeline, fallback, duplicate handling<br>• Security: SSRF (hardcoded URLs), input validation, secrets<br>• Architecture: Clean separation (models, service, main)<br>• Performance: Async HTTP, connection pooling, batch size limits<br>• Readability: Structured logging, type hints, docstrings |
| **2** | `analysis-engine` | **Needs `/rank` contract + implementation** — unblocks suggestion-api | • Correctness: Technical indicators (ta-lib), ranking algorithm<br>• Architecture: Separation of indicator calc from HTTP layer<br>• Security: DoS guards (timeout, rate-limit), input sanitization<br>• Contract: `/rank` OpenAPI spec matching `AnalysisResultSchema`<br>• Tests: Property-based tests for indicator math, contract tests |
| **3** | `suggestion-api` | **Needs `/suggestions` + JWT RS256 fix** — unblocks web-ui | • Security (CRITICAL): JWT RS256, OWASP API Top 10, rate-limit, auth/z<br>• Correctness: Rank aggregation, suggestion formatting, error handling<br>• Architecture: Fastify plugin structure, shared-typescript consumption<br>• Contract: `/suggestions` OpenAPI spec matching `SuggestionSchema[]`<br>• Performance: Caching (Redis), pagination, connection pooling |
| **4** | `web-ui` | **Needs integration + features** — final user-facing piece | • Security: XSS (no dangerouslySetInnerHTML), CSP, CORS<br>• Correctness: TanStack Query integration, error boundaries<br>• Architecture: Component structure, state management (zustand)<br>• Readability: Tailwind design system, chart.js integration<br>• Accessibility: Semantic HTML, ARIA, keyboard navigation |

### 6.2 Per-Service Review Checklist (from code-review-and-quality skill)

#### data-ingest (READY FOR REVIEW)
```
## Review: data-ingest implementation

### Context
- Implements market data ingestion from CAFEF/VNDIRECT to TimescaleDB
- Spec: BA docs (vnstock-advisor-2-ba-data-ingest), Stack record §11

### Correctness
- [ ] Ingestion job handles primary + fallback sources correctly
- [ ] Duplicate detection via unique constraint works (test: test_both_sources_fail)
- [ ] Non-trading day skipping works (test: test_run_ingestion_job_non_trading_day)
- [ ] Manual trigger `/ingest/run` validates date format and trading day
- [ ] Health check reports DB + source connectivity accurately

### Readability
- [ ] Names clear: `run_ingestion_job`, `fetch_from_cafef`, `OHLCV.normalize()`
- [ ] No nested ternaries or deep callbacks
- [ ] Structured logging with structlog throughout

### Architecture
- [ ] Clean separation: models.py / ingest_service.py / main.py
- [ ] Shared models consumed correctly (MarketDataCreate)
- [ ] No circular dependencies
- [ ] File sizes healthy (<200 lines each)

### Security
- [ ] No hardcoded secrets (API keys via env)
- [ ] External URLs hardcoded but not user-controlled (SSRF low risk)
- [ ] Pydantic validation on all external responses
- [ ] SQLAlchemy ORM prevents SQL injection
- [ ] TODO: Add Semgrep rules for hardcoded URLs, missing input validation

### Performance
- [ ] Async HTTP with httpx + retry/backoff
- [ ] Single DB transaction per symbol (could batch)
- [ ] No N+1 (each symbol independent)
- [ ] TODO: Add batch upsert for high-volume symbols

### Verification
- [ ] 350-line test suite covers happy path, fallback, errors, edge cases
- [ ] pytest-asyncio for async tests
- [ ] Build passes (ruff, mypy, pytest)

### Verdict
- [ ] **Approve** — Ready to merge
```

#### analysis-engine (NEEDS CONTRACT FIRST)
```
## Review: analysis-engine /rank endpoint contract + implementation

### Prerequisite (PRE-REVIEW)
- [ ] TECHLEAD publishes `/rank` OpenAPI contract (request: MarketDataCreate batch, response: AnalysisResultSchema[])
- [ ] Contract reviewed by PM for business alignment (ranking criteria, timeframes)
- [ ] Fixture data generated from data-ingest for DEV testing

### Correctness
- [ ] Technical indicators: MA(20/50), RSI(14), Volume SMA, Bollinger Bands
- [ ] Screening: liquidity filter, price filter, volatility filter
- [ ] Ranking: composite score with configurable weights
- [ ] Output validates against AnalysisResultSchema (signals enum, trend enum)

### Security
- [ ] Rate-limit per tenant (FastAPI dependency)
- [ ] Timeout guards on indicator computation (asyncio.wait_for)
- [ ] Input sanitization: pandas/numpy arrays validated before ta-lib
- [ ] No DoS via large batch requests (max batch size enforced)

### Architecture
- [ ] Indicator library separate from HTTP layer (testable in isolation)
- [ ] No feature logic in shared modules
- [ ] Configuration-driven weights (not hardcoded)

### Verdict
- [ ] **Request Changes** until contract published and implementation matches
```

#### suggestion-api (BLOCKED ON analysis-engine CONTRACT)
```
## Review: suggestion-api /suggestions endpoint + JWT RS256

### Prerequisite
- [ ] analysis-engine `/rank` contract frozen
- [ ] JWT RS256 keys configured (not HS256 dev secret)

### Security (CRITICAL AXIS)
- [ ] JWT: RS256 only, algorithms: ["RS256"], JWKS endpoint exposed
- [ ] OWASP API Top 10: Broken auth (JWT), Rate limit (✅), Injection (Zod), Data exposure (Problem Details)
- [ ] Secret scan clean (Gitleaks in CI)
- [ ] SCA clean (Snyk in CI)
- [ ] Helmet/CORS/Rate-limit configured correctly

### Correctness
- [ ] Calls analysis-engine `/rank` with proper timeout/retry
- [ ] Aggregates rankings → suggestions (BUY/SELL/HOLD with confidence)
- [ ] Returns SuggestionSchema[] with all required fields (id, createdAt)
- [ ] Problem Details (RFC 7807) error responses

### Architecture
- [ ] Fastify plugin structure: routes, services, plugins separated
- [ ] Shared types consumed via @vnstock/shared-typescript
- [ ] No business logic in route handlers (delegated to services)

### Verdict
- [ ] **Request Changes** until JWT RS256 fixed and /suggestions implemented
```

#### web-ui (LAST, DEPENDS ON suggestion-api)
```
## Review: web-ui suggestion dashboard integration

### Prerequisite
- [ ] suggestion-api `/suggestions` contract frozen
- [ ] Auth flow (JWT) designed

### Security
- [ ] No dangerouslySetInnerHTML (Tailwind only)
- [ ] CSP header documented for production deployment
- [ ] XSS tests: payload injection in symbol search, suggestion rendering
- [ ] CORS test: only suggestion-api origin allowed

### Correctness
- [ ] TanStack Query fetches /suggestions with proper caching/invalidation
- [ ] Error boundaries catch API failures
- [ ] Chart.js renders price + indicator overlays
- [ ] Responsive layout (Tailwind breakpoints)

### Readability
- [ ] Component hierarchy: App → Dashboard → SuggestionList → SuggestionCard → Chart
- [ ] Zustand store for UI state (filters, selected symbol)
- [ ] TypeScript strict mode, no `any`

### Verdict
- [ ] **Approve** when integration complete and security gates pass
```

---

## 7. Summary & TECHLEAD Actions

### Immediate Actions (This Session)
1. **Publish `/rank` endpoint contract** for `analysis-engine` as ADR or OpenAPI fragment — unblocks `suggestion-api` DEV
2. **Flag JWT HS256 in suggestion-api** as CRITICAL security finding — must be RS256 before any merge
3. **Create CI workflow stub** (`.github/workflows/ci.yml`) with Semgrep, Gitleaks, Snyk placeholders — enables security gate
4. **Document MarketData Decimal/float drift** in shared package README — decision: string serialization or accept precision loss

### Next Review Cycle Priorities
| Round | Expected PR | TECHLEAD Focus |
|-------|-------------|----------------|
| 1 | `data-ingest` | Full five-axis review (functional, tested, contract frozen) |
| 2 | `analysis-engine` `/rank` | Contract conformance + indicator correctness + DoS guards |
| 3 | `suggestion-api` `/suggestions` | JWT RS256, OWASP API compliance, rank aggregation logic |
| 4 | `web-ui` integration | XSS/CSP, TanStack Query, chart rendering, accessibility |

### Recurring Findings for PM Lessons (`lessons/dev.md`)
- **Shared model drift** between Python (Decimal) and TypeScript (number) for financial fields — establish convention early (string serialization or documented precision)
- **Contract-first development** blocked by missing `/rank` — TECHLEAD should publish interface contracts as ADRs before DEV starts implementation
- **Security tooling absent from CI** despite README claims — CI must be scaffolded before first PR, not after
- **HS256 dev secret in production code path** — enforce RS256 via shared config and secret scanning from day one

---

**Report to CTO:** Analysis complete. Four services mapped. Three critical blockers identified: (1) missing `analysis-engine` `/rank` contract, (2) missing `suggestion-api` `/suggestions` endpoint, (3) JWT HS256 dev secret. Shared model drift documented for Decimal/float. CI security tooling absent. Recommended review queue prioritized: data-ingest → analysis-engine → suggestion-api → web-ui. Contract-first ADR for `/rank` needed immediately to unblock parallelization.
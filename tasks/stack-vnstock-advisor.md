# Stack Decision Record — vnstock-advisor (M1/M2/M3)

**Product:** vnstock-advisor (flagship — VN stock suggestion system)
**Owner:** CTO | **Writer:** CTO (single writer) | **Status:** v1.0, created 2026-08-12 (freeze-safe staging, drain mode #160)
**Authority:** this record + the agent-skills pack + the vendored cybersecurity skill pack DEFINE "best practice" for this product (§7.2). TECHLEAD enforces it in review; QA enforces it at the ship gate.

**Envelope compliance (§7.2):** every service below is Node.js, Python, or static-web. No envelope extension needed. TESTER runs every service in-pod via the documented README commands.

---

## 0. Cross-cutting conventions (ALL services)

- **Monorepo layout:** `apps/vnstock-advisor/` with `services/<name>/`, `shared/python/`, `docs/`, `scripts/`. One repo forever — a new service is a new `services/<name>/` directory, never a new repo.
- **Shared package** `vnstock-shared-python` (`shared/python/src/vnstock_shared/`): settings/config + data models (MarketData, HealthCheck, …). **M3 does NOT edit shared/python** (it is a merge point with pending M1/M2 PRs; each service keeps its own disclaimer constants keyed to `docs/compliance/disclaimer.md` — de-duplication is a later refactor).
- **Errors:** RFC 7807 Problem Details (`application/problem+json`) with machine-readable `code` + `trace_id` — the `problem_detail()` helper pattern already in analysis-engine `schemas.py` is the house style; reuse it (suggestion-api gets its own copy).
- **Logging:** structlog, JSON format, every request path logs success/failure + error detail (OWASP API10). No PII, no tokens, no secrets in logs.
- **Linting/typing/tests (Python):** ruff (line-length 100, root config), mypy (disallow_untyped_defs), pytest + pytest-asyncio; app-root `pyproject.toml` `[tool.pytest.ini_options]` gains the new service path + `owasp` marker is already registered.
- **Security gates (all services, §7.2.1):** committed `.gitleaks.toml` (fail on ANY secret-like finding), `.semgrep.yml` (ERROR-severity custom rules: no-hardcoded-secrets, no-eval, no-raw-sql-f-string), `.snyk` (fail CVSS>=7.0), plus a committed `tests/test_owasp_security.py` suite per service. Authoritative gitleaks/semgrep/snyk runs are orchestrator-owned CI (decision #133); in-pod evidence recorded in `SECURITY_GATE_RESULTS.md` per service.
- **Secrets:** never commit `.env`; config via env vars through `vnstock_shared.config.Settings`; dev-only placeholder values documented in docker-compose/README as dev-only (prod must override).

---

## 1. M1 — data-ingest service

| Aspect | Decision |
|---|---|
| **Stack** | Python 3.11 · FastAPI + uvicorn · Pydantic v2 · httpx (legacy, kept) + tenacity (retries) + apscheduler (daily cron) · SQLAlchemy 2 async + asyncpg → TimescaleDB/Postgres · structlog · `vnstock-shared-python` |
| **Why** | Shipped and TESTER/QA-approved (PR #12 merged). Matches the M2 service family → one runtime, one test harness, one security posture. TimescaleDB hypertable on `market_data(time, symbol)` is the canonical store (schema: `scripts/init-db.sql`, model in shared). |
| **Alternatives rejected** | Pandas-based ETL (no — stream per symbol, upsert batches); cron-in-container (no — apscheduler in-app with trading-day guard, `is_trading_day()`); raw psycopg2 (no — async SQLAlchemy is already the house ORM). |
| **Conventions** | Trading-day guard before any ingest; upsert idempotent per `(symbol, time)`; source-fallback chain CAFEF→VNDIRECT (per `docs/research/data-sources.md`: CAFEF primary — no auth, TradingView-UDF JSON `{t,o,h,l,c,v,s}`; VNDIRECT fallback); `meta` envelope carries the disclaimer on every response; port 8001 (`data_ingest_port`). |

---

## 2. M2 — analysis-engine service (indicators + ranking)

| Aspect | Decision |
|---|---|
| **Stack** | Python 3.11 · FastAPI + uvicorn · Pydantic v2 (frozen-contract schemas) · pandas + numpy (vectorized indicator math) · structlog · `vnstock-shared-python` · port 8002 (`analysis_engine_port`) |
| **Why** | Shipped on the security-gate branch (task-15, TECHLEAD-approved, pending merge). Frozen contract `docs/specs/screening-ranking.md` + `use-cases/analysis-engine.md` UC-AE-3: `POST /indicators/compute`, `POST /analyze`, `POST /rank`, `GET /health`. Ranking (`ranking.py`) is deterministic + versioned (`v1.0` frozen) with weight-set + sum-to-1.0 validation (TESTER D2 fix). |
| **Alternatives rejected** | TA-Lib (no — native C dep, heavy for in-pod); redis-cached indicators (no — v1.0 computes on demand from request `series`; caching is a later optimization); pure-Python indicator loops (no — pandas/numpy already in root requirements). |
| **Frozen `/rank` contract (M3 consumer — read-only, never change):** `POST /rank {symbols[1..100], as_of_date, algorithm_version "v1.0", weights?, series{symbol: OHLCVBar[]}}` → `{algorithm_version, as_of_date, ranked_at, weights_used, ranked[], excluded[]}`. `ranked[]` items: `{rank, symbol, composite_score, components{momentum,trend,volume,volatility}, sub_components{...}, reasoning[]}`. `excluded[]` items: `{symbol, reason, missing_indicators[]}`. **No `screening` field exists in `/rank` output.** Symbol pattern (frozen, in `schemas.py`): `^[A-Z][A-Z0-9]{0,9}$`. |
| **Conventions** | Errors as RFC 7807 via `problem_detail()`; explicit Pydantic input guards (C6: unresolvable symbols → 400 listing them, no silent drops); OWASP suite (`test_owasp_security.py`) committed; every request path logs. |

---

## 3. M3 — suggestion-api service

### 3.1 Stack

| Aspect | Decision |
|---|---|
| **Framework** | Python 3.11 · FastAPI + uvicorn · Pydantic v2 (strict) · structlog · `vnstock-shared-python` (read-only) · port 8003 (`suggestion_api_port`) |
| **JWT** | **PyJWT** (`PyJWT>=2.13`) — RS256 sign/verify + JWKS serialization. Verified healthy: 2.13.0 (2026-05), Production/Stable, MIT, sigstore-attested. **Rejected python-jose 3.5.0** (stale ~1yr, multi-backend complexity, maintenance-mode reputation) and authlib (overkill; FastAPI plugins like fastapi-jwt-auth are niche/under-maintained — no framework lock-in). |
| **Refresh tokens + rate limiting** | **redis-py** (`redis>=8.1`, async client) against the existing docker-compose Redis (7-alpine, `redis_url` already in shared config) for: opaque rotating refresh tokens with token-family revocation, and **slowapi** (`slowapi>=0.1.10`, verified active 2026-06) with the Redis storage backend for the 429 `rate_limit.exceeded` contract. Rejected: in-memory limiter storage (doesn't survive multi-worker/restart), DB-stored rate counters (Redis is right-sized and already deployed). |
| **Password hashing** | stdlib `hashlib.pbkdf2_hmac` (HMAC-SHA256, 600k iterations, per-user random 16-byte salt) — a standard-library KDF, not home-rolled crypto; zero new SCA surface. Rejected: passlib (stale), bcrypt lib (healthy but adds a dep for seeded demo users; revisit when real user registration lands — then prefer bcrypt/argon2). |
| **Internal HTTP** | **httpx2** (`httpx2>=2.10`) for the `POST /rank` client. **Supply-chain note (verified, not a typosquat):** `httpx2` is the Pydantic-stewarded continuation of httpx (Tom Christie author, Pydantic maintainer, sigstore-attested, 2026-08-09); it already sits in root `requirements.txt`. Existing M1/M2 `httpx` imports stay as-is; new M3 code uses `httpx2`. Flag to TECHLEAD: consolidation of the two HTTP clients into one is a backlog cleanup, not M3 work. |
| **DB reads** | SQLAlchemy 2 async + asyncpg (already in root requirements) — **read-only** market_data access to build per-symbol `series` for `/rank`. Parameterized queries only (semgrep `no-raw-sql-f-string` gate). |

### 3.2 Endpoints (v1.0) — corrects the pre-drafted `docs/api/suggestion-api.openapi.yaml` (that file was never approved; three divergences resolved below)

| Endpoint | Auth | Contract notes |
|---|---|---|
| `POST /auth/login` | none (rate-limited) | `{username, password}` → `200 {access_token, refresh_token, token_type: "Bearer", expires_in: 900}`. RS256 access token, **15 min TTL** per UC-SA-2 AC-02 — NOTE: shared config default `jwt_access_token_expire_minutes=30` drifts from the contract; M3 pins 15 via env. PBKDF2 verify; constant-time compare. |
| `POST /auth/refresh` | refresh token body | Rotates: old token revoked (single-use), new pair issued. **Reuse of a revoked token → 409 `auth.refresh_reuse` and the whole family is revoked** (fails closed, AC-04). |
| `GET /auth/jwks` | none | Public RSA JWK(s) (`kty: RSA`, `use: sig`, `kid`, `alg: RS256`). |
| `GET /suggestions` | Bearer RS256 + `suggestions:read` scope | Query params: `symbols` (comma-separated, optional → default universe from `SELECT DISTINCT symbol FROM market_data` capped at 100, fallback to the documented default list if DB empty) and `weights` (optional, encoded; must contain exactly the 4 keys, each [0,1], sum 1.0 ±0.001). 401/403/422/429 per UC-SA-1. **GET chosen per UC-SA-1's explicit "from query params" flow** (read-only, idempotent, cacheable) — the openapi draft's POST-style `PortfolioInput` body is rejected. |
| `GET /health` | none | liveness + checks + `meta` disclaimer envelope. |

**Response shape (data contract, downstream of frozen `/rank`):**
```json
{ "request_id": "<uuid>", "generated_at": "<iso>", "source": "analysis-engine-v1.0",
  "disclaimer": {"vi-VN": "...", "en-US": "..."},
  "ranked": [{"rank":1, "symbol":"VNM", "composite_score":78.3,
              "components": {"momentum":..,"trend":..,"volume":..,"volatility":..},
              "sub_components": {...}, "reasoning": ["..."]}],
  "excluded": [{"symbol":"ABC", "reason":"insufficient_data", "missing_indicators":[...]}] }
```
- `ranked[]`/`excluded[]` are a **1:1 passthrough of `/rank` output** (rank re-stamped by /rank already; reasoning passed untouched per UC-SA-3 step 5). `X-Disclaimer` header present on every response; `meta.disclaimer` body carries both locales (compliance/disclaimer.md is the text source of truth).
- **Decision — `screening` field is DROPPED from RankedSuggestion.** The pre-drafted openapi required it, but it is NOT in the frozen `/rank` output and cannot be derived from it (screening needs price/sma20/rsi/volume which `/rank` does not return). Adding it would force a second endpoint call per symbol (perf + coupling). Flag to PM/BA: M3 v1.0 suggestion responses carry rank/components/sub_components/reasoning only; if `screening` is business-required, it becomes an M2 `/rank` contract change (new version) — not an M3 mapper invention.
- **Decision — symbol pattern** is `^[A-Z][A-Z0-9]{0,9}$` (same as frozen `/rank`), NOT the openapi draft's `^[A-Z]{3}$` — VN tickers include 4-letter and digit-bearing codes; a narrower pattern would silently reject universe members.

### 3.3 File layout (disjoint seams)

```
services/suggestion-api/
  pyproject.toml, README.md            ← M3-C only
  src/suggestion_api/
    main.py                            ← M3-C only (wires A+B routers, lifespan, middleware)
    auth/                              ← M3-A ONLY
      jwt_service.py     RS256 sign/verify, alg-allowlist ["RS256"], JWKS build
      password.py        PBKDF2-HMAC-SHA256 hash/verify (600k, salt)
      refresh_store.py   redis-py async: issue/rotate/revoke/family, compare_digest
      routers.py         /auth/login, /auth/refresh, /auth/jwks
    suggestions/                       ← M3-B ONLY
      market_data_repo.py  SQLAlchemy async read of market_data (parameterized)
      rank_client.py       httpx2 → POST /rank (timeouts, error mapping)
      mapper.py            /rank response → suggestion response (passthrough, drops screening)
      disclaimers.py       text + X-Disclaimer header + body object (compliance doc source)
      routers.py           GET /suggestions (authn dependency + scope check + query validation)
    middleware/
      rate_limit.py        ← M3-A ONLY (slowapi limiter, login/refresh policies)
      security_headers.py  ← M3-B ONLY (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
      error_handlers.py    ← M3-B ONLY (RFC 7807 handlers, 401/403/422/429/502 mapping)
  tests/
    test_auth_jwt.py, test_auth_refresh.py      ← M3-A
    test_suggestions.py, test_disclaimer.py     ← M3-B
    test_owasp_security.py (auth+api surface)   ← M3-A + M3-B (split by file)
```
**Boundary rules:** M3-A never imports from `suggestion_api.suggestions` and vice versa; neither touches `main.py`, root `requirements.txt`, root `pyproject.toml`, `shared/python`, or `docs/`. The only cross-slice interface is `auth` exposing a dependency (e.g. `require_scope("suggestions:read")`) that `suggestions/routers.py` consumes — that function's **signature is frozen in this record** so both slices build against it without touching each other's files. M3-C adds `PyJWT`, `redis`, `slowapi` to root `requirements.txt`, registers the new pytest path + `suggestion_api` in root `pyproject.toml`, finalizes the openapi, writes the README, and runs the e2e.

---

## 4. M3 — web-ui service

| Aspect | Decision |
|---|---|
| **Stack** | **Vite + TypeScript + vitest** (company precedent: colorlab already ships Vite+TS+vitest in this repo with `package-lock.json`; loremipsum ships Vite+vitest). **Reuse the Vite major already vendored/lockfile-verified in the repo** — safest supply-chain posture (npmjs.com is not reachable in-pod; the in-repo lockfile is the verified source). Port 3000 (`web_ui_port`). |
| **UI approach** | Vanilla TypeScript + Vite (no React/Vue/Angular). M3 scope is two views (suggestion list, suggestion detail) + login — a framework adds hundreds of lockfile deps for no parallelization or quality gain. Small modules: `api/client.ts` (fetch wrapper: Bearer attach, 401→refresh→retry-once, error mapping to ProblemDetails), `api/types.ts` (mirrors the §3.2 response contract), `views/` (login, list, detail), `components/` (disclaimer banner — rendered above the fold, non-dismissible, per compliance doc). |
| **Serving (TESTER-runnable)** | `npm run build` → static `dist/`, served by a **zero-dependency Node static server** (`server.mjs`, `node:http`) that pins security headers (CSP `default-src 'self'`; `X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy: no-referrer`; HSTS when `NODE_ENV=production`). **Rejected:** `vite preview` (no header control — fails the security-headers gate), express+helmet (2 extra deps for a static server; helmet is the noted upgrade path if a framework server ever lands). Dev: `vite dev` with proxy → `http://localhost:8003` (no CORS in dev; prod is same-origin behind a reverse proxy). |
| **Conventions** | vitest unit tests for `api/client.ts` (refresh/retry logic, error mapping) + a headers test asserting `server.mjs` emits the pinned headers; npm `audit` clean + snyk scan of the web-ui lockfile at the ship gate; no secrets in the client bundle (only non-secret `import.meta.env` config). |

### 4.1 File layout (disjoint — one slice owns the entire tree)

```
services/web-ui/
  package.json, package-lock.json, vite.config.ts, tsconfig.json, index.html
  src/
    main.ts, api/client.ts, api/types.ts, api/disclaimer.ts
    views/login.ts, views/list.ts, views/detail.ts
    components/disclaimer-banner.ts
    styles.css
  tests/ (vitest: client.test.ts, headers.test.ts, disclaimer.test.ts)
  server.mjs, README.md
```
**Boundary rules:** web-ui touches NO Python files and no shared/python. It builds against the §3.2 contract (documented here + openapi) and a committed fixture/mock response for development — it does not wait for suggestion-api code, only for the contract.

---

## 5. Security section (M3 — §7.2.1 gate mapping)

### 5.1 Attack surfaces → controls

| Surface | Risk | Concrete controls (stack-level) |
|---|---|---|
| `POST /auth/login` | Credential stuffing, brute force, timing | slowapi rate limit (e.g. 10/min per IP+username) → 429 `rate_limit.exceeded`; PBKDF2-HMAC-SHA256 600k iters (slows offline guessing); `hmac.compare_digest` (constant-time); generic error body (no user-exists oracle); structlog rate-limit + login-failure events. |
| `POST /auth/refresh` | Refresh-token theft/replay | Opaque 256-bit tokens (`secrets.token_urlsafe(32)`); Redis store keyed by token hash with TTL = refresh window; **rotation + family revocation on reuse → 409** (UC-SA-2 AC-03/04); `compare_digest` on lookup. |
| JWT layer | alg confusion, signature bypass, key disclosure | PyJWT with **explicit `algorithms=["RS256"]`** (rejects `none`/HS downgrade); `exp`+`iat` validation; `kid` matched against the served JWKS; RSA keys via env (`jwt_private_key`/`jwt_public_key`), never committed (gitleaks gate); key rotation = new `kid` in JWKS (backlog). |
| `GET /suggestions` | Broken authz, injection, DoS | Scope check `suggestions:read` → 403 `auth.scope_denied`; Pydantic strict query validation (`^[A-Z][A-Z0-9]{0,9}$`, symbols ≤ 100 — mirrors `/rank` cap, weights exact-keyset + sum 1.0); slowapi per-token limit (e.g. 60/min); all output is contract-shaped (no reflection of free-form input). |
| suggestion-api → analysis-engine `/rank` | Internal abuse, SSRF, timeout pileup | Outbound client targets a **fixed configured URL** (never user input → no SSRF); strict timeouts + small retry budget; failure → 502 ProblemDetails (no internal stack); internal docker network only; analysis-engine reachable in-pod for TESTER. |
| DB layer | SQL injection, data exposure | SQLAlchemy **parameterized queries only** (semgrep `no-raw-sql-f-string` is a fail-on-high gate rule); read-only usage; `market_data` is public market data (no PII) — nothing sensitive served. |
| Web UI | XSS (ranked content, reasoning strings), token exfiltration | Render API-derived strings via `textContent`/`createElement` only — **no `innerHTML` with API data** (reasoning strings are treated as untrusted); CSP `default-src 'self'` (no inline scripts — Vite emits hashed bundles); no third-party scripts/CDNs; access token in-memory + refresh token storage documented with the localStorage tradeoff (mitigation: CSP + no untrusted HTML; httpOnly-cookie refresh = hardening backlog); dev proxy only (no wildcard CORS). |
| Static server | Header-based attacks, clickjacking, MIME sniffing | `server.mjs` pins: CSP, `nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, HSTS (prod) — verified by the headers test (`performing-security-headers-audit` skill at QA). |
| Supply chain | Typosquat/dependency confusion, vulnerable deps | All new PyPI deps verified on this record's date (PyJWT 2.13.0, redis 8.1.0, slowapi 0.1.10 — healthy, active; httpx2 = Pydantic-stewarded, **not** a typosquat); web-ui reuses the in-repo vendored Vite lockfile; snyk scans both `requirements.txt` and the web-ui `package-lock.json` (fail CVSS ≥ 7.0); gitleaks gates any committed secret-like string. |

### 5.2 §7.2.1 gate checks for M3

- **OWASP API Top 10** → committed `tests/test_owasp_security.py` per service slice: API2 (JWT negative matrix: `alg:none`, HS256-downgrade, expired, bad kid → 401 `auth.token_*`), API3 (no secrets/internal paths in any response), API4 (symbol cap, weight validation → 422), API5/6 (unwanted methods 405, extra-body fields rejected), API7 (no stack traces — asserted across negative cases), API8 (malformed login/weights → clean 4xx), API10 (structlog coverage asserted).
- **XSS** (web surface) → vitest rendering tests (no `innerHTML` with API data) + CSP header assertion; QA uses the XSS/CSP skills on the shipped UI.
- **CORS** (API) → CORS allowlist locked to configured origins (dev proxy avoids CORS entirely; prod same-origin); a test asserts no wildcard and no credentials.
- **Security headers** (API + web) → header tests + QA `performing-security-headers-audit` on both `server.mjs` responses and suggestion-api responses.
- **SAST/SCA/secrets** → existing repo configs extended: semgrep scan path adds `services/suggestion-api/src`; snyk adds web-ui lockfile; gitleaks unchanged (fail-on-any). New M3 `SECURITY_GATE_RESULTS.md` per service, honest-evidence style (task-14/15 pattern).

---

## 6. Parallelization assessment (CTO duty 4 — feeds PM → CEO)

**Task seams (file-disjoint, ordering-free):**

| Task | Owns (files) | Depends on |
|---|---|---|
| **M3-A** suggestion-api auth slice | `suggestion_api/auth/*`, `middleware/rate_limit.py`, `tests/test_auth_*`, `tests/test_owasp_security.py` (auth half) | nothing (frozen `require_scope` signature from this record) |
| **M3-B** suggestion-api suggestions slice | `suggestion_api/suggestions/*`, `middleware/security_headers.py`, `middleware/error_handlers.py`, `tests/test_suggestions_*`, `tests/test_disclaimer.py`, `tests/test_owasp_security.py` (suggestions half) | nothing |
| **M3-D** web-ui | entire `services/web-ui/` tree | nothing (builds on §3.2 contract + fixtures) |
| **M3-C** assembly + e2e | `suggestion_api/main.py`, root `requirements.txt`/`pyproject.toml`, openapi finalize, READMEs, e2e | **A + B merged** (imports both packages) |
| **M3-E** TESTER e2e | (tester-owned) | **C + D merged** |

**Concurrent:** M3-A ∥ M3-B ∥ M3-D — three fully independent branches, zero shared files, zero shared state, no ordering. A and B interoperate only through the one frozen function signature; both may be reviewed in parallel by TECHLEAD. This is the shape designed in §3.3/§4.1 (not an after-the-fact assessment).

**Serial after:** M3-C (needs A+B), then M3-E (needs C+D). M3-C is inherently a merge task — do NOT slice it for parallelism.

**Instance math:** 3 concurrent DEV tracks shrinks the M3 build critical path to ~2 serial legs (parallel build → assembly → e2e) vs ~5 serial legs if built single-file. **Recommendation: 3 DEV instances justified for the M3 build window** (true disjointness, no merge contention), contingent on PR-cap headroom (#155, cap 5): A+B+D = 3 open PRs, leaving 2 slots for review/drain churn — PM verifies the live count when scheduling. If headroom forces 2 DEVs: run A∥B first, then D (web-ui is the most contract-stable and can also start as a 2nd slice). TESTER at 2 instances (already CEO-approved) is justified: one drains M1/M2 e2e, one covers M3-E.

**Architecture-health note (duty 7 lens):** M3's seams are small, single-purpose slices by design (auth vs suggestions vs UI). If the drain shows M1/M2 branches piling up, the fix pattern proven here — one frozen interface signature + disjoint modules + assembly task — is what PM should apply to M3-C's breakdown as well.

---

## 7. Open flags for CEO/PM (from grounding M3 in shipped M1/M2)

1. **`screening` dropped** from suggestion responses (§3.2) — deviates from the never-approved pre-drafted openapi; BA must not require it in M3 v1.0 use cases.
2. **`^[A-Z]{3}$` symbol pattern in the openapi draft is too narrow** — M3 uses the frozen `/rank` pattern `^[A-Z][A-Z0-9]{0,9}$`.
3. **Access-token TTL drift:** shared config default is 30 min; contract (UC-SA-2 AC-02) is 15 min — M3 pins 15 via env; a shared-config default fix is a backlog item.
4. **`httpx2` verified legitimate** (Pydantic-stewarded httpx continuation) — coexists with `httpx` for legacy M1/M2 code; consolidation is backlog, not M3.
5. M3-C finalizing the openapi should get TECHLEAD/QA review of the contract corrections (§3.2) before the ship gate.

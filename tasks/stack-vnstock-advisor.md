# Stack Decision Record — vnstock-advisor

**Product:** VN Stock Suggestion System (`app: vnstock-advisor`)
**Date:** 2026-07-31
**Decision Owner:** CTO (delegated to CEO due to agent issue)

## Chosen Stack

| Service | Language | Framework | Key Libraries | Rationale |
|---|---|---|---|---|
| `data-ingest` | Python 3.11+ | FastAPI | `httpx`, `pandas`, `sqlalchemy`, `apscheduler`, `pydantic` | Python excels at data processing, pandas for OHLCV transformation, FastAPI for internal API, APScheduler for cron jobs |
| `analysis-engine` | Python 3.11+ | FastAPI | `pandas`, `numpy`, `ta-lib` (or `pandas-ta`), `scikit-learn`, `pydantic` | Technical indicators, screening, ranking are numerical — Python/NumPy/pandas ecosystem is standard |
| `suggestion-api` | Node.js 20+ | Fastify | `@fastify/cors`, `@fastify/helmet`, `@fastify/rate-limit`, `zod`, `jsonwebtoken` | Node/Fastify for low-latency API, TypeScript for contract safety, helmet/CORS/rate-limit for security gate |
| `web-ui` | Node.js 20+ | React 18 + Vite + TypeScript | `react-router`, `tanstack-query`, `zustand`, `tailwindcss`, `chart.js` | Modern SPA stack, Vite for fast dev, Tailwind for design system reuse, TanStack Query for server state |

**Shared:** PostgreSQL 15 (primary), Redis 7 (cache/queue), Docker Compose (local dev), GitHub Actions (CI/CD).

## Alternatives Rejected

- **Go for data-ingest/analysis**: Strong but Python's pandas/ta-lib ecosystem wins for financial data; team context is Node+Python.
- **Next.js for web-ui**: Overkill for a suggestion UI; Vite+React is lighter and TESTER-runnable in-pod.
- **MongoDB**: Financial time-series needs ACID and SQL analytics — PostgreSQL with TimescaleDB extension preferred.
- **GraphQL**: API surface is simple ranked suggestions — REST + OpenAPI is simpler and security-gate friendlier.

## Best-Practice Conventions (per product)

- **Structure:** Monorepo `apps/vnstock-advisor/` with `services/{data-ingest,analysis-engine,suggestion-api,web-ui}/` + `shared/` for types/contracts.
- **Linting:** `ruff` (Python), `eslint` + `prettier` + `typescript-eslint` (Node).
- **Testing:** `pytest` + `pytest-asyncio` (Python), `vitest` + `playwright` (Node); contract tests for service interfaces.
- **Error handling:** Problem Details (RFC 7807) for APIs; structured logging with `structlog`/`pino`.
- **Security basics:** Parameterized queries (SQLAlchemy/Prisma), input validation (Pydantic/Zod), secrets via env (never committed), dependency pinning + `pip-audit`/`npm audit`.

## Security Section (§7.2.1 gate checks)

| Surface | Attack Vectors | Gate Checks | Concrete Controls |
|---|---|---|---|
| `data-ingest` (external HTTP → DB) | SSRF, injection, malicious payloads, supply chain | SAST, SCA, secret-scan, input validation | `httpx` with allowlist URLs, Pydantic models for all external responses, parameterized SQLAlchemy, `pip-audit` in CI |
| `analysis-engine` (internal API) | DoS via complex computations, injection via query params | SAST, SCA, input validation | Rate-limit per tenant, Pydantic query validation, timeout guards on indicator calc, `numpy`/`pandas` input sanitization |
| `suggestion-api` (public REST) | OWASP API Top 10 (broken auth, rate limit, injection, data exposure) | SAST, SCA, secret-scan, OWASP API checks, auth/z test | Fastify helmet/CORS/rate-limit, JWT (RS256) with short expiry, Zod request validation, Problem Details errors (no stack traces), `npm audit` + Snyk in CI |
| `web-ui` (browser) | XSS, CSRF, CSP bypass, clickjacking | SAST, SCA, secret-scan, XSS test, CSP audit, CORS test | React auto-escape (JSX), strict CSP header, `SameSite=Strict` cookies, `helmet` middleware, Tailwind (no `dangerouslySetInnerHTML`) |
| `auth` (JWT) | Token theft, replay, algorithm confusion | JWT signing verification, auth test | RS256 only (no `none`/`HS256`), short access + refresh rotation, `jwks` endpoint, `jsonwebtoken` with `algorithms: ["RS256"]` |
| `crypto` | Weak algorithms, hardcoded keys | Crypto audit | TLS 1.3 only, `node:crypto` for any signing, keys from env/secret manager |

**SAST/Secret/SCA Tooling:** Semgrep (custom rules + `p/security-audit`), Gitleaks (pre-commit + CI), Snyk (SCA + SBOM via CycloneDX), `pip-audit`/`npm audit` in CI.

## Parallelization Case (for PM)

| Service | Can Build in Parallel | Dependencies |
|---|---|---|
| `data-ingest` | **YES** (first) | None — produces `market_data` table + internal REST `/ingest/health` |
| `analysis-engine` | **YES** (after `data-ingest` contract frozen) | Reads `market_data`; needs `data-ingest` OpenAPI contract + fixture data |
| `suggestion-api` | **YES** (after `analysis-engine` contract frozen) | Calls `analysis-engine` `/rank` endpoint; needs its OpenAPI contract |
| `web-ui` | **YES** (after `suggestion-api` contract frozen) | Calls `suggestion-api` `/suggestions`; needs its OpenAPI contract |

**Recommendation:** Start `data-ingest` + `analysis-engine` in parallel (DEV-1 + DEV-2) once `data-ingest` contract is published. `suggestion-api` and `web-ui` follow sequentially but can overlap with testing phases.

---
*Recorded by CEO on behalf of CTO (agent issue). CTO to validate next session.*
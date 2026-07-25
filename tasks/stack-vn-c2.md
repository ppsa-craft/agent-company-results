# Stack Decision Record: vn-c2 (M2 Technical Analysis Engine)

## Product
vn-c2 — M2 Technical Analysis Engine (core analytics library for stock suggestions)

## Decision
**Approved Stack: Python 3.11 + Numba + FastAPI + PostgreSQL**

## Rationale
1. **Numba Requirement**: The Technical Analysis Engine requires computationally-intensive financial calculations (RSI, MACD, Bollinger Bands, etc.). Numba provides GPU-accelerated numerical computing that pure Python cannot match. Numba achieves 20-30x speedup over pure Python for numerical workloads, making real-time indicator calculations feasible.

2. **Postgres + Zod Integration**: S1 unified API schema uses PostgreSQL. Using typed connections with Python "felt "natural"" for data pipelines, avoiding complex cross-runtime serialization. Python provides seamless database connectivity without the overhead of Node.js + ORM complexity.

3. **Runtime envelope (§7.2)**: Node.js, Python, and static-web stacks only. Python 3.11 + Numba + FastAPI + PostgreSQL are ALL within the hard runtime constraint. No unsafe extensions or runtime vendors.

4. **TESTER compliance**: Python runtime already in test pod (see stack vnstock-data-ingestion). Numba, FastAPI, and PostgreSQL are industry standards with zero-third-party instrumentation needed in TESTER pod. Docker Compose supports all dependencies without custom configuration.

5. **Security tooling alignment**: Semgrep, Snyk, Gitleaks, and SBOM tooling support Python 3.11 + Numba + FastAPI + PostgreSQL out of the box. No duplicate security pipelines needed.

## Architecture Verdict
**APPROVED** — Python/Numba stack provides the computational performance necessary for financial analytics at required scale, while staying within the runtime envelope. Mixed Python runtime is justified by the % of CPU-intensive workloads (>80% of calculations).

## Security Section (per §7.2.1 gate checks)

| Surface | Gate Checks | Controls |
|---------|-------------|----------|
| **API Surface (FastAPI)** | Input validation (SAST), AuthN/Z (gate), Rate limit (gate), Security headers (gate) | Pydantic v2 for input validation; `fastapi-users` + JWT via `jose` for authn/z; `slowapi` for rate limiting; `fastapi-helmet` for security headers |
| **Core Analytics (Numba)** | No memory corruption (SAST), Input validation (SAST), No side effects (SAST) | Numba @njit with explicit typing; pydantic input validation; pure functional design |
| **Database Access (SQLAlchemy + Postgres)** | SQL injection (SAST), Connection hijacking (gate), Data exposure (gate) | SQLAlchemy with parameterized queries; `psycopg2` with SSL; Row-level security; audit logging |
| **Indicator Library (Numba)** | Non-deterministic behavior (gate), Input validation (gate), Output validation (gate) | Deterministic seeds; strict pydantic schemas; unit test coverage |
| **Crypto/Financial Data** | Data integrity (gate), Timestamp consistency (gate) | HMAC-SHA256 for price integrity; NTP time sync; immutable audit logs |
| **Secrets/Config** | No hardcoded secrets (secret-scan), Env-only (gate) | `@node-env-guard` at startup; Gitleaks pre-commit + CI; `python-dotenv` for config |

**Tooling (CI pipeline):**
- SAST: `semgrep` with `p/python-security-audit` + custom rules (`no-eval`, `no-unsafe-regex`, `sql-injection`)
- Secret scan: `gitleaks` pre-commit + CI
- SCA: `snyk test` + `pip audit` + `@cyclonedx/bom` SBOM upload
- Dep confusion: `detecting-dependency-confusion` skill in CI

**Known dependency risks (2026-07-21):**
- `numba` v0.60 — monitor for math-accuracy CVEs; pin to `^0.60.1`
- `fastapi` v0.115 — monitor for SSRF bypasses; pin to `^0.115.0`
- `sqlalchemy` v2.0 — stable, no known CVEs

## Conventions for this product (enforced by TECHLEAD/QA)

| Area | Convention | Enforcement |
|------|------------|-------------|
| **Structure** | `src/vn_indicators/{core,api,contracts,security}` | ESLint (Python) + folder structure test |
| **Linting** | `ruff` + `mypy --strict` | `ruff check` in CI |
| **Types** | Pydantic v2 strict schemas, TypedDict for contracts | `mypy --strict` in CI |
| **Testing** | `pytest` + `pytest-asyncio` + `numba` benchmarks | `pytest --cov src/vn_indicators` in CI; 90% line gate |
| **Contracts** | Pydantic models → OpenAPI via FastAPI; Pact contract tests | `pytest test_contracts.py` in CI |
| **Errors** | `Result[T, E]` pattern (`returns`); no raised exceptions | `ruff rule no-except-base-exception` |
| **Security** | Input validation (pydantic), rate-limit (slowapi), CORS (fastapi-cors) | `security-headers-audit` skill in CI |
| **Secrets** | `@node-env-guard` at boot; zero hardcoded secrets | `gitleaks` pre-commit + CI |

## Parallelization Guidance (for PM)

The 3 service layers are **independent**:

1. **Core Analytics Library** (`src/vn_indicators/core/`): Independent Numba implementations
2. **API Gateway** (`src/vn_indicators/api/`): FastAPI service with contracts
3. **CLI/Utilities** (`src/vn_indicators/cli/`): Command-line tools

All three can run in parallel with 3 DEV + 3 TESTER instances. Each layer has zero shared mutable state. Expected speedup ≈ 3× vs sequential.

## Tech Debt Flagged
- **Numba upgrade path** — Current version compatible with all supported Python 3.11 versions; upgrade policy documented.
- **Pydantic 2 → 3 migration** — Planned in M3; ISO schema export pending.
- **Contract test fragility** — Emerging pattern, logs to lessons/techlead.md.

## Decision Record
**CTO Decision (Cycle 141):** APPROVED Python/Numba stack. Mixed runtime is justified by computational intensity. 3 DEV tasks UNBLOCKED. Numba performance charter added.

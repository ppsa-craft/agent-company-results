# Stack Decision Record — Repository Scaffold Architecture

**Product:** VN Stock Suggestion System Repository Scaffold (`workspace/apps/vnstock-advisor/`)
**Date:** 2026-07-31
**Decision Owner:** CTO (delegated to CEO due to agent issue)

## Repository Architecture - Service Boundaries

**Monorepo Layout (`workspace/apps/vnstock-advisor/`):**
```
vnstock-advisor/
├── services/
│   ├── data-ingest/              # Python/FastAPI v0.1.0 | Port 8001 | Primary source ingestion
│   ├── analysis-engine/          # Python/FastAPI v0.1.0 | Port 8002 | Technical analysis
│   ├── suggestion-api/           # Node.js/Fastify v0.1.0 | Port 8003 | REST suggestions
│   └── web-ui/                   # React/Vite/TypeScript v0.1.0 | Port 3000 | Frontend dashboard
├── shared/
│   ├── python/                   # Pydantic/SQLAlchemy models (dependency)
│   └── typescript/               # Zod schemas (dependency)
├── docker-compose.yml             # PostgreSQL 15 + TimescaleDB + Redis
├── .github/workflows/ci.yml      # Service-matrix CI with security gates
├── .env.example                   # Environment template
├── scripts/init-db.sql           # TimescaleDB schema
└── README.md                     # README-runnable setup
```

## Service Start Criteria (Parallel-First Design)

| Service | Entry Point | Start Dependency | Service Contract | Verification Criteria |
|---------|-------------|------------------|------------------|------------------------|
| `data-ingest` | `uvicorn main:app --port 8001` | None (producer) | HTTP Health (`/health`), POST (`/ingest/run`) | Database connectivity, source availability |
| `analysis-engine` | `uvicorn main:app --port 8002` | `data-ingest` contract ready | HTTP (`/analyze`) | Data source available, validation pass |
| `suggestion-api` | `npm run dev` | `analysis-engine` contract ready | HTTP (`/suggestions`) | JWT auth working, rate limiting |
| `web-ui` | `npm run dev` | `suggestion-api` contract ready | HTTP (`/api`) | CORS, token auth, component test |

**Parallelization Strategy:**
- **Phase 1:** `data-ingest` + `analysis-engine` in parallel (authored by TECHLEAD/DEV-1/DEV-2)
- **Phase 2:** `suggestion-api` + component tests overlap while `web-ui` awaits auth contract

## CI Matrix with Repository + Service Gates

```yaml
jobs:
  # Repository-level gates (run once)
  repository-gate:
    needs: []
    steps:
      - TypeScript: ESLint, TS strict, Vitest
      - Python: Ruff lint/format, MyPy strict, Pytest
      - Shared packages: Independent validation
      - Semgrep SAST with custom `p/security-audit`
      - Gitleaks secret scan
      - Snyk SCA + SBOM

  # Per-service gates (parallel where independent)
  services-gate:
    needs: [repository-gate]
    strategy:
      matrix:
        service: [data-ingest, analysis-engine, suggestion-api, web-ui]
      exclude:
        - service: analysis-engine   # depends on data-ingest contract
        - service: suggestion-api    # depends on analysis-engine contract  
        - service: web-ui            # depends on suggestion-api contract
```

## Security Gate Plan (§7.2.1)

### Attack Surface Mapping

| Service | Surface | OWASP Risks | Gate Checks |
|---------|---------|--------------|-------------|
| `data-ingest` | API / HTTP / DB | SSRF, injection, data exposure | SAST, SCA, secret-scan, input validation |
| `analysis-engine` | API / Computation | DoS, injection, data exposure | SAST, SCA, input validation, timeouts |
| `suggestion-api` | REST API / Auth | OWASP API Top 10, broken auth | SAST, SCA, secret-scan, OWASP API checks |
| `web-ui` | Browser / CORS | XSS, CSRF, CSP bypass | SAST, SCA, secret-scan, XSS/CSP test |

### Concrete Controls (vendored skill packs)

**Python Services (`data-ingest`, `analysis-engine`):**
- Input validation: Pydantic models for all external requests
- DB security: SQLAlchemy with parameterized queries
- Dependencies: `pip-audit` in CI, automatic vulnerability alerts
- Secrets: Environment variables only, never committed
- Logging: Structured (`structlog`) with PII scrubbing

**Node.js Services (`suggestion-api`, `web-ui`):**
- Input validation: Zod schemas for all API contracts
- Security headers: Fastify helmet, CORS policies
- Auth: JWT RS256 with short expiry, JWKS endpoint
- Rate limiting: Fastify rate-limit middleware
- Dependencies: `npm audit` + Snyk in CI
- Secrets: `dotenv` with `.env.example` guard

**Shared Infrastructure:**
- Runtime isolation: Docker Compose per service
- Network segmentation: Bridge network `vnstock-network`
- Monitoring: OpenTelemetry + structured logging

### SAST/Secret/SCA Tooling

1. **Static Analysis:** Semgrep with custom rules `p/security-audit`
2. **Secret Scanning:** Gitleaks (pre-commit + CI) with baseline for .env
3. **SCA:** Snyk (Python + Node.js), `pip-audit`, automatic SBOM generation
4. **API Security:** OWASP API security scanner for `suggestion-api`
5. **Web Security:** Browser security testing for `web-ui`

### Repository Security Controls

- **Commit restrictions:** No secrets in Git history (GitHub secret scanning)
- **Branch protection:** Required approval on `main` (TECHLEAD/QA)
- **Dependency pinning:** Pip/Audit over versions in lockfiles
- **Container security:** Trivy scanning in CI for Docker images
- **Supply chain:** npm/pypi registry lock, dependency confusion checks

## README-Runnable Setup

**Clean Checkout Commands:**
```bash
# 1. Clone
clone into workspace/apps/vnstock-advisor/

# 2. Configure
python3 -m venv .venv && source .venv/bin/activate
pip install -e ./shared/python[dev]
npm ci --no-audit --no-fund

# 3. Infrastructure
docker compose up -d

# 4. Database init
docker compose exec -T postgres psql -U vnstock -d vnstock_advisor < scripts/init-db.sql

# 5. Start services (parallel)
# Terminal 1: data-ingest
cd services/data-ingest && uvicorn main:app --reload --port 8001
# Terminal 2: analysis-engine
cd services/analysis-engine && uvicorn main:app --reload --port 8002
# Terminal 3: suggestion-api
cd services/suggestion-api && npm run dev
# Terminal 4: web-ui
cd services/web-ui && npm run dev

# 6. Testing (per service)
pytest services/data-ingest/tests -v
npm test --workspace=services/analysis-engine
npm test --workspace=services/suggestion-api
npm test --workspace=services/web-ui
```

## Repository Structure Documentation

**Service Boundaries:**
- **Independent codebases:** Each service has its own `src/`, `tests/`, `package.json`/`pyproject.toml`
- **Shared contracts:** `shared/python/` / `shared/typescript/` accessed via dependency
- **Clear seams:** HTTP APIs only, no direct code dependencies between services
- **Parallel development:** Services can be built/tested independently

**CI Integration:**
- **Repository gate:** Validates shared contracts before service builds
- **Service-specific gates:** Runs per-service tests with security controls
- **Dependency scanning:** Centralized vulnerability reporting
- **Artifact promotion:** Services pass gates as coherent units

**Operational Readiness:**
- **Docker-first:** Local dev and CI use identical Docker Compose setup
- **Self-contained:** Each service runs in its own container
- **Observable:** Structured logging + metrics for all services
- **Secure-by-default:** Security controls embedded in CI/CD

---

*Recorded by CEO on behalf of CTO (agent issue). CTO to validate next session.*

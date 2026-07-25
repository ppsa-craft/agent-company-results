# Stack Decision Record: vn-stock-suggestion (M1 Data Ingestion Service)

**Product:** vn-stock-suggestion (Flagship)
**Milestone:** M1 — Data Ingestion Service
**Date:** 2026-07-19
**Author:** CTO

---

## Chosen Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API Gateway / Web** | **Node.js 20 + Fastify** | Low-latency HTTP, TypeScript native, low overhead, fits runtime envelope |
| **Data Processing / Ingestion Workers** | **Python 3.11 + FastAPI (internal)** | Pandas/NumPy for VN stock data normalization, yfinance/vnstock wrappers, async io for rate-limited APIs |
| **Storage** | **SQLite (file) + Redis (cache/rate-limit)** | Zero-config, embeddable, TESTER-friendly; Redis for API rate-limit token buckets |
| **Message Bus (internal)** | **Redis Streams** | Lightweight, in-envelope, backpressure for ingestion → storage pipeline |
| **Orchestration / CLI** | **Node.js (Commander.js)** | Thin CLI wrapper around internal HTTP API |
| **Web Monitoring UI** | **Vite + Vanilla TypeScript + Preact** | Tiny (<10KB), static deploy, no framework tax |
| **Shared Types / Contracts** | **TypeScript + Zod schemas (shared package)** | Single source of truth for API contracts, validated at runtime |
| **Testing** | **Vitest (Node) + pytest (Python) + Playwright (E2E)** | Fast, parallel, in-envelope |
| **Lint/Format** | **Biome (JS/TS) + Ruff (Python)** | Fast, unified config |
| **Container/Run** | **Docker Compose (dev) / single binary (prod via pkg/zipapp)** | TESTER can `docker compose up` in clean checkout |

---

## Architecture Seam Boundaries (for MAX parallelism)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL CLIENTS                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │  Web Monitor │    │   CLI Tool   │    │  External API│           │
│  │  (Preact)    │    │  (Commander) │    │  Consumers   │           │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘           │
└─────────┼────────────────────┼────────────────────┼─────────────────┘
          │                  │                    │
          ▼                  ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (Fastify + TS)                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  REST API: GET /stocks/:symbol, GET /stocks/:symbol/history  │   │
│  │  WS: /ws/realtime/:symbol                                     │   │
│  │  Auth: API-key (simple), Rate-limit: Redis token bucket      │   │
│  │  Contracts: Zod schemas (shared package)                     │   │
│  └────────────────────────────┬─────────────────────────────────┘   │
└───────────────────────────────┼─────────────────────────────────────┘
                                │ HTTP/JSON + WS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  INTERNAL MESSAGE BUS (Redis Streams)               │
│  Stream: stock.ingest.raw   →  Consumer Group: ingest-workers       │
│  Stream: stock.ingest.norm  →  Consumer Group: storage-workers      │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│ INGEST WORKER │      │ INGEST WORKER │      │ INGEST WORKER │
│ (Python proc) │      │ (Python proc) │  ... │ (Python proc) │
│ - yfinance    │      │ - vnstock     │      │ - AlphaVantage│
│ - AlphaVantage│      │ - VNIndex API │      │ - Mock (test) │
│ - Rate limit  │      │ - Rate limit  │      │ - Rate limit  │
└───────┬───────┘      └───────┬───────┘      └───────┬───────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                    ┌───────────────────────┐
                    │ NORMALIZER (Python)   │
                    │ - Pandas normalize    │
                    │ - Schema validate     │
                    │ - Emit to norm stream │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ STORAGE WORKER (Python)│
                    │ - SQLite upsert       │
                    │ - Redis cache warm    │
                    │ - Emit events         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   SQLite (file)       │
                    │   + Redis (cache)     │
                    └───────────────────────┘
```

---

## Service Boundaries (Independent DEV/TESTER Task Boundaries)

| Service / Module | Owner | Independent Tasks | Shared Contract |
|------------------|-------|-------------------|-----------------|
| **api-gateway** (Fastify) | DEV-1 | REST endpoints, WS, auth, rate-limit, OpenAPI spec | `packages/contracts` (Zod) |
| **web-monitor** (Preact) | DEV-2 | Dashboard, real-time charts, historical views, settings | `packages/contracts` + API |
| **cli** (Commander) | DEV-3 | `vnstock fetch`, `vnstock serve`, `vnstock history` | `packages/contracts` + API |
| **ingest-workers** (Python) | DEV-4 | yfinance worker, vnstock worker, AlphaVantage worker, mock worker | `packages/contracts` (Python port) + Redis Streams |
| **normalizer** (Python) | DEV-5 | Pandas normalization, schema validation, anomaly detection | `packages/contracts` (Python port) |
| **storage-worker** (Python) | DEV-6 | SQLite upserts, Redis cache, migration runner | `packages/contracts` (Python port) |
| **shared-contracts** (TS+Python) | TECHLEAD | Zod schemas, Python pydantic models, codegen script | — |
| **core-types** (TS) | TECHLEAD | Domain types, error codes, constants | — |

**Each row above = 1 independent DEV task + 1 independent TESTER task + 1 BA task (requirements). Zero shared mutable state between rows. Communication ONLY via Redis Streams + HTTP/WS contracts.**

---

## Rejected Alternatives

| Alternative | Why Rejected |
|-------------|--------------|
| **Pure Node (no Python)** | VN stock data libraries (vnstock, vnquant) are Python-first; pandas normalization is 10x faster in Python |
| **Pure Python (FastAPI only)** | Web UI + CLI + API gateway better in Node/TS; TESTER tooling (Playwright, Vitest) is JS-native |
| **PostgreSQL** | Outside runtime envelope (no PG in TESTER pod); SQLite + Redis is zero-config for TESTER |
| **RabbitMQ / Kafka** | Outside runtime envelope; Redis Streams is in-envelope, supports consumer groups |
| **Next.js / React** | Too heavy for static monitoring UI; Preact + Vite < 10KB gzipped |
| **Shared DB (no message bus)** | Couples ingest workers to storage — blocks parallel DEV work |

---

## Best-Practice Conventions (Enforced by TECHLEAD Review)

| Area | Convention |
|------|------------|
| **Project Structure** | Monorepo (pnpm workspaces): `apps/api-gateway`, `apps/web-monitor`, `apps/cli`, `workers/ingest-*`, `workers/normalizer`, `workers/storage`, `packages/contracts`, `packages/core-types` |
| **TypeScript** | Strict mode, `exactOptionalPropertyTypes`, no `any`, Zod for all boundaries |
| **Python** | `pyproject.toml`, `ruff` + `mypy --strict`, `pydantic` for contracts, `pytest-asyncio` |
| **Contracts** | Single source: `packages/contracts/schemas.ts` → codegen → `packages/contracts/python/schemas.py` via `zod-to-py` script |
| **Error Handling** | `Result<T, E>` pattern (TS: `neverthrow`, Python: `returns`); no thrown exceptions across service boundaries |
| **Config** | `config.ts` (zod-validated) + `config.py` (pydantic-settings); single `.env` file |
| **Testing** | Unit: Vitest (TS) / pytest (Py) >90% coverage on pure logic; Contract: Vitest + Pact-style against shared schemas; E2E: Playwright (web) + Vitest (API) |
| **Security** | Helmet (Fastify), CSP, rate-limit (Redis), input validation (Zod), no eval, secrets in `.env` only |
| **Observability** | Pino (TS) + structlog (Py) → stdout JSON; `/health` + `/metrics` (Prometheus text) on all services |
| **CI/CD** | GitHub Actions: lint → typecheck → unit → contract → e2e → build images; Docker Compose for integration test |

---

## Parallelization Plan (for PM)

| Parallel Track | DEV Tasks | TESTER Tasks | BA Tasks | Dependencies |
|----------------|-----------|--------------|----------|--------------|
| **Track A: Contracts** | 1 (shared-contracts) | 1 (contract tests) | 1 (contract reqs) | **None — START FIRST** |
| **Track B: API Gateway** | 1 (api-gateway) | 1 (API contract + E2E) | 1 (API reqs) | Track A |
| **Track C: Web Monitor** | 1 (web-monitor) | 1 (Playwright E2E) | 1 (UI reqs) | Track A |
| **Track D: CLI** | 1 (cli) | 1 (CLI contract) | 1 (CLI reqs) | Track A |
| **Track E: Ingest Workers** | 4 (yfinance, vnstock, alphavantage, mock) | 4 (unit + contract each) | 1 (ingest reqs) | Track A |
| **Track F: Normalizer** | 1 (normalizer) | 1 (unit + contract) | — | Track A |
| **Track G: Storage** | 1 (storage-worker) | 1 (unit + contract) | — | Track A, E, F |
| **Track H: Integration** | 1 (docker-compose, wiring) | 1 (full E2E) | — | All above |

**Total parallel DEV tracks: 8** (can run 8 DEVs simultaneously after Track A).
**TESTER parallelism: 10+** independent test suites.
**BA parallelism: 4** independent requirement tracks.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Python/Node version drift in TESTER pod | Medium | High | Pin versions in `.tool-versions` / `package.json` + `pyproject.toml`; CI pins |
| Redis Streams backpressure under burst | Low | Medium | Configure `MAXLEN ~` + consumer group `BLOCK 5000`; backpressure to API gateway 503 |
| VN data source API changes | High | Medium | Adapter pattern per source; mock worker for tests; contract tests catch breakage |
| SQLite write contention (multi-worker) | Medium | Medium | Single storage worker (serializer); WAL mode; batch inserts |
| TESTER pod lacks Redis | Low | Critical | Docker Compose in repo; CI spins Redis; document in README |

---

## Deliverable

**Output ADR:** `workspace/architecture/vnstock-data-ingestion-stack.md` (to be written by CTO task)
**Stack Decision Record:** This file (`tasks/stack-vnstock-data-ingestion.md`)
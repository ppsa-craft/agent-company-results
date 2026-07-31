# Task: vnstock-advisor-1-repo-scaffold

**Role:** DEV
**Product:** vnstock-advisor
**DoD Tier:** 2 (Feature: repo scaffold + CI foundation)
**Status:** claimed:DEV-1

---

## Goal

Create the monorepo structure for `vnstock-advisor` in `workspace/apps/vnstock-advisor/` with Docker Compose, shared config, and CI/CD foundation so all four services can be developed in parallel.

---

## Acceptance Criteria (traceable to use cases)

- [ ] Monorepo directory structure exists: `apps/vnstock-advisor/services/{data-ingest,analysis-engine,suggestion-api,web-ui}/` + `shared/`
- [ ] Docker Compose file starts PostgreSQL 15, Redis 7, and provides service networks
- [ ] Shared TypeScript/Python config packages publishable via `npm`/`pip` (or local path imports)
- [ ] GitHub Actions CI workflow runs lint, type-check, and test for all services
- [ ] `README.md` with how-to-run instructions works verbatim in clean checkout
- [ ] All services share common `.env.example` with required variables documented

---

## Implementation Plan (for DEV)

**Architecture seam:** This task cuts along the *repo foundation* seam — it creates the shared infrastructure that all service tasks depend on but touches no service business logic. No other task modifies these files.

**Technical approach:**
1. Create `workspace/apps/vnstock-advisor/` with monorepo structure per stack decision
2. Write `docker-compose.yml` with PostgreSQL 15 (with TimescaleDB extension), Redis 7, and service networks
3. Create `shared/` package with:
   - `shared/typescript/` — Zod schemas for API contracts, TypeScript config
   - `shared/python/` — Pydantic models for `market_data` table, Python packaging config
4. Create root `package.json` with workspaces + `pyproject.toml` for Python workspace
5. Write GitHub Actions `.github/workflows/ci.yml` with matrix jobs for each service (ruff/pytest for Python, eslint/tsc/vitest for Node)
6. Create `.env.example` with all required vars: `DATABASE_URL`, `REDIS_URL`, `JWT_PRIVATE_KEY`, `JWT_PUBLIC_KEY`, data source API keys
7. Write root `README.md` with `docker compose up -d` and per-service dev commands

**Ordered subtask checklist:**
- [ ] Create directory structure
- [ ] Write docker-compose.yml
- [ ] Create shared/typescript package
- [ ] Create shared/python package
- [ ] Write root package.json + pyproject.toml
- [ ] Write GitHub Actions CI workflow
- [ ] Write .env.example
- [ ] Write README.md with verified run steps

---

## Test Plan (for TESTER)

**Scenario 1: Clean checkout + docker compose up**
- Steps: `git clone <repo>`, `cd workspace/apps/vnstock-advisor`, `cp .env.example .env`, `docker compose up -d`
- Expected: PostgreSQL and Redis containers healthy, no port conflicts

**Scenario 2: CI workflow runs locally via `act` or pushed branch**
- Steps: Push a test branch, watch GitHub Actions
- Expected: All matrix jobs pass (lint, type-check, test — tests may be empty but commands run)

**Scenario 3: Shared packages importable**
- Steps: In `data-ingest` service, `from shared.python.models import MarketData`; in `suggestion-api`, `import { MarketDataSchema } from '@vnstock/shared-typescript'`
- Expected: No import errors, type-check passes

**Edge case: Missing .env values**
- Steps: Run without `.env` or with partial values
- Expected: Clear error messages naming missing vars, not cryptic crashes

---

## Dependencies

- None (first task, foundation for all others)
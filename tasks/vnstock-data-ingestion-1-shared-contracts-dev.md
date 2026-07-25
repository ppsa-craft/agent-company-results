## Task: vnstock-data-ingestion-1-shared-contracts-dev

**Product:** vnstock-data-ingestion (FLAGSHIP M1)
**Type:** implementation
**Assignee:** dev-1
**Status:** ready
**DoD Tier:** 2 (Feature)
**Architecture Seam:** Track A — shared-contracts (Zod schemas + Python pydantic models, codegen script)

### Goal
Implement the shared contracts package (`packages/contracts`) as the single source of truth for all API contracts between services. This is the **critical path foundation** — all other tracks depend on this.

### Acceptance Criteria (traceable to use cases)
- [ ] `packages/contracts/schemas.ts` defines Zod schemas for: StockQuote, HistoricalPrice, IngestJob, APIError, HealthResponse, WSMessage
- [ ] `packages/contracts/python/schemas.py` generated via `zod-to-py` script (checked in, not generated at build time)
- [ ] `packages/contracts/codegen.ts` script reads Zod schemas and emits Python pydantic models
- [ ] TypeScript types exported from `packages/contracts/index.ts` (consumer imports: `import { StockQuote } from '@vnstock/contracts'`)
- [ ] Python package installable via `pip install -e packages/contracts/python`
- [ ] Unit tests verify TS↔Py schema parity (same field names, types, required/optional)
- [ ] No circular dependencies; contracts package has zero runtime dependencies except zod

### Implementation Plan (for DEV)
**Technical Approach:** Monorepo (pnpm workspaces). Create `packages/contracts` with:
1. `schemas.ts` — Zod schemas for all domain types (StockQuote, HistoricalPrice, IngestJob, APIError, HealthResponse, WSMessage)
2. `codegen.ts` — Script using `zod-to-ts` / custom emitter to generate Python pydantic models
3. `package.json` — exports TS types, Python package config
4. `pyproject.toml` — Python package config with pydantic dependency
5. Run codegen, commit generated `python/schemas.py`
6. Unit tests: Vitest for TS schema validation, pytest for Python model validation, parity test comparing field sets

**Files/Modules Created:**
- `packages/contracts/schemas.ts`
- `packages/contracts/codegen.ts`
- `packages/contracts/index.ts`
- `packages/contracts/package.json`
- `packages/contracts/pyproject.toml`
- `packages/contracts/python/schemas.py` (generated, committed)
- `packages/contracts/tests/parity.test.ts`
- `packages/contracts/tests/python/test_parity.py`

**Ordered Subtask Checklist:**
1. [ ] Scaffold `packages/contracts` with pnpm workspace config
2. [ ] Define Zod schemas in `schemas.ts` for all 6 domain types
3. [ ] Write `codegen.ts` to emit Python pydantic models
4. [ ] Run codegen, verify `python/schemas.py` compiles
5. [ ] Export TS types from `index.ts`
6. [ ] Write parity unit tests (TS + Python)
7. [ ] Verify `pnpm -F @vnstock/contracts build` and `pip install -e packages/contracts/python` work

### Test Plan (for TESTER)
**Scenario 1: TS Schema Validation**
- Import `StockQuote` schema, validate valid payload → passes
- Validate payload missing required field → fails with ZodError
- Validate payload with wrong type → fails with ZodError

**Scenario 2: Python Model Validation**
- Import `StockQuote` from `vnstock.contracts`, instantiate valid → passes
- Instantiate missing required field → raises ValidationError
- Instantiate wrong type → raises ValidationError

**Scenario 3: TS↔Py Parity**
- Extract field names + types from TS schema and Python model
- Assert sets are equal (no extra/missing fields on either side)

**Scenario 4: Package Install**
- `pnpm install` in monorepo root succeeds
- `pnpm -F @vnstock/contracts build` succeeds
- `pip install -e packages/contracts/python` succeeds

### DoD Tier 2 Checklist
- [ ] Implementation complete per acceptance criteria
- [ ] Unit tests >90% coverage on contracts package
- [ ] Parity tests pass (TS ↔ Python)
- [ ] README updated with usage examples for TS and Python consumers
- [ ] Analytics plan updated (contract version tracking)
- [ ] No TECHLEAD review blockers
# Task: T-43-1 VnDirect REST API Client

## Goal
Implement VnDirect REST API client for VNIndex, VN30, HNX, UPCOM indices + top 100 liquidity stocks OHLCV data.

## Status
**IN_PROGRESS** — Cycle 43 interrupted, resuming Cycle 45

## DoD (Definition of Done) — Tier 1 (Service)
- [ ] VnDirect API client with typed TypeScript interfaces
- [ ] Fetch VNIndex, VN30, HNX, UPCOM index OHLCV
- [ ] Fetch top 100 liquidity stocks OHLCV
- [ ] Retry/backoff logic for transient failures
- [ ] Rate limiting compliance (respect VnDirect limits)
- [ ] Unit tests (Vitest) — coverage ≥ 80%
- [ ] Integration test with mocked API responses
- [ ] All DoD items traceable to use cases in BA docs

## Work Remaining
1. **API client core** — `src/clients/vndirect-client.ts` with fetch wrapper, error handling
2. **Index endpoints** — Methods for VNIndex, VN30, HNX, UPCOM daily OHLCV
3. **Stock endpoints** — Methods for top 100 liquidity stocks OHLCV
4. **Retry/backoff** — Exponential backoff with jitter, max retries config
5. **Rate limiting** — Token bucket or simple delay between requests
6. **Type definitions** — TypeScript interfaces for all response shapes
7. **Unit tests** — Mock fetch, test success/error/retry paths
8. **Integration test** — Mock server (msw) to verify contract

## Workspace State
- `workspace/apps/vn-stock-suggestion/` — **DOES NOT EXIST YET** (create on branch)
- Will need: package.json, tsconfig.json, vitest.config.ts, src/, tests/

## Assignment
**Assignee:** DEV-1 (only available DEV instance)
**Branch:** `task/T-43-1-vndirect-client-dev-1`
**Skills required:** `incremental-implementation`, `test-driven-development`, `spec-driven-development`

## Assignment Instructions
1. Check out branch `task/T-43-1-vndirect-client-dev-1` from main
2. Initialize `workspace/apps/vn-stock-suggestion/` with Node/TypeScript project
3. Implement VnDirect client following TDD (tests first)
4. Target ≥80% test coverage
5. Run `npm test` before completing
6. Push branch and report status

## DoD Tier
**Tier 1 — Service** (reusable library + tests + contracts)

## Traceability
Trace each DoD item to use cases in BA docs (to be created by BA if needed).

## Report Back To
PM — report: what was done, status (done/in-progress/blocked), blockers.
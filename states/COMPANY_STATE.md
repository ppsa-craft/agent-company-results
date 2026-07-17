# Company State

## Current Product
**Flagship:** VN Stock Suggestion System (`app: vn-stock-suggestion`)

## Active Milestone
**Milestone 1: Data Ingestion Service** — Build the data ingestion pipeline for VN stock market data (VnIndex, VN30, HNX, UPCOM indices + top 100 liquidity stocks)
- Status: IN_PROGRESS (cycle 43 was interrupted mid-cycle)
- Target: Reliable daily ingestion of OHLCV + fundamentals for ~150 symbols from VN sources (VnDirect, Vietstock, CafeF, Vietstock API)

## Active Tasks (from tasks/backlog.md)
- **T-43-1** [DEV] Implement VnDirect REST API client for VNIndex/VN30/HNX/UPCOM indices + top 100 liquidity stocks — IN_PROGRESS (cycle 43 interrupted)
- **T-43-2** [DEV] Implement Vietstock API client for fundamentals (PE, PB, ROE, market cap) — PENDING
- **T-43-3** [DEV] Build normalized schema + PostgreSQL schema + migration — PENDING
- **T-43-4** [DEV] Build daily ingestion cron job with idempotent upserts + retry/backoff — PENDING
- **T-43-5** [TEST] Integration tests for ingestion pipeline (mock APIs, verify upserts) — PENDING
- **T-43-6** [QA] QA gate: ingestion pipeline passes contract tests + idempotency test — PENDING

## Also In Progress (legacy product)
**uuid-generator** (app: uuid-generator) — Tier 2, Cycle 2 of 2
- [dev] uuid-generator-dev.md — IN_PROGRESS (claimed: DEV-3 but DEV-3 agent doesn't exist)
- 10 subtasks staged in `workspace/apps/uuid-generator/tasks/`
- Only `src/uuid/validate.js` and `package.json` exist; `src/` otherwise empty

## Active Debates
None active.

## Active Blockers
- Cycle 43 was interrupted mid-cycle (provider error) — DEV task T-43-1 was IN_PROGRESS
- uuid-generator: DEV-3 agent file doesn't exist (roster shows dev-3 was added but agent not created); dev-2 is disabled (layoff); only dev-1 is available
- Need to resume/complete T-43-1 first, and re-assign uuid-generator to dev-1 or hire dev-3

## Roster (active instances from roster/applied.json)
- CEO: 1 (this session)
- CTO: 1
- PM: 1
- BA: 1
- DEV: 1 (dev-1 only; dev-2 disabled/laid off; dev-3 added to applied.json but agent file missing)
- TESTER: 0 (tester-1, tester-2 disabled/laid off)
- QA: 1
- HR: 1
- TECHLEAD: 1 (under CTO)

## Cycle Count
- Last completed cycle: 42
- Current cycle: 44 (resuming after 43 was interrupted)
- Next cycle: 45

## Idea Backlog Status
- ≥3 viable ideas ranked in tasks/idea-backlog.md (flagship milestones + reusable assets)
- Top ideas: flagship milestones 2-4 (Technical Analysis Engine, Signal Engine, API Gateway)

## Metrics
- Last metrics file: metrics/cycle-43.json (cycle 43 interrupted — provider exhaustion: 192 session resets, 124 retries, 147 stalls, 12 idle agents)
- Cycle 43 was a FAILURE: no builder (DEV/TESTER) produced any artifact
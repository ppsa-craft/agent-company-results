# Task: tech-analysis-140-01-m2a-core-indicators

**Task ID**: T-140-01
**Title**: M2A Core Indicators — SMA, EMA, RSI, MACD, Bollinger
**Role**: DEV
**Status**: READY
**Assigned Agent**: dev-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature (use cases + tests + docs/README update + analytics update)

## File Ownership (Architecture Seam: M2A Core Indicators Service)
- `workspace/apps/tech-analysis/services/m2a-core-indicators/**`
- `workspace/apps/tech-analysis/tests/unit/m2a-core-indicators/**`
- `workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md` (shared with BA)
- `workspace/apps/tech-analysis/docs/architecture/m2a-contracts.md` (shared with TECHLEAD)
- `workspace/apps/tech-analysis/security/m2a-gate-report.md` (shared with QA)

## Goal
Implement the M2A Core Indicators Service: SMA, EMA, RSI, MACD, Bollinger Bands as a reusable technical analysis service. This is the core indicator library that M2A and future services will consume.

## Acceptance Criteria (traceable to M2A-UC Specs)
- UC-M2A-01: SMA calculator — correct values for period N, handles NaN for insufficient data
- UC-M2A-02: EMA calculator — correct EMA with configurable smoothing factor, handles warm-up period
- UC-M2A-03: RSI calculator — correct RSI(14) with Wilder smoothing, handles 0/100 bounds
- UC-M2A-04: MACD calculator — MACD line, signal line, histogram with configurable fast/slow/signal periods
- UC-M2A-05: Bollinger Bands — middle band (SMA), upper/lower bands at k standard deviations
- UC-M2A-06: All indicators handle NaN/NaN propagation correctly for insufficient lookback
- UC-M2A-06: All indicators return consistent data structure: `{ timestamp, value, metadata }`
- UC-M2A-07: Service exposes gRPC/HTTP endpoint for indicator computation
- UC-M2A-08: Unit test coverage ≥ 90% per indicator

## Implementation Plan (for DEV-1)
**Architecture Seam**: M2A Core Indicators Service — `workspace/apps/tech-analysis/services/m2a-core-indicators/`

**Technical Approach** (informed by CTO's stack record `tasks/stack-tech-analysis.md`):
- Language: TypeScript/Node.js (per stack decision)
- Framework: Fastify + gRPC (per stack decision)
- Indicators implemented in `services/m2a-core-indicators/src/indicators/` as pure functions
- gRPC service definition in `services/m2a-core-indicators/proto/indicators.proto`
- HTTP REST gateway via `@grpc/grpc-js` + `@grpc/proto-loader`
- Unit tests in `tests/unit/m2a-core-indicators/` using Vitest
- Integration tests in `tests/integration/m2a-core-indicators/`
- Shared types in `packages/ta-core-types/` (extracted later in T-140-26)

**Ordered Subtask Checklist**:
1. Scaffold service scaffold: `services/m2a-core-indicators/` with package.json, tsconfig, proto, src structure
2. Define protobuf schema: `proto/indicators.proto` with ComputeIndicatorsRequest/Response
3. Implement SMA indicator: `src/indicators/sma.ts` — pure function, handles warm-up NaN
4. Implement EMA indicator: `src/indicators/ema.ts` — Wilder smoothing, configurable alpha
5. Implement RSI indicator: `src/indicators/rsi.ts` — Wilder RSI, 0-100 bounds, NaN warm-up
6. Implement MACD indicator: `src/indicators/macd.ts` — fast/slow/signal periods, histogram
7. Implement Bollinger Bands: `src/indicators/bollinger.ts` — SMA middle, k*stddev bands
7. Create indicator registry: `src/indicators/registry.ts` — map indicator name → function
8. Implement gRPC server: `src/server.ts` — Fastify + gRPC, register indicator methods
9. Implement HTTP gateway: `src/gateway.ts` — REST endpoints for each indicator
10. Add input validation: Zod schemas for request validation
11. Add unit tests: `tests/unit/m2a-core-indicators/` — ≥90% coverage per indicator
12. Add integration tests: `tests/integration/m2a-core-indicators/` — gRPC + HTTP happy paths
13. Add README.md with run instructions, API examples
14. Update analytics plan reference in `workspace/apps/tech-analysis/docs/analytics/plan.md`

## Test Plan (for TESTER - T-140-02)
**Test Scenarios per Acceptance Criterion**:
- UC-M2A-01 SMA: 
  - Happy: 20-period SMA on 50 data points → correct values from index 19 onward
  - Edge: 5 data points, period 10 → all NaN
  - Edge: Empty array → empty result
  - Edge: NaN in input → NaN propagates correctly
- UC-M2A-02 EMA:
  - Happy: EMA(12) on 50 points → matches reference implementation from index 11
  - Edge: Period 1 → equals input
  - Edge: Alpha=1 → equals input
- UC-M2A-03 RSI:
  - Happy: RSI(14) on trending data → 0-100 bounds respected
  - Edge: All gains → 100, all losses → 0
  - Edge: Flat data → 50 (or NaN for first 14)
- UC-M2A-04 MACD:
  - Happy: MACD(12,26,9) → line, signal, histogram all present
  - Edge: Insufficient data → all NaN
- UC-M2A-05 Bollinger:
  - Happy: BB(20,2) → middle=SMA(20), upper/lower = middle ± 2σ
  - Edge: Period > data length → all NaN
- UC-M2A-06 NaN propagation: All indicators — NaN in input at index i → NaN in output at i and affected downstream indices
- UC-M2A-07 gRPC/HTTP: 
  - Happy: gRPC call ComputeIndicators({indicators:["sma","rsi"], data:[...]}) → valid response
  - Happy: POST /indicators/compute → valid JSON response
  - Edge: Invalid indicator name → gRPC error / HTTP 400
  - Edge: Malformed input → validation error
- UC-M2A-08 Coverage: `npm run test:coverage` → ≥90% per file

## Acceptance Criteria Checklist (for DEV-1 sign-off)
- [ ] All 5 indicators implemented with correct math (verified against reference impl)
- [ ] NaN handling consistent across all indicators
- [ ] gRPC + HTTP endpoints respond correctly
- [ ] Unit tests ≥90% coverage per indicator file
- [ ] Integration tests pass (gRPC + HTTP)
- [ ] README.md with run instructions works in clean checkout
- [ ] Analytics plan updated with M2A indicators reference

## DoD Tier 2 Checklist
- [ ] Use cases implemented (UC-M2A-01 through UC-M2A-08)
- [ ] Unit tests ≥90% coverage
- [ ] Integration tests pass
- [ ] README.md updated with run instructions
- [ ] Analytics plan updated (reference in `docs/analytics/plan.md`)
- [ ] BA specs reviewed and signed off (T-140-03)
- [ ] TECHLEAD contract review passed (T-140-04)
- [ ] QA security gate passed (T-140-05)
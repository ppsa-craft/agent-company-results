# Task: tech-analysis-140-11-m3a-alert-rules

**Task ID**: T-140-11
**Title**: M3A Alert Rule Engine — Threshold, Crossover, Multi-Condition
**Role**: DEV
**Status**: READY
**Assigned Agent**: dev-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M3A Alert Rules Service)
- `workspace/apps/tech-analysis/services/m3a-alert-rules/**`
- `workspace/apps/tech-analysis/tests/unit/m3a-alert-rules/**`
- `workspace/apps/tech-analysis/tests/integration/m3a-alert-rules/**`
- `workspace/apps/tech-analysis/docs/ba/m3a-uc-specs.md` (shared with BA)
- `workspace/apps/tech-analysis/docs/architecture/m3a-contracts.md` (shared with TECHLEAD)
- `workspace/apps/tech-analysis/security/m3a-gate-report.md` (shared with QA)

## Goal
Implement M3A Alert Rule Engine: threshold alerts, crossover alerts, multi-condition alerts. Consumes indicators from M2A Core, evaluates rules on streaming data, emits alert events.

## Acceptance Criteria (traceable to M3A-UC Specs T-140-13)
- UC-M3A-01: Threshold Alert — alert when indicator crosses above/below value
- UC-M3A-02: Crossover Alert — alert when two indicators cross (e.g., MACD line crosses signal)
- UC-M3A-03: Multi-Condition Alert — alert when ALL/ANY of N conditions met
- UC-M3A-04: Rule CRUD — create, read, update, delete rules via API
- UC-M3A-05: Rule Evaluation — evaluates on each new bar (1m, 5m, 15m, 1h, 1D)
- UC-M3A-06: Alert Emission — emits AlertEvent to message bus (NATS/Kafka)
- UC-M3A-07: Alert State — tracks firing/acknowledged/resolved state
- UC-M3A-08: Cooldown/Throttling — per-rule cooldown, max alerts per period
- UC-M3A-09: gRPC/HTTP API — rule management + evaluation trigger
- UC-M3A-10: Unit test coverage ≥90% per rule type

## Implementation Plan (for DEV-1)
**Architecture Seam**: M3A Alert Rules Service — `workspace/apps/tech-analysis/services/m3a-alert-rules/`

**Technical Approach** (per stack record):
- Language: TypeScript/Node.js (Fastify + gRPC)
- Message bus: NATS (per stack decision)
- Rule storage: PostgreSQL (rule definitions) + Redis (evaluation state)
- Indicator consumption: gRPC client to M2A Core Indicators (T-140-01)
- Rule DSL: JSON-based rule definition (AST evaluator)
- Evaluator: Pure function `evaluate(rule, indicatorSnapshot) → AlertEvent | null`

**Ordered Subtask Checklist**:
1. Scaffold service: `services/m3a-alert-rules/` with proto, src, tests
2. Define protobuf: `proto/alerts.proto` — Rule, Condition, AlertEvent, CRUD methods
3. Implement Rule AST: `src/rules/ast.ts` — Condition types (threshold, crossover, multi)
4. Implement Threshold evaluator: `src/rules/threshold.ts` — above/below, value/indicator
5. Implement Crossover evaluator: `src/rules/crossover.ts` — two series, direction
6. Implement MultiCondition evaluator: `src/rules/multi.ts` — AND/OR logic
7. Implement Rule Registry: `src/registry.ts` — CRUD, validation, versioning
8. Implement Evaluation Engine: `src/engine.ts` — subscribes to indicator stream, evaluates
9. Implement Alert State Machine: `src/state.ts` — firing → acknowledged → resolved
10. Implement Cooldown/Throttle: `src/throttle.ts` — per-rule, per-symbol
11. Implement NATS publisher: `src/publisher.ts` — emit AlertEvent to `alerts.fired`
12. Implement gRPC server: `src/server.ts` — RuleService, EvaluationService
13. Implement HTTP gateway: `src/gateway.ts` — REST for rule CRUD
14. Add input validation: Zod schemas for rule definitions
15. Unit tests: `tests/unit/m3a-alert-rules/` — ≥90% per evaluator
16. Integration tests: `tests/integration/m3a-alert-rules/` — gRPC + HTTP + NATS
17. README.md with run instructions
18. Update analytics plan reference

## Test Plan (for TESTER - T-140-12)
**Test Scenarios per Acceptance Criterion**:
- UC-M3A-01 Threshold:
  - Happy: RSI > 70 on VNM 1h → alert fired
  - Edge: RSI exactly 70 → no alert (strict >)
  - Edge: Indicator NaN → no alert, no error
  - Edge: Rule disabled → no evaluation
- UC-M3A-02 Crossover:
  - Happy: MACD line crosses above signal → bullish alert
  - Happy: MACD line crosses below signal → bearish alert
  - Edge: Cross at same value (touch) → no alert (strict cross)
  - Edge: Insufficient history (need 2 bars) → no eval
- UC-M3A-03 Multi-Condition:
  - Happy: (RSI > 70) AND (MACD bullish cross) → alert
  - Happy: (RSI > 70) OR (price > BB upper) → alert on either
  - Edge: One condition NaN → AND=false, OR=depends on other
- UC-M3A-04 CRUD:
  - Create valid rule → 201, rule persisted
  - Create invalid (bad AST) → 400
  - Get by ID → 200
  - Update → 200, version incremented
  - Delete → 204, soft delete
- UC-M3A-05 Evaluation:
  - Bar arrives → rule evaluated within 10ms
  - Multiple rules same symbol → all evaluated
- UC-M3A-06 Emission:
  - AlertEvent published to NATS `alerts.fired` subject
  - Payload: ruleId, symbol, timeframe, condition, value, timestamp
- UC-M3A-07 State:
  - Fired → ack (via API) → acknowledged
  - Auto-resolve when condition false → resolved
- UC-M3A-08 Cooldown:
  - Rule cooldown 1h → second fire within 1h suppressed
  - Max 5/day → 6th suppressed
- UC-M3A-09 API:
  - gRPC CreateRule → valid response
  - HTTP POST /rules → valid response
  - Invalid rule → 400 with validation errors
- UC-M3A-10 Coverage: `npm run test:coverage` ≥90% per evaluator file

## DoD Tier 2 Checklist
- [ ] All 10 UCs implemented
- [ ] Unit tests ≥90% coverage
- [ ] Integration tests pass
- [ ] README.md works in clean checkout
- [ ] Analytics plan updated
- [ ] BA specs reviewed (T-140-13)
- [ ] TECHLEAD contract review passed (T-140-14)
- [ ] QA security gate passed (T-140-15)
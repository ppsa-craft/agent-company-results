# Task T-139-06: M3A Alert Rules

## Goal
Implement alert rule engine (m3-alerts/rules) evaluating technical indicator conditions (crossovers, thresholds, divergences) against enriched OHLCV stream from M2B. Outputs alert events to M3B Notification Channels. Sequential after M2A (DEV-1 chain).

## Acceptance Criteria (Traceable to Use Cases)
- [ ] **UC-M3A-01**: Define alert rule DSL — conditions: `indicator > value`, `indicator_a crosses indicator_b`, `indicator crosses level`, `divergence(price, indicator)`
- [ ] **UC-M3A-02**: Rule CRUD API — `POST /rules`, `GET /rules`, `GET /rules/{id}`, `PATCH /rules/{id}`, `DELETE /rules/{id}`
- [ ] **UC-M3A-03**: Rule validation — syntax check, referenced indicators exist in M2A registry, parameters in valid ranges
- [ ] **UC-M3A-04**: Real-time evaluation — consume enriched OHLCV from M2B Kafka topic, evaluate all active rules per symbol per bar
- [ ] **UC-M3A-05**: Alert event emission — on condition transition (false→true), emit `AlertEvent` to Kafka topic `alerts.raw` with: rule_id, symbol, timestamp, condition, indicator_values, severity
- [ ] **UC-M3A-06**: Cooldown/debounce — configurable per rule (default 15m), prevents re-alert within window
- [ ] **UC-M3A-07**: Alert state tracking — `ACTIVE`, `ACKNOWLEDGED`, `RESOLVED`, `EXPIRED` with TTL (default 24h)
- [ ] **UC-M3A-08**: Historical backtest — `POST /rules/{id}/backtest` with date range → returns trigger timestamps, precision/recall if labels provided
- [ ] **UC-M3A-09**: Performance — evaluate 10k rules × 1k symbols < 100ms per bar batch
- [ ] **UC-M3A-10**: OpenAPI contract at `/contracts/m3-rules.yaml` — consumed by M3B and UI

## Estimated Effort
- **Effort**: 3 cycles (Cycle 140-142) — starts AFTER T-139-01 completes
- **DoD Tier**: Tier 2

## Assigned Agent
- **Role**: DEV
- **Agent**: dev-1
- **Cycle**: 139 (READY, blocked on T-139-01)
- **Status**: READY

## File Ownership (Disjoint Boundary: `services/m3-alerts/src/rules/`)
```
workspace/apps/tech-analysis/services/m3-alerts/
├── src/
│   ├── rules/
│   │   ├── __init__.py
│   │   ├── dsl/
│   │   │   ├── __init__.py
│   │   │   ├── parser.py           # Lark/PEG parser for rule DSL
│   │   │   ├── ast.py              # AST nodes: Comparison, Crossover, Divergence
│   │   │   ├── validator.py        # Semantic validation against M2A registry
│   │   │   └── compiler.py         # AST → evaluation function
│   │   ├── engine/
│   │   │   ├── __init__.py
│   │   │   ├── evaluator.py        # Rule evaluation per bar (vectorized)
│   │   │   ├── state.py            # AlertStateManager (cooldown, TTL, transitions)
│   │   │   └── backtest.py         # Historical evaluation
│   │   ├── registry/
│   │   │   ├── __init__.py
│   │   │   ├── store.py            # PostgreSQL + Redis cache
│   │   │   └── sync.py             # Sync with M2A indicator registry
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py           # CRUD + backtest endpoints
│   │   │   ├── schemas.py          # Pydantic models
│   │   │   └── dependencies.py
│   │   └── consumer/
│   │       ├── __init__.py
│   │       ├── handler.py          # Kafka consumer → evaluator → producer
│   │       └── metrics.py          # Prometheus metrics
│   ├── main.py
│   └── config.py
├── tests/
│   ├── unit/
│   │   ├── test_dsl_parser.py
│   │   ├── test_validator.py
│   │   ├── test_evaluator.py
│   │   ├── test_state_manager.py
│   │   └── test_backtest.py
│   ├── contract/
│   │   └── test_openapi_contract.py
│   ├── integration/
│   │   └── test_kafka_flow.py
│   └── fixtures/
│       ├── sample_rules.json
│       └── sample_ohlcv.json
├── contracts/
│   └── m3-rules.yaml
├── pyproject.toml
├── README.md
└── Dockerfile
```

## Implementation Plan (for DEV)

**Architecture Seam**: `services/m3-alerts/src/rules/` — disjoint from `src/channels/` (T-139-07). Communicates with M2B via Kafka topic `enriched.ohlcv`. Outputs to `alerts.raw` for M3B.

**Tech Stack**: Python 3.11, FastAPI, Lark for DSL parser, Faust/Kafka consumer, PostgreSQL (rules), Redis (state cache), Prometheus client.

**Ordered Subtask Checklist**:
1. [ ] Wait for T-139-01 completion (M2A contract published)
2. [ ] Scaffold service structure (shared m3-alerts repo with channels)
3. [ ] Implement DSL parser (`parser.py`) — grammar for: comparison, crossover, threshold, divergence
4. [ ] Implement AST nodes (`ast.py`) + compiler to evaluation lambdas
5. [ ] Implement validator (`validator.py`) — checks indicator names against M2A registry (HTTP call at startup, cached)
6. [ ] Implement evaluator (`evaluator.py`) — vectorized NumPy evaluation per symbol per bar
7. [ ] Implement state manager (`state.py`) — cooldown, TTL, state transitions, Redis-backed
8. [ ] Implement backtest engine (`backtest.py`) — replays historical bars, returns triggers
9. [ ] Implement registry sync (`sync.py`) — periodic fetch from M2A `/indicators` endpoint
10. [ ] Implement API layer (CRUD + backtest) with Pydantic schemas
11. [ ] Implement Kafka consumer/producer (`handler.py`) — exactly-once semantics
12. [ ] Write OpenAPI contract `contracts/m3-rules.yaml`
13. [ ] Unit tests: DSL parser (all operators), validator (valid/invalid), evaluator (vectorized correctness), state manager (cooldown, TTL, transitions), backtest
14. [ ] Contract test against OpenAPI spec
15. [ ] Integration test: Kafka → evaluator → producer (Testcontainers)
16. [ ] Performance test: 10k rules × 1k symbols benchmark
17. [ ] README + run instructions
18. [ ] Analytics: rule_eval_latency_ms, alert_emitted_total, cooldown_skipped_total
19. [ ] Docker build test

**Dependencies**: T-139-01 (M2A contract) MUST complete first. T-139-07 (M3B channels) consumes `alerts.raw` topic.

## Test Plan (for TESTER)

**Happy Path Scenarios**:
1. **Rule create + evaluate**: POST rule `RSI > 70` → consume bar with RSI=75 → alert emitted to `alerts.raw`
2. **Crossover detection**: Rule `SMA_50 crosses SMA_200` → golden cross bar → alert emitted
3. **Cooldown enforcement**: Rule triggers → immediate next bar same condition → no alert (cooldown active)
4. **State transitions**: Alert ACTIVE → ACKNOWLEDGED (API) → RESOLVED (condition false + TTL) → EXPIRED
5. **Backtest**: POST `/rules/{id}/backtest` with 1yr data → returns trigger timestamps matching manual calc
6. **Vectorized eval**: 1000 symbols, 100 rules, single bar batch → < 100ms

**Edge Cases**:
1. Invalid DSL (unknown indicator, syntax error) → 400 with parse error location
2. Rule references indicator not in M2A registry → validation error at create time
3. Divergence condition (price higher high, RSI lower high) → correctly detected
4. Kafka consumer restart → state recovered from Redis, no duplicate alerts
5. M2A registry sync failure → cached registry used, alert logged
6. Backtest with missing bars → handled gracefully (skip, log gap)

**Expected Results**: All scenarios pass. Contract test validates API. Performance test meets <100ms. Integration test uses real Kafka.

## DoD Tier 2 Checklist
- [ ] All 10 UCs implemented with tests
- [ ] OpenAPI contract published and validated
- [ ] Unit tests ≥ 90% coverage on rules/
- [ ] Contract test passing
- [ ] Integration test with Kafka passing
- [ ] Performance benchmark documented
- [ ] README with run instructions
- [ ] Analytics events instrumented
- [ ] Code review approved
- [ ] No file overlap with M3B channels (verified)
# Task T-139-05: M2B-UC Specs (BA)

## Goal
Produce use cases and acceptance criteria for M2B Data Pipeline service (m2-pipeline). Debated per §5.1 before build starts. Validated against CEO strategy. Output feeds DEV-2 (T-139-02) and TESTER (T-139-03).

## Acceptance Criteria (BA Doc Quality Gates)
- [ ] **DOC-01**: Use case diagram (Mermaid) showing actors (Kafka, M2A, TimescaleDB, M3 Alerting) and 10 UCs
- [ ] **DOC-02**: Each UC has: ID, title, actor, precondition, main flow, alternate flows, postcondition, acceptance criteria (Gherkin)
- [ ] **DOC-03**: Non-functional requirements: throughput (10k msg/s), latency (<500ms p99 e2e), durability (exactly-once), replayability
- [ ] **DOC-04**: Data contracts: raw OHLCV protobuf, enriched OHLCV+indicators protobuf, DLQ message schema
- [ ] **DOC-05**: Validation rules catalog: all OHLCV checks with error codes (e.g., `OHLC_INVALID_HIGH_LOW`, `VOLUME_NEGATIVE`, `TIMESTAMP_NON_MONOTONIC`, `GAP_EXCEEDS_THRESHOLD`)
- [ ] **DOC-06**: Gap handling policy: forward-fill ≤5min, mark `gap_filled=true`, longer gaps → separate bar with `gap_filled=false`
- [ ] **DOC-07**: Backfill specification: idempotency key design, checkpoint tracking, progress reporting, concurrency limits
- [ ] **DOC-08**: M2A integration contract: request/response shapes, retry policy, circuit breaker config, timeout budget
- [ ] **DOC-09**: Analytics events defined per UC (pipeline_lag_ms, throughput_msg_s, dlq_size, validation_errors_total, enrichment_latency_ms, backfill_progress_pct)
- [ ] **DOC-10**: Debate record + PM/CTO sign-off, published at `docs/ba/m2b-uc-specs.md`

## Estimated Effort
- **Effort**: 1 cycle (Cycle 139)
- **DoD Tier**: Tier 2 (BA docs quality-gated)

## Assigned Agent
- **Role**: BA
- **Agent**: ba-2
- **Cycle**: 139
- **Status**: READY

## File Ownership
```
workspace/apps/tech-analysis/docs/ba/m2b-uc-specs.md
```

## Implementation Plan (for BA)

**Deliverable**: Single markdown file `m2b-uc-specs.md`.

**Structure**:
1. **Overview**: Pipeline role, data flow diagram (Mermaid)
2. **Use Case Diagram** (Mermaid)
3. **Use Cases** (UC-M2B-01 through UC-M2B-10) — full template
3. **Non-Functional Requirements** table
4. **Data Contracts** (protobuf schemas + JSON equivalents)
5. **Validation Rules Catalog** (table: rule, condition, error code, DLQ payload)
6. **Gap Handling Policy** (decision tree)
7. **Backfill Specification** (idempotency key = hash(symbol+start+end), checkpoint table)
8. **M2A Integration Contract** (retry: 3x exp backoff 100/500/2000ms, CB: 50% errors/10s → open 30s)
9. **Analytics Events** table
10. **Debate Record**
11. **Sign-off**

**Process**:
1. [ ] Review M2A UC specs (T-139-04) for integration contract alignment
2. [ ] Draft UCs 1-6 (core pipeline flow)
3. [ ] Draft UCs 7-10 (backfill, health, NFR, contract)
4. [ ] Define protobuf schemas (coordinate with shared `market-data-protos` package)
5. [ ] Document validation rules exhaustively (cover all OHLCV invariant violations)
6. [ ] Specify gap handling — debate if threshold should be 5min or 15min
7. [ ] Design backfill idempotency (critical for correctness)
8. [ ] Define analytics events with concrete payload examples
9. [ ] Run debate if needed (gap threshold, exactly-once vs at-least-once)
9. [ ] PM/CTO sign-off
10. [ ] Publish to `docs/ba/m2b-uc-specs.md`

**Dependencies**: T-139-04 (M2A UC specs) for integration contract. T-139-02 (DEV-2) and T-139-03 (TESTER) consume this.

## Test Plan (for TESTER — validation of BA output)

**Validation Scenarios**:
1. **Completeness**: All 10 UCs with full template
2. **Validation exhaustiveness**: Every OHLCV invariant has a rule + error code
3. **Protobuf schemas**: Valid .proto files, compile with protoc, match JSON examples
4. **Gap policy clarity**: Decision tree covers all cases (no gap, ≤5min, >5min, weekend)
5. **Backfill idempotency**: Spec enables testable idempotency (re-run = no dupes)
6. **M2A contract**: Retry/CB/timeout values concrete, match DEV implementation plan
7. **Analytics**: Events have schemas, cover all observability needs

**Expected Results**: BA doc passes PM/CTO review. DEV-2 implements without clarification. TESTER writes integration tests from specs.

## DoD Tier 2 Checklist
- [ ] All 10 DOC criteria met
- [ ] Mermaid diagrams render
- [ ] Gherkin acceptance criteria per UC
- [ ] Protobuf schemas included/referenced
- [ ] Validation rules catalog complete
- [ ] Gap handling decision documented
- [ ] Backfill idempotency design specified
- [ ] Debate record + sign-offs
- [ ] Published at correct path
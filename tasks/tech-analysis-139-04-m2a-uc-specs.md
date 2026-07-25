# Task T-139-04: M2A-UC Specs (BA)

## Goal
Produce use cases and acceptance criteria for M2A Core Indicators service (m2-indicators). Debated per §5.1 before build starts. Validated against CEO strategy. Output feeds DEV-1 (T-139-01) and TESTER (T-139-03).

## Acceptance Criteria (BA Doc Quality Gates)
- [ ] **DOC-01**: Use case diagram (Mermaid) showing actors (Trader, AlgoEngine, M2B Pipeline) and 10 UCs
- [ ] **DOC-02**: Each UC has: ID, title, actor, precondition, main flow, alternate flows, postcondition, acceptance criteria (Gherkin-style)
- [ ] **DOC-03**: Non-functional requirements: latency (<50ms p99), throughput (10k req/s), availability (99.9%), data freshness
- [ ] **DOC-04**: Data contracts: input OHLCV schema, output indicator schema, error schema (RFC 7807)
- [ ] **DOC-05**: Indicator formulas appendix (mathematical definitions for all 7 indicators — source: TA-Lib / standard definitions)
- [ ] **DOC-06**: Edge case behaviors documented: NaN propagation, insufficient data, flat prices, weekend gaps
- [ ] **DOC-07**: Analytics events defined per UC (event name, payload schema, sample)
- [ ] **DOC-08**: Debate record: link to debate artifact, resolution of any contested decisions
- [ ] **DOC-09**: Signed off by PM (business alignment) and CTO (technical feasibility)
- [ ] **DOC-10**: Published at `workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md`

## Estimated Effort
- **Effort**: 1 cycle (Cycle 139)
- **DoD Tier**: Tier 2 (BA docs quality-gated like code)

## Assigned Agent
- **Role**: BA
- **Agent**: ba-1
- **Cycle**: 139
- **Status**: READY

## File Ownership
```
workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md
```

## Implementation Plan (for BA)

**Deliverable**: Single markdown file `m2a-uc-specs.md` with all sections.

**Structure**:
1. **Overview**: Service purpose, scope, actors
2. **Use Case Diagram** (Mermaid)
3. **Use Cases** (UC-M2A-01 through UC-M2A-10) — each with full template
4. **Non-Functional Requirements** table
5. **Data Contracts** (JSON Schema for request/response/error)
6. **Indicator Formulas** appendix (with references)
7. **Edge Case Behaviors** table
8. **Analytics Events** table
9. **Debate Record** (link + summary)
10. **Sign-off** section

**Process**:
1. [ ] Review CEO strategy for technical analysis engine (target users: retail traders, algo devs)
2. [ ] Draft UCs 1-7 (core indicators) with formulas from standard sources (Wilder, Bollinger, etc.)
3. [ ] Draft UCs 8-10 (API, performance, contract)
4. [ ] Define data contracts aligned with M2B consumer needs (from T-139-02 UC-M2B-04)
5. [ ] Document edge cases based on TA-Lib behavior + production reality
6. [ ] Define analytics events (indicator_calculated, batch_latency, error)
7. [ ] Run debate (§5.1) if any UC contested (e.g., RSI formula variant, NaN vs 50 for flat)
8. [ ] Incorporate debate resolutions
9. [ ] PM review (business alignment), CTO review (feasibility)
10. [ ] Publish to `docs/ba/m2a-uc-specs.md`

**Dependencies**: None (starts immediately). T-139-01 (DEV) and T-139-03 (TESTER) consume this.

## Test Plan (for TESTER — validation of BA output)

**Validation Scenarios**:
1. **Completeness**: All 10 UCs present with full template fields
2. **Traceability**: Each UC acceptance criterion maps to a test case in T-139-01/T-139-03
3. **Contract alignment**: Request/response schemas match what DEV will implement
4. **Formula correctness**: Indicator formulas match standard definitions (cross-ref TA-Lib)
5. **Edge case coverage**: NaN, flat, insufficient data, gaps all addressed
6. **Analytics actionability**: Events have payload schemas, can be implemented

**Expected Results**: BA doc passes PM/CTO sign-off. DEV can implement without clarification. TESTER can write contract tests directly from schemas.

## DoD Tier 2 Checklist
- [ ] All 10 DOC criteria met
- [ ] Mermaid diagram renders correctly
- [ ] Gherkin-style acceptance criteria for each UC
- [ ] Data contracts as JSON Schema (validatable)
- [ ] Debate record linked (or "no debate required" noted)
- [ ] PM sign-off recorded
- [ ] CTO sign-off recorded
- [ ] Published at correct path
- [ ] Analytics events defined with schemas
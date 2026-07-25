# Task: tech-analysis-140-13-m3a-uc-specs

**Task ID**: T-140-13
**Title**: M3A-UC Specs (BA)
**Role**: BA
**Status**: READY
**Assigned Agent**: ba-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership
- `workspace/apps/tech-analysis/docs/ba/m3a-uc-specs.md`

## Goal
Produce Use Case specifications for M3A Alert Rule Engine (T-140-11) traceable to M3A milestone goals.

## Acceptance Criteria
- UC-M3A-01 through UC-M3A-10 fully specified per BA template
- Each UC includes: Actor, Preconditions, Postconditions, Main Flow, Alternative Flows, Error Flows, NFR (eval latency <10ms p99, throughput >10k rules/sec, NATS emit <5ms), Data Contracts (Rule AST JSON schema, AlertEvent protobuf schema with examples)
- Edge cases: NaN indicators, disabled rules, cooldown active, NATS unavailable, rule version conflicts
- Document reviewed and signed off by PM before DEV starts
- Versioned at `workspace/apps/tech-analysis/docs/ba/m3a-uc-specs.md`

## BA Specification Template
See T-140-03. Apply to M3A UCs:
- UC-M3A-01: Threshold Alert — single indicator vs value
- UC-M3A-02: Crossover Alert — two indicator series cross
- UC-M3A-03: Multi-Condition Alert — boolean logic (AND/OR/NOT) over conditions
- UC-M3A-04: Rule CRUD — lifecycle management
- UC-M3A-05: Stream Evaluation — per-bar evaluation on indicator stream
- UC-M3A-06: Alert Emission — NATS event publishing
- UC-M3A-07: Alert State Machine — fired → ack → resolved
- UC-M3A-08: Throttling/Cooldown — per-rule, per-symbol
- UC-M3A-09: API Contract — gRPC + HTTP rule management
- UC-M3A-10: Accuracy — evaluation matches reference implementation

## Data Contract Examples Required
- Rule AST JSON (all condition types)
- AlertEvent protobuf message
- gRPC CreateRuleRequest/Response
- HTTP POST /rules request/response

## DoD Tier 2 Checklist
- [ ] All 10 UCs specified with template fields
- [ ] NFRs defined per UC
- [ ] Data contracts with JSON/protobuf examples
- [ ] PM sign-off obtained
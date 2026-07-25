# Task: tech-analysis-140-08-m2b-uc-specs

**Task ID**: T-140-08
**Title**: M2B-UC Specs (BA)
**Role**: BA
**Status**: READY
**Assigned Agent**: ba-2
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership
- `workspace/apps/tech-analysis/docs/ba/m2b-uc-specs.md`

## Goal
Produce Use Case specifications for M2B Data Pipeline Service (T-140-06) traceable to M2B milestone goals.

## Acceptance Criteria
- UC-M2B-01 through UC-M2B-14 fully specified per BA template
- Each UC includes: Actor, Preconditions, Postconditions, Main Flow, Alternative Flows, Error Flows, NFR (latency <100ms p99 ingestion, throughput >10k symbols/min), Data Contracts (input/output schemas with examples)
- Edge cases covered: source API failure, rate limit, malformed data, timezone ambiguity, duplicate timestamps, gap fill strategies
- Document reviewed and signed off by PM before DEV starts
- Versioned at `workspace/apps/tech-analysis/docs/ba/m2b-uc-specs.md`

## BA Specification Template (per UC)
See T-140-03 for template structure. Apply to M2B UCs:
- UC-M2B-01: VN Source Adapter — VNDirect, CafeF, VietStock
- UC-M2B-02: Normalization — schema mapping, type coercion, timezone to UTC
- UC-M2B-03: Gap Detection — missing timestamps, gap classification
- UC-M2B-04: Gap Fill — forward fill, linear interpolation, none
- UC-M2B-05: Storage — TimescaleDB hypertable write, partitioning
- UC-M2B-06: gRPC GetBars — query by symbol, timeframe, range
- UC-M2B-07: HTTP GET /bars — REST gateway
- UC-M2B-08: Health/Readiness — liveness/readiness probes
- UC-M2B-09: Metrics — Prometheus exposition
- UC-M2B-10: Source Circuit Breaker — trip on 5xx, half-open
- UC-M2B-11: Rate Limiting — token bucket per source
- UC-M2B-12: Data Quality Metrics — completeness, freshness, anomaly score
- UC-M2B-13: Replay/Backfill — historical re-ingestion
- UC-M2B-14: Symbol Registry — VN symbol master data management

## DoD Tier 2 Checklist
- [ ] All 14 UCs specified with template fields
- [ ] NFRs defined per UC
- [ ] Data contracts with JSON examples
- [ ] PM sign-off obtained
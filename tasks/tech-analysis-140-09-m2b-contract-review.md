# Task: tech-analysis-140-09-m2b-contract-review

**Task ID**: T-140-09
**Title**: M2B Contract Review (TECHLEAD)
**Role**: TECHLEAD
**Status**: READY
**Assigned Agent**: techlead-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M2B Data Pipeline Service)
- `workspace/apps/tech-analysis/docs/architecture/m2b-contracts.md`

## Goal
Review and approve M2B Data Pipeline Service contracts (gRPC, HTTP, storage interface, adapter interfaces) against BA specs and architecture principles.

## Acceptance Criteria
- Contract review document completed with:
  - gRPC service review: `GetBars`, `SubscribeBars`, `GetSymbols`, `HealthCheck`
  - HTTP gateway review: REST mappings, query params, response envelopes
  - Adapter interface contract: `fetch()`, `healthCheck()`, `getRateLimit()`
  - Storage interface contract: `write()`, `query()`, `healthCheck()`
  - Normalization pipeline contract: input/output schemas, config schema
  - Error code taxonomy alignment
  - Versioning strategy (proto field numbers, HTTP API versioning)
  - Performance budgets: ingestion <100ms p99, query <50ms p99
  - Security contracts: auth, rate limits, input validation
- Review result: APPROVED / CHANGES_REQUESTED / REJECTED
- DEV-2 (T-140-06) unblocked or blocked with rationale

## Review Checklist
- [ ] Service boundaries: M2B owns ingestion→normalization→storage, NOT indicator computation
- [ ] Dependency direction: M2B → TA Core Library (for shared types), NOT reverse
- [ ] gRPC follows company protobuf style (naming, field numbers, options)
- [ ] HTTP gateway uses standard REST (not RPC-over-HTTP)
- [ ] Adapter interface is pluggable (new sources add without core changes)
- [ ] Storage interface abstracts TimescaleDB (testable with mock)
- [ ] Normalization config is declarative (not code)
- [ ] Observability contracts: metric names, log fields, trace attributes defined

## Deliverables
- `workspace/apps/tech-analysis/docs/architecture/m2b-contracts.md`
- Review result in document header
- Inline comments if CHANGES_REQUESTED

## DoD Tier 2 Checklist
- [ ] Contract review document completed
- [ ] Review result recorded
- [ ] DEV-2 unblocked or blocked with rationale
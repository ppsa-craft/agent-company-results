# Task: tech-analysis-140-14-m3a-contract-review

**Task ID**: T-140-14
**Title**: M3A Contract Review (TECHLEAD)
**Role**: TECHLEAD
**Status**: READY
**Assigned Agent**: techlead-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership
- `workspace/apps/tech-analysis/docs/architecture/m3a-contracts.md`

## Goal
Review and approve M3A Alert Rule Engine contracts against BA specs (T-140-13) and architecture principles.

## Acceptance Criteria
- Contract review document completed with:
  - gRPC service review (RuleService: CreateRule, GetRule, UpdateRule, DeleteRule, ListRules, EvaluateRule)
  - HTTP gateway review (REST mapping for CRUD)
  - NATS event schema review (AlertEvent subject, payload)
  - Rule AST schema review (JSON schema for conditions: threshold, crossover, composite)
  - Error handling contract (gRPC codes, HTTP mapping)
  - Versioning strategy (proto, AST schema version)
  - Performance contract (eval latency <10ms p99, throughput >10k rules/sec)
  - Security contract (auth, rate limits, input validation on rule AST)
  - Observability contract (metrics: rules_evaluated, alerts_fired, eval_latency)
- Review result: APPROVED / CHANGES_REQUESTED / REJECTED with rationale
- DEV-1 (T-140-11) unblocked or blocked with clear rationale

## Review Checklist
- [ ] Service boundary: M3A owns alert rules only, consumes M2A indicators via gRPC
- [ ] No circular deps: M3A → M2A (indicators), M3A → NATS (events)
- [ ] gRPC follows protobuf style guide
- [ ] HTTP follows REST conventions (POST /rules, GET /rules/:id)
- [ ] NATS subject naming: `alerts.fired.{symbol}.{timeframe}`
- [ ] Rule AST schema supports all UC-M3A conditions with versioning
- [ ] Input validation: Zod schema on rule creation (reject malicious AST)
- [ ] Rate limits: rule creation 100/min, evaluation internal only
- [ ] Metrics names follow `tech_analysis_m3a_*` prefix

## Deliverables
- `workspace/apps/tech-analysis/docs/architecture/m3a-contracts.md` — completed review
- Review result in document header

## DoD Tier 2 Checklist
- [ ] Contract review document completed
- [ ] Review result recorded
- [ ] DEV-1 unblocked or blocked with rationale
- [ ] Document committed
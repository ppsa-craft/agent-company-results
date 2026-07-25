# Task: vn-stock-M2-1-dev-feature-store

**Product:** vn-stock (VN Stock Suggestion System)
**Cycle:** 137
**Milestone:** M2: Recommendation Engine Core
**Role:** DEV
**DoD Tier:** Tier 2 — Feature (use cases + tests + docs/README update + analytics update)
**Assigned Agent:** dev (1 of 4 parallel DEV instances)
**Depends On:** vn-stock-M2-14-techlead-fs-contract (TECHLEAD contract review must be APPROVED)
**Architecture Seam:** Feature Store Service — disjoint file tree: `workspace/apps/vn-stock/services/feature-store/**`

---

## Goal
Implement the Feature Store service for M2: real-time feature serving for candidate generation, ranking, and portfolio optimization. This service owns the feature_store.proto contract (frozen by TECHLEAD review) and serves feature vectors at <10ms p99 latency.

---

## Acceptance Criteria (traceable to M2 use cases)

| AC ID | Use Case | Acceptance Criterion |
|-------|----------|----------------------|
| AC-M2-FS-01 | UC-M2-01: Real-time Feature Serving | FeatureStore.GetFeatures(gRPC) returns feature vector for entity_id in <10ms p99 |
| AC-M2-FS-02 | UC-M2-02: Feature Freshness | FeatureStore.RefreshFeatures() updates feature cache within 5s of source data commit |
| AC-M2-FS-03 | UC-M2-03: Feature Schema Evolution | FeatureStore.RegisterFeature() accepts new feature definitions without service restart |
| AC-M2-FS-04 | UC-M2-04: Multi-tenant Isolation | FeatureStore enforces tenant_id isolation — tenant A cannot read tenant B features |
| AC-M2-FS-05 | UC-M2-05: Observability | /metrics exposes feature_store_requests_total, feature_store_latency_seconds, feature_store_cache_hit_ratio |

---

## Implementation Plan (for DEV)

### Architecture Seam
**Feature Store Service** — owns `workspace/apps/vn-stock/services/feature-store/**` exclusively. No other DEV task touches this directory. Contract: `feature_store.proto` (frozen by vn-stock-M2-14-techlead-fs-contract).

### Files/Modules to Create/Touch
```
workspace/apps/vn-stock/services/feature-store/
├── cmd/feature-store/main.go                    # Service entrypoint
├── internal/
│   ├── server/feature_store_server.go           # gRPC server impl
│   ├── storage/
│   │   ├── redis_store.go                       # Redis feature cache
│   │   └── postgres_store.go                    # Postgres feature definitions
│   ├── cache/
│   │   └── feature_cache.go                     # In-memory LRU + TTL
│   ├── registry/
│   │   └── feature_registry.go                  # Feature definition registry
│   └── tenant/
│       └── tenant_resolver.go                   # Tenant isolation middleware
├── api/feature_store.proto                      # Frozen by TECHLEAD review
├── go.mod / go.sum
├── Dockerfile
├── Makefile
├── README.md                                    # How-to-run (Tier 2 requirement)
└── configs/
    ├── config.yaml.example
    └── config.prod.yaml
```

### New Interfaces/Data Contracts
- `feature_store.proto` — gRPC service: `GetFeatures`, `RefreshFeatures`, `RegisterFeature`, `ListFeatures`
- `FeatureVector` message — repeated `FeatureValue` (name, value, timestamp, dtype)
- `FeatureDefinition` message — name, dtype, description, source, refresh_interval_s
- Tenant isolation via `tenant_id` in all RPC metadata

### Ordered Subtask Checklist
- [ ] 1. Scaffold service: go.mod, Dockerfile, Makefile, config.yaml.example, README.md skeleton
- [ ] 2. Implement gRPC server skeleton with health/ready endpoints
- [ ] 3. Implement Postgres store for feature definitions (CRUD + list)
- [ ] 4. Implement Redis cache for feature vectors (GET/SET with TTL)
- [ ] 4. Implement in-memory LRU cache with TTL for hot features (<10ms p99)
- [ ] 5. Implement feature registry (RegisterFeature, ListFeatures, schema validation)
- [ ] 6. Implement tenant resolver middleware (extract tenant_id from gRPC metadata)
- [ ] 7. Implement GetFeatures RPC: cache lookup → Redis → Postgres fallback → assemble FeatureVector
- [ ] 8. Implement RefreshFeatures RPC: invalidate cache, trigger async refresh
- [ ] 9. Add Prometheus metrics (requests_total, latency_seconds, cache_hit_ratio)
- [ ] 10. Add structured logging (request_id, tenant_id, latency_ms)
- [ ] 11. Write unit tests for each internal package (>80% coverage)
- [ ] 12. Write integration tests against testcontainers (Redis, Postgres)
- [ ] 13. Update README.md with: how to run locally, config reference, API examples, latency benchmarks
- [ ] 14. Update analytics plan: emit `feature_served` event with feature_names, latency_ms, cache_hit, tenant_id
- [ ] 15. Run `make test` and `make build` — verify clean

---

## Test Plan (for TESTER)

### Test Scenarios per Acceptance Criterion

| Scenario ID | AC | Steps | Expected Result |
|-------------|-----|-------|-----------------|
| TS-M2-FS-01 | AC-M2-FS-01 | 1. Register 100 features via RegisterFeature<br>2. Call GetFeatures for entity_id "stock:VNM" with 50 features<br>3. Measure latency over 1000 requests | p99 latency < 10ms; all 50 features returned with correct values |
| TS-M2-FS-02 | AC-M2-FS-01 | 1. Call GetFeatures for non-existent entity_id<br>2. Call GetFeatures with empty feature list | Returns NOT_FOUND for unknown entity; returns empty FeatureVector for empty list |
| TS-M2-FS-03 | AC-M2-FS-02 | 1. Update feature definition in Postgres<br>2. Call RefreshFeatures<br>3. Call GetFeatures within 5s | Updated feature value returned within 5s |
| TS-M2-FS-04 | AC-M2-FS-03 | 1. Call RegisterFeature with new feature definition<br>2. Call GetFeatures requesting new feature | New feature served without service restart |
| TS-M2-FS-05 | AC-M2-FS-04 | 1. Tenant A registers feature "price"<br>2. Tenant B calls GetFeatures for "price"<br>3. Tenant A calls GetFeatures for "price" | Tenant B gets NOT_FOUND; Tenant A gets feature value |
| TS-M2-FS-06 | AC-M2-FS-05 | 1. Call /metrics endpoint<br>2. Make 100 GetFeatures requests<br>3. Check metrics | feature_store_requests_total=100; latency histogram populated; cache_hit_ratio > 0 |

### Edge Cases
- Empty feature list in GetFeatures → empty FeatureVector
- Feature definition with invalid dtype → INVALID_ARGUMENT
- Redis connection failure → fallback to Postgres, degraded latency
- Postgres connection failure → return cached values, log error
- Tenant_id missing from metadata → INVALID_ARGUMENT
- Concurrent RegisterFeature for same name → idempotent update

### Restart Behavior
- Service restart: Redis cache cold, Postgres definitions intact → first requests slower, then <10ms p99
- Config reload (SIGHUP): new config applied without restart

---

## Definition of Done (Tier 2)
- [ ] All ACs verified by TESTER (test report linked)
- [ ] Unit tests >80% coverage (coverage report)
- [ ] Integration tests pass (testcontainers)
- [ ] README.md complete: local run, config, API examples, benchmark results
- [ ] Analytics events implemented and documented
- [ ] TECHLEAD review APPROVED (vn-stock-M2-14-techlead-fs-contract)
- [ ] QA security gate PASS (vn-stock-M2-23-qa-security-gate)
- [ ] Changelog entry added
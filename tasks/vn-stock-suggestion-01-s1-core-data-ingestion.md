# Task: vn-stock-suggestion-01-s1-core-data-ingestion

## Goal
Implement S1 Data Ingestion Service: core component that ingest real-time VN stock price data from multiple sources and normalizes into standardized `RawPriceTick` events published to Kafka.

## Acceptance Criteria (traceable to use cases)
- UC-ING-01: System fetches real-time VN stock data from VNIndex API every 5 seconds per symbol
- UC-ING-02: Ingestion normalizes all source responses to canonical `RawPriceTick` schema (symbol, price, volume, timestamp, source)
- UC-ING-03: Handles API errors with exponential backoff (max 3 retries, 100ms-2s delay)
- UC-ING-04: Publishes normalized ticks to Kafka topic `raw.price.ticks.vn` via shared Kafka producer library
- UC-ING-05: Provides health endpoint `/health` and metrics endpoint `/metrics` (Prometheus format)
- UC-ING-06: Runs as Kubernetes Deployment with HPA (CPU-based, min 1, max 10 replicas)
- UC-ING-07: Integration test validates end-to-end: source API → ingestion → Kafka → schema validation

## DoD Tier
Tier 1 — Product launch: full artifact table (code, working product + tests + docs + analytics + launch readiness)

## Estimated Effort
4 dev-days (DEV implementation) + 1 test-day (TESTER integration tests)

## Assigned Agent
DEV (implementation), TESTER (integration test harness)

## Implementation Plan (for DEV)
**Architecture Seam**: PKG-01 Data Ingestion Layer — Core ingestion service (independent module, zero code sharing with other ingestion workers except shared Kafka producer)

**Files/Modules to Create**:
```
vn-stock-suggestion/
└── services/
    └── s1-core/
        ├── cmd/
        │   └── ingestion/
        │       └── main.go                 # Entry point, config loading, graceful shutdown
        ├── internal/
        │   ├── config/
        │   │   └── config.go               # Ingestion-specific config (sources, intervals, symbols)
        │   ├── fetcher/
        │   │   └── fetcher.go             # Multi-source data fetcher with retry/backoff
        │   ├── normalizer/
        │   │   └── normalizer.go           # Source response → RawPriceTick normalization
        │   ├── publisher/
        │   │   └── publisher.go           # Wrapper around PKG-01F Kafka producer
        │   ├── health/
        │   │   └── health.go              # /health and /metrics endpoints
        ├── pkg/
        │   └── schema/
        │       └── raw_price_tick.proto    # Protobuf schema for RawPriceTick (shared)
        ├── configs/
        │   └── config.yaml.example        # Example config with source endpoints
        ├── deploy/
        │   ├── deployment.yaml            # K8s Deployment with HPA
        │   ├── service.yaml               # K8s Service for health/metrics
        │   ├── hpa.yaml                   # HorizontalPodAutoscaler
        │   └── configmap.yaml             # ConfigMap for non-secret config
        ├── Dockerfile
        ├── go.mod / go.sum
        ├── Makefile
        └── README.md
```

**Shared Dependency**: PKG-01F Kafka Producer Library (`github.com/vn-stock-suggestion/kafka-producer-lib`)

**Ordered Subtask Checklist**:
1. [ ] Scaffold Go module with Makefile (`build`, `test`, `docker-build`, `deploy` targets)
2. [ ] Implement `config.go` — env/file loading, validate sources (VNIndex, CafeF, Vietstock, VNDirect), intervals, symbol list
3. [ ] Implement `fetcher.go` — HTTP clients per source, exponential backoff (100ms-2s), request signing per source API spec, 5s timeout
4. [ ] Implement `normalizer.go` — map source JSON fields to `RawPriceTick` protobuf (symbol normalization, price scaling, timestamp to Unix ms)
5. [ ] Implement `publisher.go` — wrapper around PKG-01F `KafkaProducer` with topic `raw.price.ticks.vn`, schema registry integration, async produce with callbacks
6. [ ] Implement `main.go` — wire config → fetcher → normalizer → publisher; goroutine per symbol; graceful shutdown (SIGTERM drain)
7. [ ] Implement `health.go` — `/health/live`, `/health/ready` (Kafka/schema registry ready), `/metrics` (Prometheus)
8. [ ] Write K8s manifests with resource limits (CPU 100m/500m, Mem 128Mi/512Mi), HPA min 1/max 10 CPU 70%
9. [ ] Write `Dockerfile` (multi-stage builder → distroless, non-root user)
10. [ ] Write unit tests for fetcher (source API), normalizer (table-driven with sample payloads), health endpoints
11. [ ] Write `README.md` with architecture, config, local run (docker-compose), K8s deploy, health/metrics

**Integration Points**:
- Consumes: PKG-01F shared Kafka producer library (go module)
- Produces: Kafka topic `raw.price.ticks.vn` with `RawPriceTick` Avro/Protobuf schema (schema registry)
- Depends on: PKG-01H integration test harness (Testcontainers Kafka + mocked source APIs)

## Test Plan (for TESTER)
**Test Environment**: Testcontainers (Kafka + Schema Registry + mocked source HTTP servers)

**Scenarios**:
1. **Happy Path — Single Source**
   - Start Testcontainers Kafka + Schema Registry
   - Start mocked VNIndex HTTP server returning valid price tick
   - Start ingestion service with config for VNIndex symbol "VNM"
   - Wait 30 seconds (6 fetches at 5s intervals)
   - Consume from `raw.price.ticks.vn`, verify:
     - Exactly 6 messages received (1/5s × 30s)
     - Each message: valid `RawPriceTick` schema, symbol="VNM", source="VNIndex", price>0, volume≥0, timestamp within last 30s
   - **Expected**: PASS

2. **Multiple Sources**
   - Config with sources [VNIndex, CafeF], symbols ["VNM", "VIC"]
   - Run 60 seconds
   - Consume topic, verify 8 messages total (4 per source), each with correct symbol and source field
   - **Expected**: PASS

3. **Error Handling — 429 Rate Limited**
   - Mock source returns 429 with `Retry-After: 2`
   - Ingestion should back off 2s, then retry
   - Verify backoff logged, metrics `ingestion_rate_limited_total` incremented
   - **Expected**: PASS

4. **Error Handling — 500 Server Error**
   - Mock source returns 500 for 3 requests, then 200
   - Ingestion retries with exponential backoff (100ms, 200ms, 400ms)
   - Verify eventual success, metrics tracking
   - **Expected**: PASS

5. **Error Handling — Timeout**
   - Mock source delays 15s (client timeout 10s)
   - Ingestion should timeout, log error, back off, retry next cycle
   - Verify `ingestion_timeouts_total` incremented, worker continues
   - **Expected**: PASS

6. **Schema Validation — Invalid Payload**
   - Mock source returns malformed JSON (missing required field)
   - Ingestion normalizer should log error, NOT publish, continue next cycle
   - **Expected**: PASS

7. **Graceful Shutdown**
   - Start ingestion service, send SIGTERM
   - Verify in-flight request complete or cancelled, producer `Flush()` called, `/health/ready` returns 503
   - **Expected**: PASS

8. **K8s Deployment Validation**
   - Apply K8s manifests to kind cluster
   - Verify Deployment creates 1 pod, HPA created, Service exposes :8080
   - Scale HPA to 3 replicas → 3 pods running
   - **Expected**: PASS

**Restart Behavior**: After pod restart, service reconnects to Kafka, re-registers schema, resumes polling from config symbol list — no offset commitment needed.

## Artifacts to Produce
- `services/s1-core/` — complete Go service
- `services/s1-core/deploy/*.yaml` — K8s manifests
- `services/s1-core/README.md` — runbook
- Unit tests (`*_test.go`)
- Integration test (TESTER writes in `tasks/vn-stock-suggestion-02-s1-integration-test.md`)

## Dependencies
- **Blocks**: PKG-01H (Integration Test Harness needs this service)
- **Depends on**: PKG-01F (Kafka Producer Library) — must be published first
- **Independent of**: Other ingestion workers (PKG-01B, PKG-01C, PKG-01D, PKG-01E — zero code sharing)

## DoD Checklist (Tier 1)
- [ ] Code compiles, passes `go vet`, `golangci-lint`, unit tests >80% coverage
- [ ] Docker image builds, runs locally with docker-compose (mock sources + Kafka)
- [ ] K8s manifests apply to kind, HPA works, health endpoints respond
- [ ] Integration tests (TESTER) all pass in CI
- [ ] README.md with runbook, config reference, troubleshooting
- [ ] Schema registered in Schema Registry (CI step)
- [ ] Metrics exposed, scrapeable by Prometheus
- [ ] No high/critical SAST/SCA findings

---
**Task Status**: READY
**Assigned**: DEV (implementation), TESTER (integration test)
**Architecture Seam**: PKG-01 Data Ingestion Layer — Core ingestion service (independent module)
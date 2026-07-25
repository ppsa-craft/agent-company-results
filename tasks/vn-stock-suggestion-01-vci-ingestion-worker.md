# Task: vn-stock-suggestion-01-vci-ingestion-worker

## Goal
Implement the VCI Ingestion Worker — an independent module with its own config, rate limiter, VCI API client, and normalization to `RawPriceTick` events published to Kafka topic `raw.price.ticks.vn`.

## Acceptance Criteria (traceable to use cases)
- UC-ING-01: VCI worker fetches real-time price ticks from VCI API every 1 second per symbol (configurable)
- UC-ING-02: VCI worker normalizes VCI API response to canonical `RawPriceTick` schema (symbol, price, volume, timestamp, source="VCI")
- UC-ING-03: VCI worker respects per-symbol rate limit (configurable, default 1 req/sec/symbol) and global rate limit
- UC-ING-04: VCI worker publishes `RawPriceTick` events to Kafka topic `raw.price.ticks.vn` using shared Kafka producer library (PKG-01F)
- UC-ING-05: VCI worker handles VCI API errors (rate limit, 5xx, timeout) with exponential backoff and dead-letter logging
- UC-ING-06: VCI worker exposes health endpoint (`/health`) and metrics endpoint (`/metrics` Prometheus format)
- UC-ING-07: VCI worker runs as independent Kubernetes Deployment with HPA (CPU-based, min 1, max 10 replicas)
- UC-ING-08: Integration test verifies end-to-end: mocked VCI API → worker → Kafka → `RawPriceTick` schema validation

## DoD Tier
Tier 1 — Product launch: full artifact table (code, working product + tests + docs + analytics + launch readiness)

## Estimated Effort
5 dev-days (DEV implementation) + 2 test-days (TESTER integration tests)

## Assigned Agent
DEV (implementation), TESTER (integration test harness)

## Implementation Plan (for DEV)
**Architecture Seam**: PKG-01 Ingestion Layer — VCI Worker (independent module, zero code sharing with other source workers except PKG-01F shared Kafka library)

**Files/Modules to Create**:
```
vn-stock-suggestion/
└── services/
    └── ingestion-vci/
        ├── cmd/
        │   └── worker/
        │       └── main.go                 # Entry point, config loading, graceful shutdown
        ├── internal/
        │   ├── config/
        │   │   └── config.go               # VCI-specific config (API base URL, API key, rate limits, symbol list)
        │   ├── client/
        │   │   └── vci_client.go           # VCI API client with retry/backoff, request signing
        │   ├── normalizer/
        │   │   └── normalizer.go           # VCI response → RawPriceTick normalization
        │   ├── publisher/
        │   │   └── publisher.go            # Wrapper around PKG-01F Kafka producer library
        │   ├── ratelimit/
        │   │   └── ratelimiter.go          # Per-symbol + global token bucket rate limiter
        │   ├── health/
        │   │   └── health.go               # /health endpoint (liveness/readiness)
        │   └── metrics/
        │       └── metrics.go              # Prometheus metrics (requests, errors, latency, kafka produce latency)
        ├── pkg/
        │   └── schema/
        │       └── raw_price_tick.proto    # Protobuf schema for RawPriceTick (shared with PKG-01F)
        ├── configs/
        │   └── config.yaml.example         # Example config with all tunables
        ├── deploy/
        │   ├── deployment.yaml             # K8s Deployment with HPA
        │   ├── service.yaml                # K8s Service for health/metrics
        │   ├── hpa.yaml                    # HorizontalPodAutoscaler
        │   └── configmap.yaml              # ConfigMap for non-secret config
        ├── Dockerfile
        ├── go.mod / go.sum
        ├── Makefile
        └── README.md
```

**Shared Dependency**: PKG-01F Kafka Producer Library (go module `github.com/vn-stock-suggestion/kafka-producer-lib`)

**Ordered Subtask Checklist**:
1. [ ] Scaffold Go module structure (`go.mod`, directory layout, `Makefile` with `build`, `test`, `docker-build`, `deploy` targets)
2. [ ] Implement `config.go` — load from env/file, validate required fields (API key, Kafka brokers, schema registry URL)
3. [ ] Implement `ratelimiter.go` — token bucket per symbol + global, configurable rates, metrics emission
4. [ ] Implement `vci_client.go` — HTTP client with retry/backoff (max 3 retries, exponential backoff 100ms-2s), request signing per VCI API spec, timeout handling (5s connect, 10s read)
5. [ ] Implement `normalizer.go` — map VCI JSON response fields to `RawPriceTick` protobuf (symbol normalization: VCI "VNM" → canonical "VNM", price scaling, timestamp parsing to Unix ms)
6. [ ] Implement `publisher.go` — thin wrapper around PKG-01F `KafkaProducer` with topic `raw.price.ticks.vn`, schema registry integration, async produce with delivery callbacks
7. [ ] Implement `main.go` — wire config → rate limiter → client → normalizer → publisher; goroutine per symbol; graceful shutdown on SIGTERM (drain in-flight, flush producer)
8. [ ] Implement `health.go` — `/health/live` (liveness), `/health/ready` (readiness: Kafka connected, schema registry reachable), `/metrics` (Prometheus)
9. [ ] Write K8s manifests (`deployment.yaml`, `service.yaml`, `hpa.yaml`, `configmap.yaml`) with resource limits (CPU 100m/500m, Mem 128Mi/512Mi), HPA min 1/max 10 CPU 70%
10. [ ] Write `Dockerfile` (multi-stage: builder → distroless, non-root user, distroless base)
11. [ ] Write unit tests for normalizer (table-driven tests with VCI sample payloads), rate limiter (token bucket behavior), client retry logic
12. [ ] Write `README.md` with: architecture overview, config reference, local run instructions (docker-compose with mock VCI + Kafka), K8s deploy steps, health/metrics endpoints

**Integration Points**:
- Consumes: PKG-01F shared Kafka producer library (go module)
- Produces: Kafka topic `raw.price.ticks.vn` with `RawPriceTick` Avro/Protobuf schema (schema registry)
- Depends on: PKG-01H integration test harness (Testcontainers Kafka + mocked VCI API)

## Test Plan (for TESTER)
**Test Environment**: Testcontainers (Kafka + Schema Registry + mocked VCI HTTP server)

**Scenarios**:
1. **Happy Path — Single Symbol**
   - Start testcontainers Kafka + Schema Registry
   - Start mocked VCI HTTP server returning valid price tick for "VNM"
   - Start VCI worker with config for symbol "VNM", rate limit 10/sec
   - Wait 5 seconds
   - Consume from `raw.price.ticks.vn`, verify:
     - Exactly 5 messages received (1/sec × 5s)
     - Each message: valid `RawPriceTick` schema, symbol="VNM", source="VCI", price>0, volume≥0, timestamp within last 5s
   - **Expected**: PASS

2. **Happy Path — Multiple Symbols**
   - Config with symbols ["VNM", "VIC", "FPT"], rate limit 1/sec each
   - Run 3 seconds
   - Consume topic, verify 3 messages/sec (1 per symbol), each with correct symbol
   - **Expected**: PASS

3. **Rate Limit Enforcement**
   - Config: 1 symbol "VNM", rate limit 2/sec
   - Mock VCI server adds 100ms latency per request
   - Run 3 seconds
   - Verify: ~6 messages (2/sec × 3s), not more (rate limiter respected despite latency)
   - **Expected**: PASS

4. **VCI API Error Handling — 429 Rate Limited**
   - Mock VCI returns 429 with `Retry-After: 2`
   - Worker should back off 2s, then retry
   - Verify no messages lost, backoff logged, metrics `vci_rate_limited_total` incremented
   - **Expected**: PASS

5. **VCI API Error Handling — 500 Server Error**
   - Mock VCI returns 500 for 3 requests, then 200
   - Worker should retry with exponential backoff (100ms, 200ms, 400ms), then succeed
   - Verify eventual success, `vci_errors_total{code="500"}` = 3, `vci_retries_total` = 3
   - **Expected**: PASS

6. **VCI API Timeout**
   - Mock VCI delays 15s (client timeout 10s)
   - Worker should timeout, log error, back off, retry next cycle
   - Verify `vci_timeouts_total` incremented, no panic, worker continues
   - **Expected**: PASS

7. **Schema Validation — Invalid Payload**
   - Mock VCI returns malformed JSON (missing price field)
   - Worker normalizer should log error, increment `normalization_errors_total`, NOT publish to Kafka, continue next cycle
   - Consume topic → verify no message for that cycle
   - **Expected**: PASS

8. **Graceful Shutdown**
   - Start worker, send SIGTERM
   - Verify: in-flight request completes or context cancelled, Kafka producer `Flush()` called, `/health/ready` returns 503 within 5s
   - **Expected**: PASS

9. **Kubernetes Deployment Validation**
   - Apply K8s manifests to kind cluster
   - Verify: Deployment creates 1 pod, HPA created, Service exposes :8080, ConfigMap mounted
   - Scale HPA to 3 replicas → 3 pods running
   - **Expected**: PASS

10. **Metrics Exposition**
    - Scrape `/metrics` endpoint
    - Verify presence of: `vci_requests_total`, `vci_request_duration_seconds`, `vci_errors_total`, `kafka_produce_duration_seconds`, `rate_limiter_wait_duration_seconds`, `go_*`, `process_*`
    - **Expected**: PASS

**Restart Behavior**: After pod restart (OOM kill, node drain), worker reconnects to Kafka, re-registers schema, resumes polling from config symbol list — no offset commitment needed (source is external API, not Kafka consumer).

**Edge Cases**:
- Empty symbol list in config → worker starts, logs warning, idle (ready=healthy)
- Schema registry unavailable at startup → readiness fails, liveness passes, retries with backoff
- Kafka broker unavailable → producer buffers (max 10k messages), readiness fails, liveness passes

## Artifacts to Produce
- `services/ingestion-vci/` — complete Go service
- `services/ingestion-vci/deploy/*.yaml` — K8s manifests
- `services/ingestion-vci/README.md` — runbook
- Unit tests (`*_test.go`)
- Integration test (TESTER writes in `tasks/vn-stock-suggestion-08-vci-integration-test.md`)

## Dependencies
- **Blocks**: PKG-01H (Integration Test Harness needs this worker)
- **Depends on**: PKG-01F (Kafka Producer Library) — must be published first
- **Independent of**: PKG-01B, PKG-01C, PKG-01D, PKG-01E (other source workers — zero code sharing)

## DoD Checklist (Tier 1)
- [ ] Code compiles, passes `go vet`, `golangci-lint`, unit tests >80% coverage
- [ ] Docker image builds, runs locally with docker-compose (mock VCI + Kafka)
- [ ] K8s manifests apply to kind, HPA works, health endpoints respond
- [ ] Integration tests (TESTER) all pass in CI
- [ ] `README.md` with runbook, config reference, troubleshooting
- [ ] Schema registered in Schema Registry (CI step)
- [ ] Metrics exposed, scrapeable by Prometheus
- [ ] No high/critical SAST/SCA findings

---
**Task Status**: READY
**Assigned**: DEV (implementation), TESTER (integration test)
**Architecture Seam**: PKG-01 Ingestion Layer — VCI Worker (independent module)
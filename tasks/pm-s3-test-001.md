# Task: pm-s3-test-001 — S3 API Gateway Load Tests + Contract Tests

## Metadata
- **ID**: pm-s3-test-001
- **Role**: TESTER
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1-S3
- **Assignee**: tester-3
- **Depends on**: pm-s3-002 (Rate Limiting + Routing + Aggregation), pm-s3-001 (S3 Scaffold)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
S3 API Gateway: Load Testing, Circuit Breaker Validation, and S3→S4 Contract Tests

## Description
Comprehensive test suite for the S3 gateway: load testing with k6, circuit breaker behavior verification, cache effectiveness measurement, and contract tests for S4 Web UI consumption.

## Acceptance Criteria
- [ ] k6 load test: ramp to 1000 req/s, sustain 5min, p99 latency < 100ms
- [ ] Rate limit test: verify 429 responses at tier limits, headers correct (Retry-After, X-RateLimit-*)
- [ ] Circuit breaker test: induce upstream failures, verify open/half-open/closed transitions
- [ ] Cache test: verify cache hits reduce upstream calls, TTL expiration works
- [ ] Contract tests (Pact): S3 responses match S4 consumer expectations
- [ ] Failover test: S1/S2 partial degradation, gateway returns degraded responses gracefully
- [ ] Security headers test: CSP, HSTS, X-Frame-Options, Referrer-Policy present

## Verification
- k6 results uploaded as CI artifacts with trend comparison
- Pact verification results published to broker
- All tests pass in CI pipeline

## Security Notes
- Test with invalid JWTs, expired tokens, malformed requests
- Verify no sensitive data in error responses
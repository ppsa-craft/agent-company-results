# Task T-139-03: M2T Contract Tests

## Goal
Build and maintain the M2 contract test suite (m2-contract-tests) that validates M2A Indicators API and M2B Pipeline internal API against their OpenAPI specifications. Runs in parallel with M3T contract tests. Blocks TECHLEAD contract review gate (T-139-11).

## Acceptance Criteria (Traceable to Contract Gates)
- [ ] **CT-M2A-01**: M2A `/indicators/calculate` request/response matches `contracts/m2-indicators.yaml` exactly (schema, enums, required fields)
- [ ] **CT-M2A-02**: All 7 indicators (SMA, EMA, RSI, MACD, BB, ATR, Stoch) return correct output shape for valid input
- [ ] **CT-M2A-03**: Invalid requests (missing fields, out-of-range params, unknown indicators) return 422 with RFC 7807 error structure
- [ ] **CT-M2A-04**: Batch request (multiple symbols, multiple indicators) response structure matches spec (nested by symbol then indicator)
- [ ] **CT-M2A-05**: Response latency header `X-Calc-Latency-Ms` present and accurate
- [ ] **CT-M2B-01**: M2B internal API `/health` response matches `contracts/m2-pipeline.yaml`
- [ ] **CT-M2B-02**: M2B `/metrics` exposes Prometheus format with required labels (pipeline_lag_ms, throughput_msg_s, dlq_size)
- [ ] **CT-M2B-03**: M2B `POST /backfill` request/response schema validated
- [ ] **CT-CROSS-01**: M2A → M2B contract compatibility: M2B client sends requests matching M2A server expectations
- [ ] **CT-GATE-01**: Contract test suite runs in CI, fails build on any schema mismatch
- [ ] **CT-GATE-02**: Contract tests packaged as reusable pytest plugin for DEV local runs

## Estimated Effort
- **Effort**: 2 cycles (Cycle 139-140)
- **DoD Tier**: Tier 2 (Feature: contract tests + docs + CI integration)

## Assigned Agent
- **Role**: TESTER
- **Agent**: tester-1
- **Cycle**: 139
- **Status**: READY

## File Ownership (Disjoint Boundary: `tests/contract/m2/`)
```
workspace/apps/tech-analysis/tests/contract/m2/
├── __init__.py
├── conftest.py                 # Fixtures: M2A client, M2B client, schema validators
├── schemas/
│   ├── m2-indicators.yaml      # Copied from m2-indicators service at build time
│   └── m2-pipeline.yaml        # Copied from m2-pipeline service at build time
├── test_m2a_contract.py        # M2A Indicators API contract tests
├── test_m2b_contract.py        # M2B Pipeline API contract tests
├── test_cross_contract.py      # M2A→M2B compatibility tests
├── test_ci_gate.py             # CI gate enforcement tests
├── fixtures/
│   ├── valid_indicator_request.json
│   ├── invalid_requests.json
│   ├── expected_responses/
│   │   ├── sma_response.json
│   │   ├── rsi_response.json
│   │   ├── macd_response.json
│   │   ├── bb_response.json
│   │   ├── atr_response.json
│   │   └── stoch_response.json
│   └── batch_request.json
├── plugin/
│   ├── __init__.py
│   └── contract_plugin.py      # Pytest plugin for local DEV runs
├── pyproject.toml
├── README.md
└── Dockerfile
```

## Implementation Plan (for TESTER)

**Architecture Seam**: `tests/contract/m2/` — completely independent of M2 implementation code. Consumes published OpenAPI specs only. Runs in parallel with `tests/contract/m3/` (T-139-08).

**Tech Stack**:
- Python 3.11, pytest, requests, jsonschema, openapi-spec-validator
- schemathesis for property-based contract testing (optional but recommended)
- pytest plugin for local developer experience

**Ordered Subtask Checklist**:
1. [ ] Scaffold test package structure
2. [ ] Write `conftest.py` with fixtures: `m2a_client`, `m2b_client`, `indicator_schema`, `pipeline_schema`
3. [ ] Implement schema loading from `contracts/` dir (copied at build via CI)
4. [ ] Write `test_m2a_contract.py`:
    - Parametrized test per indicator (7 indicators × valid/invalid/edge cases)
    - Batch request test (multi-symbol, multi-indicator)
    - Error response structure validation (RFC 7807)
    - Latency header presence/accuracy
5. [ ] Write `test_m2b_contract.py`:
    - Health endpoint schema
    - Metrics format validation (Prometheus text format + required metrics)
    - Backfill trigger schema
6. [ ] Write `test_cross_contract.py`:
    - Generate M2A request from M2B client code → validate against M2A schema
    - Simulate M2B→M2A call flow with recorded responses
7. [ ] Write `test_ci_gate.py`:
    - Test that contract test failure exits non-zero
    - Test that schema drift detection works (modify schema → test fails)
8. [ ] Build pytest plugin `contract_plugin.py`:
    - `pytest --contract=m2` runs M2 suite
    - Auto-discovers schemas from `contracts/`
    - Pretty diff output on mismatch
9. [ ] Create fixture data: valid/invalid requests, expected responses for each indicator
10. [ ] Configure CI (GitHub Actions): run contract tests on every PR, block merge on failure
11. [ ] Document local usage in README.md (`pytest tests/contract/m2/ --contract=m2`)

**Dependencies**: Requires M2A OpenAPI contract (T-139-01 output) and M2B contract (T-139-02 output). Can start writing tests against draft schemas in parallel.

## Test Plan (for TESTER — self-test)

**Contract Test Scenarios** (these ARE the tests being built):
1. **M2A Happy Path**: Each indicator with valid input → response matches schema exactly
2. **M2A Invalid Input**: Missing symbol, unknown indicator, period < 1, period > 500 → 422 RFC 7807
3. **M2A Batch**: 10 symbols × 5 indicators → response structure correct
4. **M2A Edge Cases**: NaN handling, flat prices, single bar → schema still valid
5. **M2B Health**: `/health` returns `{status, lag_ms, throughput, dlq_size}` matching schema
6. **M2B Metrics**: `/metrics` text format parsable, contains required metric names with labels
7. **M2B Backfill**: Request/response schemas match
8. **Cross-contract**: M2B client generates request → validates against M2A server schema
9. **CI Gate**: Introduce breaking change in schema → test fails → CI blocks

**Edge Cases for Test Suite Itself**:
1. Schema file missing at runtime → clear error message
2. Service unavailable during test → test marked `xfailed` with reason, not error
3. Schema version mismatch (spec version vs implementation) → detected

**Expected Results**: All contract tests pass against current implementations. CI gate blocks PRs with schema drift. Plugin works locally for DEV.

## DoD Tier 2 Checklist
- [ ] All contract tests implemented and passing
- [ ] Pytest plugin functional locally
- [ ] CI integration complete (blocks merge on failure)
- [ ] README with usage instructions
- [ ] Fixture data complete for all 7 indicators
- [ ] Cross-contract compatibility validated
- [ ] No file overlap with M3T contract tests (disjoint `tests/contract/m3/`)
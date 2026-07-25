# Task: S1 Data Ingestion - Integration Testing

- **ID**: pm-s1-test-001
- **Role**: TESTER
- **App**: `vn-stock-suggestion`
- **Milestone**: M1-S1
- **Assignee**: tester-1
- **Depends on**: pm-s1-001, pm-s1-002
- **Status**: ready
- **DoD Tier**: 2 (feature)

## Acceptance Criteria
- [ ] Health endpoint returns correct response
- [ ] Pydantic schemas validate valid price data
- [ ] Pydantic schemas reject invalid data
- [ ] Dockerfile builds without errors
- [ ] CI pipeline runs successfully

## Test Plan
1. Health endpoint test: GET /health → 200, {"status": "healthy"}
2. Schema validation: Post valid PriceData → validates
3. Schema rejection: Post negative price → validation error
4. Schema rejection: Post future timestamp → validation error
5. Docker build: `docker build -t s1 .` succeeds
6. README instructions work verbatim

## Architecture Seam
S1 internal — tests verify S1's API and data contracts.

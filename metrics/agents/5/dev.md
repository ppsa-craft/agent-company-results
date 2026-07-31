# dev — cycle 5 lane log

```
)

- [ ] Service runs in `workspace/apps/vnstock-advisor/services/data-ingest/`
- [ ] Fetches from primary source (per BA recommendation) + fallback
- [ ] Normalizes to `market_data` schema (per BA doc)
- [ ] Idempotent upsert: re-ingest same date/symbol → no duplicates
- [ ] APScheduler cron job (configurable, default 15:30 VN time on trading days)
- [ ] Manual trigger endpoint: `POST /ingest/run`
- [ ] Health endpoint: `GET /ingest/health` → `{status, last_run, next_run, errors}`
- [ ] Structured logging (structlog) + error tracking
- [ ] Unit tests: normalization, upsert idempotency, scheduler logic
- [ ] Integration test: full ingest against test DB
- [ ] Security: SAST clean (Semgrep), SCA clean (Snyk), secret-scan clean (Gitleaks), input validation (Pydantic on all external responses)
- [ ] README with local run instructions

---

## Implementation Plan (for DEV)

**Architecture seam:** Owns `data-ingest` service only. Interfaces: writes to `market_data` table, exposes `/ingest/health` and `/ingest/run`. No other service writes to `market_data`.

1. Set up FastAPI project in `services/data-ingest/` (per monorepo structure)
2. Implement HTTP client with allowlisted URLs, timeout, retry (httpx)
3. Implement source-specific parsers (primary + fallback) → canonical Pydantic model
4. Implement SQLAlchemy upsert with `ON CONFLICT (symbol, timestamp) DO UPDATE`
5. Implement APScheduler job with trading-day calendar (VN holidays)
6. Implement FastAPI endpoints with Pydantic request/response models
7. Add structlog configuration
8. Write tests (pytest + pytest-asyncio)
9. Verify CI passes (ruff, mypy, pytest)

---

## Test Plan (for TESTER)

**Scenario 1: Scheduled ingest runs**
- Steps: Trigger `/ingest/run`, check `market_data` table
- Expected: Rows inserted with correct schema, `ingested_at` populated

**Scenario 2: Idempotent upsert**
- Steps: Run ingest twice for same symbol/date
- Expected: Row count unchanged, values updated if source changed

**Scenario 3: Fallback source**
- Steps: Mock primary source failure, verify fallback used
- Expected: Data from fallback source inserted, logged

**Scenario 4: Health endpoint**
- Steps: Call `GET /ingest/health`
- Expected: Returns status, last_run, next_run, errors (empty if none)

**Scenario 5: Security gate**
- Steps: Run Semgrep, Snyk, Gitleaks on service
- Expected: No high/critical findings

---

## Dependencies

- `vnstock-advisor-1-repo-scaffold` (monorepo, docker-compose, shared/python models)
- `vnstock-advisor-2-ba-data-ingest` (schema, source choice, use cases)
- `vnstock-advisor-3-ba-analysis-engine` (indicator specs, fixture data)
- `workspace/apps/vnstock-advisor/services/data-ingest/src/requirements.txt` (deps added)
- `workspace/apps/vnstock-advisor/services/analysis-engine/src/requirements.txt` (deps added)
[0m
timestamp=2026-07-31T12:56:54.636Z level=INFO run=87b0ce43 message=loop session.id=ses_047c78f36fferCuDWx8l6feSuj step=39
timestamp=2026-07-31T12:56:54.668Z level=INFO run=87b0ce43 message=process session.id=ses_047c78f36fferCuDWx8l6feSuj messageID=msg_fb83fc477001paHhSVXA0RQhry
timestamp=2026-07-31T12:56:54.672Z level=INFO run=87b0ce43 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_047c78f36fferCuDWx8l6feSuj small=false agent=build mode=primary
timestamp=2026-07-31T12:56:54.683Z level=INFO run=87b0ce43 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-07-31T12:57:06.707Z level=INFO run=87b0ce43 message=loop session.id=ses_047c78f36fferCuDWx8l6feSuj step=40
timestamp=2026-07-31T12:57:06.720Z level=INFO run=87b0ce43 message="exiting loop" session.id=ses_047c78f36fferCuDWx8l6feSuj
**vnstock-advisor-4-dev-data-ingest Complete: Data Ingest Service Implementation**
timestamp=2026-07-31T12:57:06.747Z level=INFO run=87b0ce43 message="disposing instance" directory=/data
timestamp=2026-07-31T12:57:06.851Z level=INFO run=87b0ce43 message=loading path=/data/opencode.json

```

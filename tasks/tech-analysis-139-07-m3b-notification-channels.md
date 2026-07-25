# Task T-139-07: M3B Notification Channels

## Goal
Implement notification delivery channels (Email, Slack, Webhook, Push, SMS) for M3 Alerting. Consumes `alerts.raw` Kafka topic, applies routing rules, delivers via configured channels with retry/DLQ. Sequential after M2B (DEV-2 chain).

## Acceptance Criteria (Traceable to Use Cases)
- [ ] **UC-M3B-01**: Channel registry — CRUD for channel configs (type, credentials, templates, rate limits)
- [ ] **UC-M3B-02**: Email channel — SMTP/SendGrid, HTML + text templates, attachment support, unsubscribe header
- [ ] **UC-M3B-03**: Slack channel — Bot token, block kit formatting, thread replies, channel/DM routing
- [ ] **UC-M3B-04**: Webhook channel — HMAC-signed payload, custom headers, retry policy (3x exp backoff), timeout config
- [ ] **UC-M3B-05**: Push channel — FCM/APNs, device token management, collapse key for deduplication
- [ ] **UC-M3B-06**: SMS channel — Twilio/Vonage, template variables, opt-out handling, rate limit compliance
- [ ] **UC-M3B-07**: Routing engine — match alert to channels via rules (severity, symbol, tags, user prefs)
- [ ] **UC-M3B-08**: Delivery pipeline — consume `alerts.raw`, route, render template, send, track status
- [ ] **UC-M3B-09**: Retry & DLQ — per-channel retry (configurable), dead-letter to `alerts.dlq` after exhaustion
- [ ] **UC-M3B-10**: Idempotency — alert_id + channel_id unique constraint, exactly-once delivery semantics
- [ ] **UC-M3B-11**: Observability — `/metrics` with delivery_latency_ms, success_rate, retry_count, dlq_size per channel
- [ ] **UC-M3B-12**: OpenAPI contract at `/contracts/m3-channels.yaml`

## Estimated Effort
- **Effort**: 3 cycles (Cycle 140-142) — starts AFTER T-139-02 completes
- **DoD Tier**: Tier 2

## Assigned Agent
- **Role**: DEV
- **Agent**: dev-2
- **Cycle**: 139 (READY, blocked on T-139-02)
- **Status**: READY

## File Ownership (Disjoint Boundary: `services/m3-alerts/src/channels/`)
```
workspace/apps/tech-analysis/services/m3-alerts/
├── src/
│   ├── channels/
│   │   ├── __init__.py
│   │   ├── registry/
│   │   │   ├── __init__.py
│   │   │   ├── store.py              # PostgreSQL channel configs
│   │   │   ├── models.py             # ChannelConfig, Credential (encrypted)
│   │   │   └── validator.py          # Credential validation per type
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Abstract NotificationProvider
│   │   │   ├── email.py              # SendGrid/SMTP
│   │   │   ├── slack.py              # Slack SDK
│   │   │   ├── webhook.py            # aiohttp + HMAC
│   │   │   ├── push.py               # FCM/APNs
│   │   │   └── sms.py                # Twilio
│   │   ├── routing/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py             # Rule evaluation → channel list
│   │   │   ├── models.py             # RoutingRule, UserPreference
│   │   │   └── matcher.py            # Alert → channels matching
│   │   ├── pipeline/
│   │   │   ├── __init__.py
│   │   │   ├── consumer.py           # Kafka consumer alerts.raw
│   │   │   ├── renderer.py           # Jinja2 templates per channel
│   │   │   ├── dispatcher.py         # Parallel send with semaphore
│   │   │   ├── retry.py              # Retry policy, backoff, DLQ
│   │   │   └── idempotency.py        # Redis SETNX alert_id:channel_id
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py             # Channel CRUD, test send, delivery history
│   │   │   ├── schemas.py
│   │   │   └── dependencies.py
│   │   └── metrics.py                # Prometheus metrics
│   ├── main.py                       # Shared FastAPI app (rules + channels)
│   └── config.py
├── tests/
│   ├── unit/
│   │   ├── test_providers.py
│   │   ├── test_routing.py
│   │   ├── test_renderer.py
│   │   └── test_idempotency.py
│   ├── integration/
│   │   ├── test_delivery_e2e.py
│   │   └── test_retry_dlq.py
│   └── fixtures/
│       ├── alert_samples.json
│       └── channel_configs.json
├── contracts/
│   └── m3-channels.yaml
├── pyproject.toml
├── README.md
└── Dockerfile
```

## Implementation Plan (for DEV)

**Architecture Seam**: `services/m3-alerts/src/channels/` — disjoint from `rules/` (T-139-06). Shared FastAPI app but separate modules. Consumes M3A output via Kafka.

**Tech Stack**:
- Python 3.11, FastAPI, aiokafka, aiohttp, jinja2, redis, asyncpg
- Provider SDKs: sendgrid, slack-sdk, firebase-admin, twilio
- Pytest, testcontainers, fakeredis

**Ordered Subtask Checklist**:
1. [ ] Scaffold channel module structure (extends existing m3-alerts service)
2. [ ] Implement `registry/store.py` — channel config CRUD, credential encryption (Fernet)
3. [ ] Implement `registry/validator.py` — test connection per provider type
4. [ ] Implement `providers/base.py` — `NotificationProvider` ABC: `send(alert, config) -> DeliveryResult`
5. [ ] Implement `providers/email.py` — SendGrid API, template rendering, tracking pixel
6. [ ] Implement `providers/slack.py` — Block Kit builder, thread_ts for grouping
7. [ ] Implement `providers/webhook.py` — HMAC-SHA256 signature, custom headers, timeout
8. [ ] Implement `providers/push.py` — FCM (Android) + APNs (iOS), collapse_key
9. [ ] Implement `providers/sms.py` — Twilio, STOP handling, rate limit awareness
10. [ ] Implement `routing/engine.py` — rule DSL (CEL or simple JSONLogic), user preference merge
11. [ ] Implement `pipeline/consumer.py` — Kafka consumer group, batch processing
12. [ ] Implement `pipeline/renderer.py` — Jinja2 env per channel, auto-escape, fallback text
13. [ ] Implement `pipeline/dispatcher.py` — semaphore (max 50 concurrent), per-provider error isolation
14. [ ] Implement `pipeline/retry.py` — exponential backoff (10s, 1m, 10m), max 3, then DLQ
15. [ ] Implement `pipeline/idempotency.py` — Redis `SETNX alert_id:channel_id` with 24h TTL
16. [ ] API routes: channel CRUD, `POST /channels/{id}/test`, `GET /deliveries?alert_id=`
17. [ ] Write OpenAPI contract `contracts/m3-channels.yaml`
18. [ ] Unit tests: each provider (mocked), routing engine, renderer, idempotency
19. [ ] Integration tests: testcontainers (Kafka, Redis, Postgres) — full delivery flow
20. [ ] Retry/DLQ test: force provider failure → verify retries → verify DLQ message
21. [ ] Performance: 1000 alerts/sec → p99 delivery < 5s
22. [ ] README with channel setup guide, template examples
23. [ ] Update analytics (delivery_latency_ms, success_rate, dlq_by_channel)

**Dependencies**: Requires M2B enriched Kafka topic (T-139-02). M3A rules (T-139-06) produce to `alerts.raw` consumed here.

## Test Plan (for TESTER)

**Happy Path**:
1. **Email delivery**: Alert triggered → routed to email channel → SendGrid API called → 202 accepted → delivery recorded
2. **Slack formatting**: Alert with multiple indicators → Block Kit message with sections, fields, color → posted to channel
3. **Webhook HMAC**: Payload signed → receiver verifies signature → 200 OK
4. **Multi-channel routing**: Alert matches 3 rules → delivered to Email + Slack + Webhook in parallel
5. **Template rendering**: Jinja2 template with `{{symbol}}`, `{{indicator}}`, `{{value}}` → variables substituted

**Edge Cases**:
1. **Provider failure**: SendGrid 500 → retry 3x → DLQ → alert in `alerts.dlq` with error context
2. **Rate limit**: Slack 429 → respect `Retry-After` → retry after delay
3. **Invalid template**: Jinja2 syntax error → caught at channel config validation (UC-M3B-01)
4. **Duplicate alert**: Same alert_id retried → idempotency key blocks second delivery
5. **Missing credentials**: Channel config without API key → validation error on create
6. **Large payload**: Alert with 50 indicators → webhook payload > 1MB → truncate or chunk (config)

**Restart Behavior**:
1. Consumer rebalance → no duplicate deliveries (idempotency key in Redis)
2. Redis restart → keys lost but 24h TTL acceptable (alerts expire)
3. Provider outage → messages accumulate in consumer lag, drain when restored

**Expected Results**: All channels deliver correctly formatted notifications. Metrics exposed. DLQ captures failures with full context. Idempotency holds under restart.

## DoD Tier 2 Checklist
- [ ] All 12 UCs implemented and tested
- [ ] Unit test coverage ≥ 85%
- [ ] Integration tests pass (testcontainers)
- [ ] Retry/DLQ verified end-to-end
- [ ] Idempotency verified under restart
- [ ] Performance test: 1k alerts/s, p99 < 5s
- [ ] OpenAPI contract published
- [ ] README with setup for all 5 channels
- [ ] Analytics events defined
- [ ] Code review approved
- [ ] Security gate passed
- [ ] Changelog entry
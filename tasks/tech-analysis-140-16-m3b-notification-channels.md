# Task: tech-analysis-140-16-m3b-notification-channels

**Task ID**: T-140-16
**Title**: M3B Notification Channels — email, webhook, push (DEV-2)
**Role**: DEV
**Status**: READY
**Assigned Agent**: dev-2
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature

## File Ownership (Architecture Seam: M3B Notification Service)
- `workspace/apps/tech-analysis/services/m3b-notifications/**`
- `workspace/apps/tech-analysis/tests/unit/m3b-notifications/**`
- `workspace/apps/tech-analysis/tests/integration/m3b-notifications/**`

## Goal
Implement M3B Notification Channels Service: consumes AlertEvent from NATS `alerts.fired.*`, delivers via Email (SMTP/SendGrid), Webhook (HTTP POST with retry/backoff), Push (FCM/APNs via provider). Template engine for alert formatting. Delivery tracking with status (pending, sent, failed, acked).

## Acceptance Criteria (trace to M3B-UC specs T-140-18)
| AC | Trace |
|----|-------|
| NATS consumer: subscribes `alerts.fired.>` | UC-M3B-01 |
| Email channel: SendGrid/SMTP, HTML + text templates | UC-M3B-02 |
| Webhook channel: POST with signature, retry exp backoff | UC-M3B-03 |
| Push channel: FCM/APNs via provider, device token management | UC-M3B-04 |
| Template engine: Handlebars, variables: {{symbol}}, {{rule}}, {{value}} | UC-M3B-05 |
| Delivery tracking: status, attempts, lastError, sentAt | UC-M3B-06 |
| Deduplication: same alertId+channel not resent | UC-M3B-07 |
| Dead letter: max retries exceeded → DLQ topic | UC-M3B-08 |
| gRPC/HTTP: manage subscriptions (channel, filter, template) | UC-M3B-09 |
| Metrics: deliveries, latency, failures per channel | UC-M3B-10 |

## Implementation Plan (for DEV-2)
**Architecture Seam**: M3B Notification Service — `services/m3b-notifications/`

### Files/Modules
1. `src/service.ts` — main service, NATS consumer, DI
2. `src/config.ts` — Zod config (SMTP, SendGrid, FCM, webhook defaults)
3. `src/nats/consumer.ts` — JetStream consumer for `alerts.fired.>`
4. `src/channels/email.ts` — EmailChannel (nodemailer + SendGrid)
5. `src/channels/webhook.ts` — WebhookChannel (axios + retry + signature)
6. `src/channels/push.ts` — PushChannel (firebase-admin for FCM)
7. `src/templates/engine.ts` — Handlebars engine, built-in templates
8. `src/templates/builtin.ts` — default alert templates
9. `src/storage/deliveries.ts` — PostgreSQL delivery tracking
10. `src/storage/subscriptions.ts` — subscription management
11. `src/grpc/notifications.proto` — gRPC service
12. `src/http/routes/subscriptions.ts` — HTTP CRUD for subscriptions
12. `src/metrics/delivery.ts` — Prometheus metrics
13. `tests/unit/channels/*.test.ts` — channel unit tests
14. `tests/integration/notifications.test.ts` — integration test

### Ordered Subtasks
- [ ] Scaffold service structure
- [ ] Implement NATS consumer with JetStream ack
- [ ] Implement Email channel (SMTP + SendGrid)
- [ ] Implement Webhook channel (retry, signature, timeout)
- [ ] Implement Push channel (FCM)
- [ ] Implement Template engine with built-ins
- [ ] Implement Delivery tracking (PostgreSQL)
- [ ] Implement Subscription management (gRPC + HTTP)
- [ ] Add deduplication (Redis set on alertId+channel)
- [ ] Add Dead Letter Queue (NATS `alerts.dlq`)
- [ ] Add metrics
- [ ] Unit tests for channels and templates
- [ ] Integration test with NATS test container
- [ ] README with run instructions

## Test Plan (for TESTER - T-140-17)
See T-140-17 for detailed scenarios per UC.

## DoD Tier 2 Checklist
- [ ] All ACs implemented and tested
- [ ] Unit tests ≥80% coverage on channels
- [ ] Integration test passes
- [ ] BA specs reviewed (T-140-18)
- [ ] TECHLEAD contract review passed (T-140-19)
- [ ] QA security gate passed (T-140-20)
- [ ] README works in clean checkout
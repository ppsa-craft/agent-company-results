# Task: techlead-001 — Interface Contracts + Threat Models (All 4 Services)

## Metadata
- **ID**: techlead-001
- **Role**: TECHLEAD
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1
- **Assignee**: techlead
- **Depends on**: cto-001 (Stack Decision)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/stack-vn-stock-suggestion.md

## Title
Produce Interface Contracts and Threat Models for S1↔S2, S2↔S3, S3↔S4 Service Boundaries

## Description
Define and document the formal contracts between all services. Create threat models using MITRE ATT&CK for each service boundary. These artifacts gate DEV implementation and QA security reviews.

## Acceptance Criteria
- [ ] **S1→S2 Contract**: Redis stream schema (Avro/JSON) for `PriceData` events, consumer group semantics, schema evolution policy
- [ ] **S2→S3 Contract**: Signal event schema (REST + WebSocket), authentication requirements, rate limit headers
- [ ] **S3→S4 Contract**: OpenAPI 3.1 spec for REST endpoints, WebSocket message formats, auth flow specification
- [ ] **JWT Auth Contract**: Token claims, expiration, refresh flow, scopes per service
- [ ] **Threat Model - S1**: External API ingestion risks (SSRF, injection, auth bypass), mitigations
- [ ] **Threat Model - S2**: Signal manipulation, data poisoning, DoS via computation
- [ ] **Threat Model - S3**: Gateway bypass, rate limit evasion, cache poisoning, auth confusion
- [ ] **Threat Model - S4**: XSS via WebSocket, token theft, CSRF, clickjacking
- [ ] **Security Checklists**: Per-service OWASP Top 10 mapping, gate criteria for QA
- [ ] All contracts versioned, published to shared location, reviewed by CTO + BA

## Verification
- Contracts validated against actual implementation (Pact/Semgrep)
- Threat models reviewed in security gate (QA)
- CTO sign-off on contract stability

## Security Notes
- Contracts include security requirements (encryption, auth, validation)
- Threat models use MITRE ATT&CK framework
- Security gate checklist items derived from threat models
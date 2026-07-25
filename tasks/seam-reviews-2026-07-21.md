# SEAM REVIEW RECORDS — 2026-07-21 Emergency Idle Cycle
## CTO Emergency Idle Cycle — Top 5 Candidate Service Architectures

> **Source**: `debates/emergency-idle-2026-07-21.md` (CTO architecture output appended)
> **Purpose**: TECHLEAD pre-loads SEAM REVIEW templates so PM/DEV/TESTER can fill them in parallel during the cycle.
> **Owner**: TECHLEAD (writes template only — PM/DEV/TESTER fill, TECHLEAD reviews, QA gates)
> **Gate**: No service merges without a filled + TECHLEAD-approved SEAM REVIEW record.

---

## TEMPLATE DEFINITION (apply to each of the 5 services)

For each service below, PM/DEV/TESTER fill **Sections 1–6**. TECHLEAD reviews and signs `APPROVED` or `BLOCKED` per round (max 3 rounds, then CTO escalation).

---

### SECTION 1 — Service Identity & Interface Signature

| Field | Value (PM/DEV fill) |
|-------|---------------------|
| **Service Name** | `<svc-name>` |
| **Repo Path** | `apps/<slug>/` |
| **Protocol** | `REST` / `gRPC` / `GraphQL` / `Async (Kafka/NATS)` / `MCP` / `Other: ______` |
| **Base Path / Service Name** | `/api/v1/<resource>` / `<service-name>` / `<topic>` |
| **Auth Scheme** | `JWT (RS256)` / `mTLS` / `API Key` / `OAuth2 Client Credentials` / `mTLS + SPIFFE` / `None (internal mesh)` |
| **Input Contract** | OpenAPI / Protobuf / GraphQL SDL / AsyncAPI / JSON Schema — link or inline schema ref |
| **Output Contract** | Same as input contract (responses) + error envelope schema |
| **Error Envelope** | `{ "error": { "code": "ERR_CODE", "message": "human", "details": {} } }` / RFC 7807 / gRPC status / custom |
| **Idempotency** | `Idempotency-Key` header required / idempotency key in body / natural idempotency / none |
| **Pagination / Streaming** | Cursor / Offset / Keyset / Server-Sent Events / WebSocket / gRPC streaming |
| **Rate Limit** | `X-RateLimit-Limit/Remaining/Reset` headers / token bucket / none (mesh) |
| **Versioning** | URL version (`/v1/`) / Header (`Accept: application/vnd.x.v1+json`) / Package version |

---

### SECTION 2 — Data Dependencies (Reads / Writes / External)

| Dimension | Detail (DEV fills) |
|-----------|---------------------|
| **Primary Datastore** | `PostgreSQL` / `MongoDB` / `Redis` / `Cassandra` / `DynamoDB` / `SQLite` / `None` |
| **Schema Owner** | This service / Shared (name) / External (owner) |
| **Schema Migration Tool** | `golang-migrate` / `Flyway` / `Alembic` / `Prisma Migrate` / `Atlas` / `None (manual)` |
| **Read Models / Replicas** | Primary only / Read replicas (count) / Materialized views / CDC / CDC → Kafka |
| **Write Patterns** | OLTP / Event sourcing / CQRS / Append-only / Batch |
| **External Read Dependencies** | Service / API / DB (name, contract, SLA, fallback) |
| **External Write Dependencies** | Service / API / Message bus / Webhook (name, contract, idempotency, retry policy) |
| **Event Bus** | `Kafka` / `NATS` / `Redis Streams` / `RabbitMQ` / `EventBridge` / `None` |
| **Published Events** | Topic / Schema (Avro/Protobuf/JSON Schema) / Ordering guarantees / Retention |
| **Consumed Events** | Topic / Consumer group / Ordering / Idempotency key / DLQ config |
| **Cache Layer** | `Redis` / `Memcached` / `Valkey` / `In-memory` / `CDN` / `None` — TTL / Invalidation strategy |
| **Secrets / Config Source** | `Vault` / `AWS Secrets Manager` / `1Password` / `SOPS` / `Dotenv (dev only)` / `ConfigMap` |
| **Blob / Object Storage** | `S3` / `GCS` / `R2` / `MinIO` / `Azure Blob` / `None` — Bucket / Prefix / Lifecycle |
| **Search / Analytics** | `Elasticsearch` / `OpenSearch` / `MeiliSearch` / `Typesense` / `ClickHouse` / `BigQuery` / `None` |
| **Backup / DR** | RPO / RPO target / Point-in-time recovery tested? (Y/N) / Last drill date |

---

### SECTION 3 — Security Surface Checklist (TECHLEAD + Security Auditor persona)

| Control | Required? | Implementation (DEV fills) | Verified? (TECHLEAD) |
|---------|-----------|----------------------------|----------------------|
| **Input Validation** | ✅ Required | Schema validation library / location | ☐ |
| **Output Encoding** | ✅ Required | Context-aware encoding (HTML/JS/JSON/SQL/Shell) | ☐ |
| **Authentication** | ✅ Required | JWT RS256 / mTLS / API Key / OIDC / SPIFFE / None (mesh) | ☐ |
| **Authorization** | ✅ Required | RBAC / ABAC / ReBAC / OPA / Casbin / Custom / None (mesh) | ☐ |
| **Secrets Management** | ✅ Required | Vault / AWS SM / 1Password / SOPS / Env (dev only) — **no hardcoded secrets** | ☐ |
| **Secret Scanning** | ✅ Required | `gitleaks` pre-commit + CI / `trufflehog` / `git-secrets` | ☐ |
| **Crypto** | ✅ Required | TLS 1.3 only / AES-GCM / ChaCha20-Poly1305 / RSA-PSS / Ed25519 / HKDF / **No custom crypto** | ☐ |
| **TLS / mTLS** | ✅ Required (external) / Mesh (internal) | `cert-manager` / `spire` / `istio` / `linkerd` / `cert-manager` + `cert-manager-istio` | ☐ |
| **Security Headers** | ✅ Required (HTTP) | `CSP` / `HSTS` / `X-Frame-Options` / `X-Content-Type-Options` / `Referrer-Policy` / `Permissions-Policy` / `Cross-Origin-Opener-Policy` / `Cross-Origin-Resource-Policy` | ☐ |
| **CORS** | ✅ Required (HTTP) | Explicit allow-list / No wildcard with credentials / Preflight caching | ☐ |
| **Rate Limiting** | ✅ Required (external) | Token bucket / Sliding window / Distributed (Redis) / Per-tenant / Per-IP | ☐ |
| **Request Size Limits** | ✅ Required | Body limit / Header limit / Timeout | ☐ |
| **Audit Logging** | ✅ Required (audit-relevant) | Structured JSON / Immutable store / Tamper-evident / Retention | ☐ |
| **Secret Rotation** | ✅ Required | Rotation schedule / Automated / Manual process documented | ☐ |
| **Dependency Scanning (SCA)** | ✅ Required | `snyk` / `trivy` / `grype` / `osv-scanner` / `dependency-check` in CI | ☐ |
| **SAST** | ✅ Required | `semgrep` (custom rules) / `codeql` / `sonarqube` / `golangci-lint` / `bandit` / `eslint-security` | ☐ |
| **Container Hardening** | ✅ Required (container) | `distroless` / `scratch` / `gvisor` / `kata` / Non-root / Read-only FS / Drop caps / Seccomp | ☐ |
| **SBOM Generation** | ✅ Required | `syft` / `trivy` / `cyclonedx` / `spdx` in CI — SBOM artifact published | ☐ |
| **Penetration Test** | Tier 1/2 required | OWASP WSTG / API Top 10 / Scheduled / Last report date | ☐ |

---

### SECTION 4 — SAST / SCA / Secret-Scan Tooling for This Stack

| Category | Tool (DEV/TECHLEAD pick per stack) | CI Stage | Config Location | Gate Threshold |
|----------|------------------------------------|----------|-----------------|----------------|
| **SAST** | `semgrep` (custom rules) / `codeql` / `golangci-lint` / `eslint-security` / `bandit` / `semgrep-ruleset-owasp` | PR / PR + Nightly | `.github/workflows/sast.yml` / `.semgrep.yml` | **Block on High/Critical** |
| **SCA** | `snyk` / `trivy` / `grype` / `osv-scanner` / `dependency-check` / `renovate` (auto-PR) | PR / Daily / Release | `.github/workflows/sca.yml` / `.snyk` / `renovate.json` | **Block on Critical / High (CVSS ≥ 7)** |
| **Secret Scan** | `gitleaks` / `trufflehog` / `git-secrets` / `ggshield` | Pre-commit / PR / Nightly / History scan | `.gitleaks.toml` / `.github/workflows/secrets.yml` | **Block on any secret** |
| **Container Scan** | `trivy` / `grype` / `syft` / `docker scout` | PR (image build) / Nightly | `.github/workflows/container-scan.yml` | **Block on Critical / High (CVSS ≥ 7)** |
| **SBOM** | `syft` / `trivy sbom` / `cyclonedx` / `spdx` | Release build | `.github/workflows/sbom.yml` | **Artifact published** |
| **License Check** | `fossa` / `clearlydefined` / `license-checker` / `ort` | PR / Release | `.github/workflows/license.yml` | **Block on prohibited licenses** |
| **Custom Rules** | `semgrep` custom ruleset path | PR | `.semgrep/custom-rules.yml` | **Block on custom critical rules** |

> **Stack-specific notes (DEV fills per service):**
> - Language/runtime: `Go 1.22` / `Node 22` / `Python 3.12` / `Java 21` / `Rust 1.79` / `TypeScript 5` / `Other`
> - Framework: `Gin` / `Echo` / `FastAPI` / `Fastify` / `Spring Boot 3` / `Axum` / `Hono` / `Next.js` / `Remix` / `Other`
> - ORM/DB driver: `sqlx` / `gorm` / `sqlc` / `Prisma` / `Drizzle` / `Hibernate` / `Diesel` / `sqlalchemy` / `None`
> - Test framework: `testify` / `jest` / `pytest` / `junit5` / `cargo test` / `vitest` / `playwright` / `k6`

---

### SECTION 5 — Parallelism Assessment (PM + TECHLEAD)

| Question | Answer (PM/TECHLEAD) | Evidence / Notes |
|----------|----------------------|------------------|
| **Can 1 DEV build this service independently?** | ☐ Yes / ☐ No / ☐ Partial | Dependencies on other services? Shared libs? Infra prereqs? |
| **Can 1 TESTER test this service independently?** | ☐ Yes / ☐ No / ☐ Partial | Contract tests? Contract stubs? Test data isolation? Mock servers? |
| **Shared infrastructure required before DEV starts?** | ☐ None / ☐ DB / ☐ Message bus / ☐ Cache / ☐ Auth / ☐ Service mesh / ☐ Secrets / ☐ Other | Provisioned by? Ticket? |
| **Shared libraries / contracts this service depends on?** | ☐ None / ☐ `libs/<name>` (version) / ☐ Protobuf pkg / ☐ OpenAPI pkg / ☐ npm pkg / ☐ Go module | Version pinned? Published? |
| **Can DEV run full test suite locally without shared infra?** | ☐ Yes / ☐ No (needs: ______) | Testcontainers / LocalStack / Mock servers / Contract tests |
| **Can TESTER run contract + integration tests in isolation?** | ☐ Yes / ☐ No (needs: ______) | Contract test suite published? Pact / Schemathesis / PactFlow? |
| **Deployable independently?** | ☐ Yes / ☐ No (monolith / shared deploy) | Independent container? Helm chart? K8s namespace? |
| **Rollback independent?** | ☐ Yes / ☐ No (shared DB migration / shared config) | Migration backward-compatible? Feature flags? |
| **Observability independent?** | ☐ Yes / ☐ No (shared dashboards / alerts) | Own dashboards? Own alerts? Own traces? |

**Parallelism Verdict (TECHLEAD fills after assessment):**
- ☐ **FULL PARALLEL** — 1 DEV + 1 TESTER can work independently end-to-end
- ☐ **PARTIAL** — DEV independent, TESTER needs shared infra (specify)
- ☐ **BLOCKED** — Shared infra / shared lib / shared DB migration required first (blocker ticket: ______)

---

### SECTION 6 — TECHLEAD Review Checklist (Service-Specific)

*TECHLEAD adds service-specific review items here. PM/DEV/TESTER do not edit this section.*

| # | Checklist Item | Severity (Blocker/Major/Minor) | Status (TECHLEAD fills) |
|---|----------------|--------------------------------|--------------------------|
| 1 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 2 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 3 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 4 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 5 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 6 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 7 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 8 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 9 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |
| 10 | | | ☐ Open / ☐ Fixed / ☐ Waived (reason) |

> **Common TECHLEAD checklist items (adapt per service):**
> - [ ] API contract matches OpenAPI/Protobuf spec exactly (request/response/error)
> - [ ] Idempotency keys enforced on all mutating endpoints
> - [ ] Pagination uses cursor-based (not offset) for lists > 100 items
> - [ ] All mutating endpoints have authz checks (not just authn)
> - [ ] Rate limiting enforced at edge + application layer
> - [ ] Secrets scanned clean in CI + pre-commit
> - [ ] SAST clean (High/Critical = 0)
> - [ ] SCA clean (Critical/High CVSS ≥ 7 = 0)
> - [ ] Container runs non-root, read-only FS, dropped caps
> - [ ] TLS 1.3 only, cert rotation automated
> - [ ] Security headers present (CSP, HSTS, XFO, etc.)
> - [ ] CORS allow-list explicit, no wildcard with credentials
> - [ ] Input validation at API boundary (not just ORM)
> - [ ] Output encoding context-aware (HTML/JS/JSON/SQL/Shell)
> - [ ] Audit log on all authz decisions + data mutations
> - [ ] Secrets rotated on schedule, rotation tested
> - [ ] Contract tests published + consumer-driven
> - [ ] Integration tests run in CI with Testcontainers / LocalStack
> - [ ] Load test baseline captured (p95 < 200ms / p99 < 500ms / error rate < 0.1%)
> - [ ] Observability: structured logs + traces + metrics + alerts (RED + USE)
> - [ ] Runbook exists: runbook.md with runbooks/alerts/runbook.md
> - [ ] README runs verbatim in clean checkout (make run / docker compose up)
> - [ ] SBOM generated + published on release
> - [ ] License scan clean (no GPL/AGPL/SSPL unless approved)
> - [ ] Threat model documented (STRIDE / MITRE ATT&CK) for Tier 1/2 services
> - [ ] Pen test scheduled / completed for Tier 1 services

---

### SECTION 7 — Review Rounds (TECHLEAD fills per round)

#### Round 1 — TECHLEAD Comments
| # | Severity | Comment | DEV Resolution Required? |
|---|----------|---------|--------------------------|
| 1 | | | ☐ Fix / ☐ Explain |
| 2 | | | ☐ Fix / ☐ Explain |
| 3 | | | ☐ Fix / ☐ Explain |

**Verdict Round 1**: ☐ APPROVED / ☐ CHANGES REQUIRED / ☐ BLOCKED

---

#### Round 2 — TECHLEAD Comments (if Round 1 not APPROVED)
| # | Severity | Comment | DEV Resolution |
|---|----------|---------|----------------|
| 1 | | | ☐ Fixed / ☐ Explained |
| 2 | | | ☐ Fixed / ☐ Explained |

**Verdict Round 2**: ☐ APPROVED / ☐ CHANGES REQUIRED / ☐ BLOCKED

---

#### Round 3 — TECHLEAD Comments (if Round 2 not APPROVED)
| # | Severity | Comment | DEV Resolution |
|---|----------|---------|----------------|
| 1 | | | ☐ Fixed / ☐ Explained |

**Verdict Round 3**: ☐ APPROVED / ☐ **BLOCKED → CTO ESCALATION**

---

### SECTION 8 — Final Sign-Off

| Role | Name | Signature (APPROVED line) | Date |
|------|------|---------------------------|------|
| **TECHLEAD** | | `APPROVED — <one-line rationale>` | |
| **PM** (if BUSINESS-IMPACT flagged) | | `APPROVED — <one-line rationale>` | |
| **QA** (ship gate) | | `APPROVED — <one-line rationale>` | |

> **BUSINESS-IMPACT FLAG**: ☐ No / ☐ Yes — *PM approval also required before merge*

---

---

## SERVICE 1 — `<SERVICE-1-NAME>`

> **PM/DEV/TESTER: Fill Sections 1–5 above for this service. TECHLEAD fills Section 6+7+8 during review.**

*(Copy the template sections above into this service's section — or keep as reference and fill inline below.)*

### 1. Service Identity & Interface Signature
*(PM/DEV fill)*

### 2. Data Dependencies
*(DEV fills)*

### 3. Security Surface Checklist
*(DEV fills implementation; TECHLEAD verifies)*

### 4. SAST/SCA/Secret-Scan Tooling
*(DEV/TECHLEAD pick per stack)*

### 5. Parallelism Assessment
*(PM/TECHLEAD assess)*

### 6. TECHLEAD Review Checklist (Service-Specific)
*(TECHLEAD adds items)*

### 7. Review Rounds
*(TECHLEAD fills per round)*

### 8. Final Sign-Off
*(Signatures)*

---

## SERVICE 2 — `<SERVICE-2-NAME>`

### 1. Service Identity & Interface Signature
*(PM/DEV fill)*

### 2. Data Dependencies
*(DEV fills)*

### 3. Security Surface Checklist
*(DEV fills implementation; TECHLEAD verifies)*

### 4. SAST/SCA/Secret-Scan Tooling
*(DEV/TECHLEAD pick per stack)*

### 5. Parallelism Assessment
*(PM/TECHLEAD assess)*

### 6. TECHLEAD Review Checklist (Service-Specific)
*(TECHLEAD adds items)*

### 7. Review Rounds
*(TECHLEAD fills per round)*

### 8. Final Sign-Off
*(Signatures)*

---

## SERVICE 3 — `<SERVICE-3-NAME>`

### 1. Service Identity & Interface Signature
*(PM/DEV fill)*

### 2. Data Dependencies
*(DEV fills)*

### 3. Security Surface Checklist
*(DEV fills implementation; TECHLEAD verifies)*

### 4. SAST/SCA/Secret-Scan Tooling
*(DEV/TECHLEAD pick per stack)*

### 5. Parallelism Assessment
*(PM/TECHLEAD assess)*

### 6. TECHLEAD Review Checklist (Service-Specific)
*(TECHLEAD adds items)*

### 7. Review Rounds
*(TECHLEAD fills per round)*

### 8. Final Sign-Off
*(Signatures)*

---

## SERVICE 4 — `<SERVICE-4-NAME>`

### 1. Service Identity & Interface Signature
*(PM/DEV fill)*

### 2. Data Dependencies
*(DEV fills)*

### 3. Security Surface Checklist
*(DEV fills implementation; TECHLEAD verifies)*

### 4. SAST/SCA/Secret-Scan Tooling
*(DEV/TECHLEAD pick per stack)*

### 5. Parallelism Assessment
*(PM/TECHLEAD assess)*

### 6. TECHLEAD Review Checklist (Service-Specific)
*(TECHLEAD adds items)*

### 7. Review Rounds
*(TECHLEAD fills per round)*

### 8. Final Sign-Off
*(Signatures)*

---

## SERVICE 5 — `<SERVICE-5-NAME>`

### 1. Service Identity & Interface Signature
*(PM/DEV fill)*

### 2. Data Dependencies
*(DEV fills)*

### 3. Security Surface Checklist
*(DEV fills implementation; TECHLEAD verifies)*

### 4. SAST/SCA/Secret-Scan Tooling
*(DEV/TECHLEAD pick per stack)*

### 5. Parallelism Assessment
*(PM/TECHLEAD assess)*

### 6. TECHLEAD Review Checklist (Service-Specific)
*(TECHLEAD adds items)*

### 7. Review Rounds
*(TECHLEAD fills per round)*

### 8. Final Sign-Off
*(Signatures)*

---

## TECHLEAD Session Report to CTO (append at session end)

> **Session**: 2026-07-21 Emergency Idle Cycle — SEAM Review Prep
> **Reviews Prepared**: 5 templates (Services 1–5)
> **Templates Written To**: `tasks/seam-reviews-2026-07-21.md`
> **Next Action**: PM assigns DEV/TESTER pairs to each service; DEV fills Sections 1–5; TECHLEAD begins Round 1 reviews.
> **Recurring Findings (if any)**: *None yet — first cycle.*
> **Blockers**: *Awaiting CTO architecture output in `debates/emergency-idle-2026-07-21.md` for service names/stacks.*
> **Escalations**: *None.*
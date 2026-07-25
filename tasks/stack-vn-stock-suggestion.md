# Stack Decision: VN Stock Suggestion System (Option C - Parallel Flagship Tracks)

## Executive Summary

**Product**: VN Stock Suggestion System (app: `vn-stock-suggestion`)
**Decision**: Option C - Parallel Flagship Tracks with 4 independent services
**Runtime Envelope**: Node.js + Python + Static Web (compliant with §7.2)
**Status**: Ready to begin M1 parallel execution

## Service Architecture (4 Independent Services)

### Service 1: Data Ingestion Service (S1)
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Core Framework** | Python 3.11+, FastAPI + Pydantic v2 | REST API framework with strict validation |
| **Database** | PostgreSQL 15+, SQLAlchemy 2.0 | Persistent storage with parameterized queries |
| **Cache/Queue** | Redis 7 Streams | Data streaming and cache layer |
| **Testing** | pytest + hypothesis + Pact | Contract testing with downstream consumers |
| **Security** | bandit + semgrep(python) + gitleaks + snyk | SAST + secret scanning + dependency analysis |
| **Domain Adapters** | Custom Python services | VN stock data adapters (VNIndex, CafeF, Vietstock, VNDirect) |

### Service 2: Signal Engine Service (S2)
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Core Framework** | Python 3.11+, FastAPI + pydantic | Signal computation and REST API |
| **Libraries** | TA-Lib + pandas-ta (and fallback) | Technical analysis indicators |
| **Cache/Queue** | Redis 7 Streams | Signal event streaming |
| **Testing** | pytest + hypothesis + property-based | Signal integrity and computation validation |
| **Security** | bandit + semgrep(python) + gitleaks + snyk | Python security tooling |
| **Shared Library** | `vn-tech-indicators` (pypi) | Core technical analysis library |

### Service 3: API Gateway / Aggregation Service (S3)
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Core Framework** | Node.js 20+, Fastify + TypeScript | Auth, routing, aggregation |
| **Database** | PostgreSQL 15+, Knex/parameterized | Metadata and caching |
| **Cache/Queue** | Redis 7 | Response caching and pub/sub |
| **Testing** | vitest + k6 + Pact | Unit, contract, and load testing |
| **Security** | semgrep(js/ts) + eslint-security + gitleaks + snyk | JavaScript/TypeScript security |
| **Auth** | jose library + JWKS rotation | JWT validation and RBAC |
| **Shared Library** | `vn-api-gateway-core` (npm) | Auth/rate-limit/aggregation core |

### Service 4: Web UI (S4)
| Component | Technology | Responsibility |
|-----------|------------|----------------|
| **Framework** | TypeScript 5+, React 18 + Vite + Tailwind | SPA with design system |
| **Styling** | Tailwind CSS + CSS-in-JS | Modern UI design |
| **Testing** | vitest + playwright + axe-core | Component, E2E, and accessibility tests |
| **Security** | semgrep(js/ts) + eslint-plugin-jsx-a11y + gitleaks | Web UI security |
| **Build** | Vite optimized build (<500KB) | Static SPA deployment |
| **Shared Library** | `vn-design-system` (npm) | Reusable UI components |

## Clean Seam Contracts

### S1 ↔ S2 Contract
- **Schema**: `vn-stock-schemas` (Pydantic + JSON Schema + TypeScript)
- **Transport**: Redis Streams (raw → normalized topic)
- **Payload**: Normalized OHLCV + metadata schema

### S2 ↔ S3 Contract  
- **Schema**: `vn-stock-schemas` + signal-specific types
- **Transport**: Redis Streams (signal events) + REST fallback
- **Payload**: Signal events (symbol, signal, strength, timestamp, metadata)

### S3 ↔ S4 Contract
- **Schema**: OpenAPI 3.1 spec + WebSocket events
- **Transport**: HTTPS + WSS
- **Payload**: Stock data, signals, portfolio information

## Security Gate Compliance (§7.2)

### S1 Security Controls
- **SAST**: bandit + semgrep(python) + schema validation
- **Secret Scan**: gitleaks (all adapter secrets)
- **SCA**: safety + snyk + SBOM (cyclonedx-py)
- **Auth**: Internal service communication (no external auth)
- **Validation**: Pydantic v2 strict validation on all external inputs
- **Injection**: SQLAlchemy ORM + parameterized queries
- **Secure Headers**: FastAPI middleware (CSP, HSTS)
- **CORS**: FastAPI CORS middleware (allowlist origins)

### S2 Security Controls
- **SAST**: bandit + semgrep(python) + TA-Lib input bounds checking
- **Secret Scan**: gitleaks
- **SCA**: safety + snyk + SBOM
- **Auth**: Internal service communication only
- **Validation**: Pydantic v2 strict on Redis stream consumption
- **DoS**: Input schema validation + rate-limit computation
- **Resource**: Memory/CPU limits on signal computation
- **Secure Headers**: FastAPI middleware

### S3 Security Controls
- **SAST**: semgrep(js/ts) + eslint-security
- **Secret Scan**: gitleaks
- **SCA**: snyk + @cyclonedx/bom
- **Auth**: JWT validation (jose) with JWKS rotation
- **Validation**: Zod + Fastify validation (all inputs)
- **Rate Limiting**: fastify-rate-limit per tenant/IP
- **DoS**: Circuit breakers on S1/S2 calls
- **Injection**: Parameterized queries + input sanitization
- **Secure Headers**: fastify-helmet
- **Audit**: Structured logging + audit trails

### S4 Security Controls
- **SAST**: semgrep(js/ts) + eslint-plugin-jsx-a11y
- **Secret Scan**: gitleaks
- **SCA**: snyk + @cyclonedx/bom
- **Input Validation**: Zod (API client) + React escaping
- **Injection**: React default escaping + CSP
- **XSS**: Prevent dangerouslySetInnerHTML without sanitization
- **Clickjacking**: X-Frame-Options + CSP
- **Supply Chain**: npm audit + snyk + dependabot
- **Secure Headers**: Static headers (Netlify/Vercel)

## Dependency Risk Assessment

| Dependency | Risk Level | Mitigation |
|------------|------------|------------|
| TA-Lib (C extension) | **HIGH** (build failures, supply chain) | Pin exact version, use manylinux wheels, pandas-ta fallback, SBOM scan |
| fastapi / pydantic / sqlalchemy | LOW (mature) | Pin versions, dependabot, snyk monitoring |
| fastify / @fastify/* | LOW (mature) | Pin versions, dependabot, snyk monitoring |
| react / vite / tailwind | LOW (mature) | Pin versions, dependabot, snyk monitoring |
| redis-py / redis (node) | LOW | Pin versions |
| psycopg2 / pg (node) | LOW | Pin versions |

## Threat Models

### S1: Data Ingestion Surface
- **Attackers**: Stock data competitors, script kiddies
- **Threats**: SSRF to VN stock APIs, injection in external responses
- **Controls**: Allowlist domains + timeout + size limits + Pydantic validation + secret management

### S2: Signal Engine Surface
- **Attackers**: Trading bots, data poisoning
- **Threats**: Computation integrity (TA-Lib), malicious payload via Redis
- **Controls**: Input bounds checking + rate-limit computation + resource limits

### S3: API Gateway Surface
- **Attackers**: Public users, competitors, insider threats
- **Threats**: Auth bypass, rate-limit bypass, injection, DoS cascades
- **Controls**: JWT validation + rate-limit + Zod validation + circuit breakers + audit logging

### S4: Web UI Surface
- **Attackers**: End users, attackers
- **Threats**: XSS, CSP bypass, clickjacking, supply chain
- **Controls**: React escaping + strict CSP + X-Frame-Options + npm audit

## Reusable Platform Assets

| Asset | Publishing Service | Package Type | Consumers |
|-------|-------------------|--------------|-----------|
| `vn-stock-schemas` | S1 | pypi + npm | S1, S2, S3, S4, future products |
| `vn-tech-indicators` | S2 | pypi | S2, future signal consumers |
| `vn-api-gateway-core` | S3 | npm | S3, future API gateways |
| `vn-design-system` | S4 | npm | S4, future web UIs |
| `vn-data-adapters` | S1 | pypi | S1, future ingestion services |

## Parallelism Plan

**Builder Allocation for M1:**
- **4 DEV Instances**: One per service (S1, S2, S3, S4)
- **4 TESTER Instances**: One per service (S1, S2, S3, S4)  
- **1 BA Instance**: Shared across all services
- **1 TECHLEAD Instance**: Architecture review across all services

**Sequential Dependencies:**
1. **S1 completes schema publishing** → S2 and S3 can start
2. **S2 completes schema publishing** → S3 can start
3. **S3 completes OpenAPI spec** → S4 can start
4. **All services run in parallel** after initial schema publication

**First Shippable Increment:** S1 (Data Ingestion) alone is shippable in M1

## CI/CD Pipeline Configuration

Each service has its own pipeline:
- **S1**: Python coverage + security scan + contract testing with S2
- **S2**: Python coverage + security scan + contract testing with S3  
- **S3**: Node.js coverage + security scan + load testing + contract testing with S4
- **S4**: Frontend lint + accessibility test + build verification

## Milestone Sequencing

| Milestone | Services Delivered | First Shippable |
|-----------|-------------------|-----------------|
| **M1 (Cycle 99)** | S1 (Data Ingestion) ships first | **S1 alone is shippable** | 
| **M2 (Cycle 100)** | S2, S3 ship | S1+S2+S3 = signal API with auth |
| **M3 (Cycle 101)** | S4 ships | Full vertical slice: UI → Gateway → Signals → Ingestion |

## Startup Risks & Mitigations

1. **TA-Lib compilation failures** → Vendor wheels, pin versions, pandas-ta fallback
2. **Redis schema mismatches** → Shared `vn-stock-schemas` package enforced
3. **S3 authentication issues** → JWT validation with JWKS rotation
4. **S4 WebSocket connectivity** → Backpressure handling + retry logic

## Scaled Risks (Post-M1)

1. **Integration hell** (multiple services) → Clean contracts + automated contract testing
2. **Dependency confusion** → Use scoped packages + private registries where needed
3. **Performance bottlenecks** → Circuit breakers + Redis caching + load testing
4. **Security drift** (multiple teams) → TECHLEAD continuous review + shared security tooling

## Decision Rationale

**Why Option C (Parallel Flagship Tracks) over other options:**

- **Option A (Go deep)**: Too slow - only 1 service at a time, delays first value
- **Option B (Horizontal platform)**: Too balanced - steals from flagship velocity  
- **Option D (Portfolio breadth)**: Too broad - spreads resources too thin
- **Option C maximizes**: **Parallellism** (4 services), **Speed to first value** (S1 ships in M1), **Reusability** (platform assets), **Risk mitigation** (independent services)

**Runtime Envelope Compliance:**
- ✓ All services within §7.2 envelope (Node.js, Python, Static Web)
- ✓ No envelope extensions needed
- ✓ Security gates integrated into CI/CD per §7.2.1
- ✓ Quality mandate enforced across all services

**Next Steps:**
1. HR hires 4 DEV + 4 TESTER + 1 BA + 1 TECHLEAD
2. PM assigns 16+ ready tasks to all instances  
3. All services start in parallel M1
4. S1 becomes first shippable increment
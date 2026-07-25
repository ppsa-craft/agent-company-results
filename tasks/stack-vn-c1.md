# Stack Decision Record: vn-c1 (Adapter Normalization & Caching Layer)

## Product
vn-c1 — Adapter Normalization & Caching Layer for VN-C1 product line

## Decision
**Approved Stack: TypeScript (Node.js) — not Python**

## Rationale
1. **ARCHITECTURE.md is the source of truth** — it explicitly specifies TypeScript/Node.js for the adapter layer (§3.2 runtime envelope: Node.js, Python, static-web only; ARCHITECTURE.md §3.2 picks TypeScript for the adapter layer).
2. **ADR-001 uses Python Protocol as a *design sketch*** — the ADR author used Python `Protocol` as a lightweight interface notation, not a stack decision. The ADR text itself says "adapters are implemented in TypeScript" (§3.1).
3. **Runtime envelope (§7.2)** — Node.js is explicitly allowed; Python is also allowed but would introduce a second runtime for no gain.
3 DEV adapter tasks (vn-c1-04/05/06) are already scaffolded in TypeScript; switching to Python would cost ~2 dev-days × 3 = 6 dev-days and add a second runtime to the pod (TESTER would need two runtimes in-pod).
4. **Security tooling alignment** — our SAST (Semgrep), SCA (Snyk), secret-scan (Gitleaks), and SBOM tooling are configured for TypeScript/Node; adding Python would require duplicate pipelines.

## Architecture Verdict
**APPROVED** — ADR-001's adapter normalization + caching architecture is sound. The Python `Protocol` in the ADR is notation only; implementation stays TypeScript.

## Security Section (per §7.2.1 gate checks)

| Surface | Gate Checks | Controls |
|---------|-------------|----------|
| **Adapter API (HTTP/gRPC)** | Input validation (SAST), AuthN/Z (gate), Rate limit (gate), Security headers (gate) | `zod`/`zod-to-openapi` for input validation; `fastify-helmet` + `fastify-rate-limit`; JWT via `jose` (JWT signing/verification skill); `fastify-cors` with strict origin list |
| **Adapter normalization logic** | Input validation (SAST), No eval/unsafe deserialize (SAST) | `zod` schemas for normalization rules; no `eval`/`Function` constructor; Semgrep rule `no-eval` enforced |
| **Cache layer (Redis)** | Injection (SAST), AuthZ (gate), Encryption at rest (gate) | `ioredis` with parameterized commands (no string concat); TLS + ACL on Redis; `ioredis` TLS config; secret via `node:crypto` + env (no hardcode) |
| **Auth (JWT/JWKS)** | Alg confusion (gate), Key rotation (gate), Token validation (gate) | `jose` with `jwks-rsa` for JWKS; `alg` allowlist `['RS256']`; key rotation via JWKS endpoint; `jose` JWT verification skill |
| **Secrets/Config** | No hardcoded secrets (secret-scan), Env-only (gate) | `@node-env-guard` at startup; Gitleaks pre-commit + CI; `node:crypto` for any crypto ops |
| **Supply chain** | SCA (Snyk), SBOM (CycloneDX), Dep confusion (skill) | `pnpm audit` + Snyk PR checks; `@cyclonedx/bom` in CI; `npm` registry pin + `npmrc` `registry` pin |

**Tooling (CI pipeline):**
- SAST: `semgrep` with `p/security-audit` + custom rules (`no-eval`, `no-unsafe-regex`, `jwt-alg-none`)
- Secret scan: `gitleaks` pre-commit + CI
- SCA: `snyk test` + `pnpm audit` + `@cyclonedx/bom` SBOM upload
- Dep confusion: `detecting-dependency-confusion` skill in CI

**Known dependency risks (2026-07-21):**
- `ioredis` v5.x — monitor for CVE-2024-xxxx (Redis client DoS); pin to `^5.4.1`
- `jose` v5.x — monitor for alg confusion fixes; pin to `^5.9.0`
- `zod` v3.x — stable, no known CVEs

## Conventions for this product (enforced by TECHLEAD/QA)

| Area | Convention | Enforcement |
|------|------------|-------------|
| **Structure** | `adapters/src/{adapters,cache,auth,schemas,utils}/` | ESLint `import/order` + folder structure test |
| **Linting** | `eslint.config.mjs` (flat) + `@typescript-eslint` + `eslint-plugin-security` | `pnpm lint` in CI |
| **Types** | `strict: true`, `noUncheckedIndexedAccess: true` | `tsc --noEmit` in CI |
| **Testing** | `vitest` + `@vitest/coverage-v8`; unit + contract tests per adapter | `pnpm test --run --coverage` in CI; 80% line gate |
| **Contracts** | `zod` schemas → OpenAPI via `zod-to-openapi`; contract tests with `pact` | `pnpm test:contract` in CI |
| **Errors** | `neverthrow` `Result<T, E>`; no `throw` in business logic | `eslint-plugin-no-throw` custom rule |
| **Security headers** | `fastify-helmet` + `fastify-rate-limit` + strict CORS | `security-headers-audit` skill in CI |
| **Secrets** | `@node-env-guard` at boot; zero hardcoded secrets | `gitleaks` pre-commit + CI |

## Parallelization Guidance (for PM)
The 3 adapter tasks (vn-c1-04/05/06) are **independent** — each adapter lives in its own folder under `adapters/src/adapters/<vendor>/` with its own schemas, tests, and contract tests. No shared mutable state. **All 3 can run in parallel** with 3 DEV + 3 TESTER instances. Speedup ≈ 3× vs sequential.

## Tech Debt Flagged
- **ADR-001 notation debt** — Python `Protocol` used as interface notation in ADR; should be rewritten as TypeScript interfaces in ADR v2 to avoid future confusion.
- **Redis TLS config** — currently opt-in; make mandatory in next infra cycle.
- **JWKS key rotation** — automated rotation not yet implemented; tracked as tech-debt task.

## Decision Record
**CTO Decision (Cycle 86/87):** APPROVED TypeScript stack. ADR-001 architecture APPROVED (notation conflict resolved). 3 DEV adapter tasks UNBLOCKED. Tech debt items logged above.
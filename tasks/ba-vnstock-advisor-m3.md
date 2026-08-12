# BA — M3 Use Cases: Suggestion API + Web UI (vnstock-advisor)

- **App:** vnstock-advisor | **Milestone:** M3 (suggestion-api + web-ui) | **Artifact:** BA use cases
- **Status:** DRAFT — **DEBATE-READY** (delivered pre-freeze-lift; PM to schedule the §5.1 debate before M3 build starts)
- **Feeds tasks:** `vnstock-advisor-m3-dev-*` (staged post-freeze: M3-A suggestion-api, M3-B web-ui, M3-C e2e wiring per COMPANY_STATE)
- **Bars:** complete / testable / traceable (QA validates against exactly these three)

---

## 0. Scope and surfaces

M3 = idea-backlog rank 3: **ranked suggestions with reasoning + disclaimer, README-runnable end-to-end**.

| # | Surface | Owner service | Port (shared config) | Features in scope |
|---|---------|---------------|----------------------|-------------------|
| S1 | Suggestion API | `services/suggestion-api/` | 8003 | `GET /suggestions` (ranked list w/ reasoning), `POST /auth/login`, `POST /auth/refresh`, `GET /auth/jwks`, `GET /health`(+live/ready), disclaimer on every response, error handling |
| S2 | Web UI | `services/web-ui/` | 3000 | List view, symbol detail view, disclaimer visibility, API-error surfacing, locale handling |
| S3 | E2E wiring | repo root + docs | — | README-runnable end-to-end: auth → suggestions → detail, disclaimer visible end-to-end |

**Grounding (read before debate):**
- M1 merged on main: `services/data-ingest/` (FastAPI; `disclaimer.py` = shipped single source of truth), `shared/python/` (`vnstock_shared` config/models).
- M2 on `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev` (TECHLEAD-approved, pending merge): frozen `/rank` contract in `services/analysis-engine/src/analysis_engine/schemas.py` + `main.py`; docs `docs/specs/screening-ranking.md`, `docs/compliance/disclaimer.md` (PM-approved), `docs/use-cases/analysis-engine.md` (PM-approved).
- Drafts on the M2 branch (NOT approved, **do not silently treat as contract**): `docs/use-cases/suggestion-api.md`, `docs/api/suggestion-api.openapi.yaml`. Where a draft conflicts with the shipped M2 code, **the shipped M2 shape wins** for consumption (see flagged mismatches in §7).

**Dependency note:** the CTO stack record `tasks/stack-vnstock-advisor.md` **does not exist yet** (CTO task `vnstock-advisor-m3-cto-stack-record.md` is `ready`, unclaimed). These use cases are grounded in the M1/M2 evidence instead; the debate should confirm the M3 seam map once CTO produces it.

---

## 1. Actors

| Actor | Description |
|-------|-------------|
| **End User (investor)** | Vietnamese retail investor researching VN equities; reads ranked suggestions + reasoning; must always see the disclaimer |
| **API Client** | Any consumer (web-ui, script, third-party) holding a valid RS256 JWT with `suggestions:read` scope |
| **Web UI User** | Browser user of `services/web-ui/` acting on behalf of the End User |
| **Analysis Engine (upstream)** | Internal M2 service; `POST /rank` supplies `ranked[]`/`excluded[]` + reasoning (frozen contract) |
| **Monitoring System** | Probes `GET /health` (+ live/ready) |
| **Anonymous Requester** | No/invalid/expired token; must authenticate first |

---

## 2. Use cases — Suggestion API (surface S1)

### UC-M3-A1 — Authenticated user retrieves ranked suggestions (`GET /suggestions`)

**Actor:** API Client / Web UI User (via Bearer token). **Surface:** S1, endpoint `GET /suggestions`.

**Good flow:**
1. Client calls `GET /suggestions` with `Authorization: Bearer <access_token>` (RS256, `suggestions:read` scope).
2. API validates token (per UC-M3-A2), resolves portfolio input (query `symbols`, optional `weights`/`date`/`algorithm_version`), calls analysis-engine `POST /rank`, maps the result into the suggestion envelope, attaches the disclaimer (header + `meta.disclaimer`), returns `200 OK`.

**Acceptance criteria:**
- AC-A1.1: Valid token + `suggestions:read` → `200 OK`; body contains `request_id`, `generated_at`, `source`, `ranked[]`, `excluded[]`.
- AC-A1.2: Every `ranked[]` entry carries `rank` (1-based, sequential), `symbol`, `composite_score` (0–100), `components` (momentum/trend/volume/volatility), `sub_components`, `reasoning` (non-empty list) — pass-through of the frozen M2 `/rank` output shape.
- AC-A1.3: `excluded[]` entries carry `symbol`, `reason`, `missing_indicators` — matching the **shipped** M2 `/rank` exclusion shape (see §7, flag M2-1).
- AC-A1.4: `ranked[]` is ordered by `composite_score` descending; ties broken by `symbol` ascending (determinism per `screening-ranking.md` §4). TESTER: same request twice → identical ordering.
- AC-A1.5: Response carries `X-Disclaimer` header AND `meta.disclaimer` with both locales `vi-VN`/`en-US` (see UC-M3-A7 + BA doc).
- AC-A1.6: `meta.generated_at` (UTC) and `meta.source` (engine/version, e.g. `analysis-engine-v1.0`) present for freshness/traceability.

**Failure flow / acceptance:**
- AC-A1.7: Missing token → `401 auth.token_missing`; invalid signature/`alg` → `401 auth.token_invalid`; expired → `401 auth.token_expired`; valid token lacking scope → `403 auth.scope_denied`. All bodies are RFC 7807 `application/problem+json` (`type`, `title`, `status`, `detail`, `instance`).
- AC-A1.8: Unsupported `algorithm_version` → `400` (mirrors M2 `UNSUPPORTED_VERSION` semantics).

---

### UC-M3-A2 — JWT RS256 authentication: login, refresh rotation, JWKS

**Actor:** Web UI User / API Client. **Surface:** S1, `POST /auth/login`, `POST /auth/refresh`, `GET /auth/jwks`.

**Good flow:**
1. `POST /auth/login` with credentials → server validates, issues `access_token` (RS256, short-lived) + rotating `refresh_token`.
2. Protected calls present the access token as `Bearer`; server verifies: RS256 only, signature against `GET /auth/jwks` keys, `exp`/`iat`/nbf, required claims.
3. Near expiry, `POST /auth/refresh` with the current refresh token → server **rotates** (old token revoked, new pair issued).

**Acceptance criteria:**
- AC-A2.1: Login with valid credentials → `200` with `access_token`, `refresh_token`, `token_type: Bearer`, `expires_in`.
- AC-A2.2: Token with any `alg` other than RS256 (e.g. `none`, HS256 downgrade) → `401 auth.token_invalid`.
- AC-A2.3: Access token `exp` = 15 minutes from issue (per OpenAPI draft; confirm in debate — M2 branch shared config default is 30 min — **flag, see §7 open Q4**).
- AC-A2.4: Refresh **rotates**: the presented refresh token is unusable immediately after use → `401 auth.refresh_invalid`.
- AC-A2.5: Reuse of an already-rotated refresh token → `409 auth.refresh_reuse` (token-family breach revokes the session — fails closed).
- AC-A2.6: `GET /auth/jwks` returns the public JWK(s) (`kty`, `use`, `kid`, `n`, `e`, `alg`) used to verify RS256 tokens.
- AC-A2.7: No secrets in any response/error body: private key material, raw passwords, or token values must never be echoed (TESTER checks error bodies).

---

### UC-M3-A3 — Invalid portfolio input: bad symbols, empty list, invalid weights (failure path)

**Actor:** API Client (authenticated). **Surface:** S1, `GET /suggestions` params.

**Acceptance criteria (all failure-path):**
- AC-A3.1: Empty `symbols` (or `symbols` omitted with no default universe configured) → `422 validation.portfolio_invalid` (RFC 7807; message names the missing/empty field).
- AC-A3.2: Symbol not matching the VN ticker pattern (`^[A-Z][A-Z0-9]{0,9}$` per M2 `SYMBOL_PATTERN`) → `422 validation.portfolio_invalid`, detail lists the offending symbols (no silent drop, no 500).
- AC-A3.3: `symbols` exceeding the M2 `/rank` ceiling (100 per `RankRequest.max_length`) → explicit `422` naming the limit (do not silently truncate).
- AC-A3.4: `weights` present but not exactly the key set `{momentum, trend, volume, volatility}`, or not summing to 1.0 ±0.001, or any weight outside [0.0, 1.0] → `422 validation.weights_invalid` (mirrors M2 `RankingError` rules; TESTER D2 precedent).
- AC-A3.5: Malformed `date` (not `YYYY-MM-DD`) → `400`/`422` validation error.
- AC-A3.6: All failures return `application/problem+json`; none return a bare 500 or a stack trace.

---

### UC-M3-A4 — Empty universe / all symbols excluded (failure path)

**Actor:** API Client (authenticated). **Surface:** S1, `GET /suggestions`.

**Description:** Requested symbols resolve, but none are rankable (e.g., all have <200 valid bars → `excluded[]` with `insufficient_data`; or the analysis universe is empty).

**Acceptance criteria:**
- AC-A4.1: Request with zero rankable symbols → `200 OK` (not an error) with `ranked: []` and every requested symbol present in `excluded[]` carrying `reason` (e.g., `insufficient_data`) + `missing_indicators`.
- AC-A4.2: `excluded[]` must not silently drop symbols (TESTER: count(excluded) + count(ranked) == count(requested valid symbols)).
- AC-A4.3: Disclaimer (`X-Disclaimer` header + `meta.disclaimer`) is present **even when `ranked` is empty** — an empty result is still a suggestion surface.
- AC-A4.4: When the default analysis universe is empty/unconfigured and no `symbols` supplied → explicit `422 validation.portfolio_invalid` with a detail that distinguishes "no universe configured" from "no rankable symbols".

---

### UC-M3-A5 — Upstream analysis-engine failure (failure path)

**Actor:** API Client (authenticated). **Surface:** S1, `GET /suggestions`.

**Description:** Analysis-engine `POST /rank` is unreachable, times out, or returns an error.

**Acceptance criteria:**
- AC-A5.1: `POST /rank` unreachable/timeout/5xx → `502 upstream.rank_failed` (RFC 7807 body, `detail` states the upstream failure without leaking internal stack traces or connection strings).
- AC-A5.2: Timeout bounded (configurable, e.g. `RANK_TIMEOUT_SECONDS`); TESTER can verify the 502 arrives within the bound, not after client hang.
- AC-A5.3: M2 `/rank` 4xx responses are mapped to an appropriate suggestion-api 4xx/502 with the M2 problem code preserved in the body `detail`/`type` for diagnosis.
- AC-A5.4: Health reporting reflects upstream state: `GET /health/ready` returns `not_ready` with `analysis_engine: down` while `/rank` is failing (see UC-M3-A8).

---

### UC-M3-A6 — Rate limiting (failure path)

**Actor:** API Client. **Surface:** S1, `GET /suggestions`.

**Acceptance criteria:**
- AC-A6.1: Exceeding the per-user limit (`SUGGESTIONS_RATE_LIMIT`, default 100 req / 15 min per `sub`) → `429 rate_limit.exceeded` with `Retry-After` header and RFC 7807 body.
- AC-A6.2: Rate limit is keyed **per user** (`sub` claim), not per client IP.
- AC-A6.3: `GET /health` (+live/ready) is exempt from rate limiting.

---

### UC-M3-A7 — Mandatory disclaimer on every suggestion response (cross-cutting)

**Actor:** API Client / Web UI User. **Surface:** S1, every response of `GET /suggestions`.

**Acceptance criteria (the flagship constraint, made testable):**
- AC-A7.1: Every `GET /suggestions` response (200 **and** error responses that still carry a suggestion payload; at minimum all 200s) includes `X-Disclaimer` header AND `meta.disclaimer`.
- AC-A7.2: `meta.disclaimer` object contains **both** `vi-VN` and `en-US` full text, byte-identical to the single source of truth (see BA doc `tasks/ba-vnstock-advisor-m3-doc.md` §3; TESTER does exact string comparison).
- AC-A7.3: `X-Disclaimer` carries the short variant for the negotiated locale (`Accept-Language`; default `vi-VN`), byte-identical to the single source of truth.
- AC-A7.4: A suggestion response missing `meta.disclaimer` **fails the contract test** (no silent pass — QA gate; mirrors `compliance/disclaimer.md` checklist).
- AC-A7.5: Disclaimer text is never truncated/elided by pagination, filtering, or empty results.

---

### UC-M3-A8 — Health endpoints

**Actor:** Monitoring System. **Surface:** S1, `GET /health`, `GET /health/live`, `GET /health/ready`.

**Acceptance criteria:**
- AC-A8.1: `GET /health` → `200` with `status` ∈ {healthy, degraded, unhealthy}, `service`, `version`, `uptime_seconds`, `checks[]`.
- AC-A8.2: `GET /health/live` → `200 {"status":"alive"}` while the process serves.
- AC-A8.3: `GET /health/ready` → `200 {"status":"ready","dependencies":{analysis_engine, database}}` when both dependencies are up; `503 {"status":"not_ready", ...}` when any required dependency is down (matches UC-M3-A5.4).
- AC-A8.4: Health endpoints are unauthenticated and exempt from rate limiting.

---

## 3. Use cases — Web UI (surface S2)

### UC-M3-W1 — User views the ranked suggestions list (list view)

**Actor:** Web UI User. **Surface:** S2, list view (landing/dashboard of the UI).

**Good flow:**
1. User logs in (UC-M3-A2 via UI) → UI calls `GET /suggestions` → renders the ranked list in rank order.

**Acceptance criteria:**
- AC-W1.1: List renders every `ranked[]` entry in order: `rank`, `symbol`, `composite_score`, and at least the reasoning array (full `reasoning` expandable/inline); excluded symbols are shown in a clearly separated section with their `reason` (never silently hidden).
- AC-W1.2: Score/component display matches the API values (no transformation drift — TESTER cross-checks UI text vs API response for ≥1 symbol).
- AC-W1.3: **Disclaimer visible without scrolling (above the fold), on first paint, non-dismissible** (no close button, no hide flag, no "premium removes disclaimer"); present in the raw HTML (server-rendered, not JS-injected-only) per `compliance/disclaimer.md`.
- AC-W1.4: A click/tap on a listed symbol navigates to the detail view (UC-M3-W2) for that symbol.

**Failure flow / acceptance:**
- AC-W1.5: On `401`/expired token → UI routes to login and, after re-auth, returns to the list (see UC-M3-W3).
- AC-W1.6: On empty `ranked` + populated `excluded` → UI shows the empty state per UC-M3-W4 (disclaimer still rendered).

---

### UC-M3-W2 — User views symbol detail (detail view)

**Actor:** Web UI User. **Surface:** S2, detail view for a symbol.

**Good flow:**
1. User selects a symbol from the list → UI renders that symbol's detail: composite score, component scores (momentum/trend/volume/volatility), sub-components, and full reasoning.

**Acceptance criteria:**
- AC-W2.1: Detail view shows `symbol`, `composite_score`, all four `components` values, `sub_components` raw values, and the full `reasoning` list from the API payload (no fabrication).
- AC-W2.2: **Disclaimer rendered below the header and above the first signal/recommendation block**, full variant, default locale `vi-VN`, switching to `en-US` on locale switch; non-dismissible (per BA doc placement table).
- AC-W2.3: Detail view is reachable for every `ranked[]` symbol; selecting an `excluded[]` symbol shows its exclusion reason with the disclaimer still present.
- AC-W2.4: Browser back/forward and a direct URL to the detail view both work (deep-linkable) — TESTER checks a direct navigation renders the same content as clicking through.

**Failure flow / acceptance:**
- AC-W2.5: Detail data fetch fails → friendly error state per UC-M3-W3; disclaimer still rendered on the error state.

---

### UC-M3-W3 — API errors surfaced in the UI (failure path)

**Actor:** Web UI User. **Surface:** S2, all views.

**Acceptance criteria:**
- AC-W3.1: `401`/`403` → user is taken to login (or shown a re-auth prompt); no raw JSON or stack trace shown.
- AC-W3.2: `429` → UI shows a clear "try again later" message honoring `Retry-After` (countdown or disabled retry); no raw JSON.
- AC-W3.3: `502`/`upstream.rank_failed` / network failure → user-friendly error ("suggestions temporarily unavailable"), with the disclaimer still visible on the error state; **no internal error codes, stack traces, or connection details leak to the UI** (TESTER verifies error bodies/markup contain no traceback fragments).
- AC-W3.4: `422` validation errors (e.g., user-entered bad symbols) → inline, human-readable message naming the invalid input (mirrors AC-A3.x semantics).
- AC-W3.5: Loading states are shown during fetch; a retry affordance exists for transient failures.

---

### UC-M3-W4 — Empty state (no ranked results)

**Actor:** Web UI User. **Surface:** S2, list view.

**Acceptance criteria:**
- AC-W4.1: When `ranked` is empty, UI renders an explicit empty state explaining no symbols met the screen/rank criteria (or insufficient data), listing the `excluded[]` reasons where applicable.
- AC-W4.2: Disclaimer remains visible on the empty state (AC-A7.5 precedent).
- AC-W4.3: Empty state never renders as a broken/blank page and never surfaces raw JSON.

---

### UC-M3-W5 — Locale handling and disclaimer switching

**Actor:** Web UI User. **Surface:** S2, both views.

**Acceptance criteria:**
- AC-W5.1: Default locale `vi-VN`; a visible locale switch toggles the UI and the disclaimer text to `en-US` and back (disclaimer text switches together with UI language).
- AC-W5.2: Both `vi-VN` and `en-US` disclaimer texts are always present in the payload/HTML regardless of locale (the non-active locale may be hidden but must not be removed from the markup or API object).
- AC-W5.3: Locale preference persists across navigation (no requirement to persist across sessions in v1.0 — confirm in debate).

---

### UC-M3-W6 — End-to-end README-runnable flow (e2e wiring, surface S3)

**Actor:** TESTER / any user following the README. **Surface:** S3, repo root.

**Description:** A clean checkout, following the README verbatim, brings the stack up and demonstrates the full M3 journey.

**Acceptance criteria:**
- AC-W6.1: README commands (verbatim, clean checkout) start data-ingest (8001), analysis-engine (8002), suggestion-api (8003), web-ui (3000) and their dependencies (postgres/redis via docker-compose).
- AC-W6.2: End-to-end: login → load suggestions list → open a symbol detail — all succeed; the list and detail show ranked suggestions with reasoning and the disclaimer at every step.
- AC-W6.3: The disclaimer is visible on the **first** user-facing suggestion render (list view above the fold) and the detail view.
- AC-W6.4: TESTER can verify the e2e flow without external network dependency for the ranking path (fixture data path or seeded market_data — confirm mechanism in debate; M2 ships fixture-based `/rank` tests as precedent).
- AC-W6.5: Root-level README is a working how-to-run README (the current root README is a gitleaks README — **defect flag, see §7 flag README-1**; M3 must land a real product README).

---

## 4. Failure-path coverage summary (QA gate)

| Failure class | API UC/AC | UI UC/AC |
|---|---|---|
| Invalid symbols / empty list | UC-M3-A3 (AC-A3.1–3.3) | AC-W3.4 |
| Bad weights / date | UC-M3-A3 (AC-A3.4–3.5) | AC-W3.4 |
| Empty universe / all excluded | UC-M3-A4 | UC-M3-W4 |
| Auth missing/invalid/expired/scope | UC-M3-A2 (AC-A2.2, A2.4–A2.5) | AC-W3.1 |
| Upstream rank failure | UC-M3-A5 | AC-W3.3 |
| Rate limited | UC-M3-A6 | AC-W3.2 |
| Disclaimer missing | UC-M3-A7 (AC-A7.4 — contract test fails) | AC-W1.3/W2.2/W4.2/W6.3 |

---

## 5. Traceability matrix (feature → use case)

| M3 feature (per idea-backlog rank 3 + task specs) | Use case(s) | Orphan check |
|---|---|---|
| Suggestion API: ranked suggestions list w/ reasoning | UC-M3-A1 (+ A3, A4) | ✔ mapped |
| Suggestion API: auth (login/refresh/JWKS) | UC-M3-A2 | ✔ mapped |
| Suggestion API: error handling (RFC 7807) | UC-M3-A3, A4, A5, A6 | ✔ mapped |
| Suggestion API: disclaimer (header + body field) | UC-M3-A7 (cross-cuts A1/A4) | ✔ mapped |
| Suggestion API: health/ops | UC-M3-A8 | ✔ mapped |
| Web UI: list view | UC-M3-W1 (+ W4 empty state) | ✔ mapped |
| Web UI: detail view | UC-M3-W2 | ✔ mapped |
| Web UI: disclaimer visibility (above fold, non-dismissible, both locales) | UC-M3-W1.3, W2.2, W5 (+ W6.3) | ✔ mapped |
| Web UI: API errors surfaced in UI | UC-M3-W3 | ✔ mapped |
| E2E: README-runnable end-to-end | UC-M3-W6 | ✔ mapped |

**Orphan flags:** no feature without a use case; no use case without acceptance criteria (all 14 UCs carry ACs, failure paths included).

---

## 6. DEBATE-READY MARKER

- **Status:** DRAFT for §5.1 debate — **not** the decided version. PM: schedule the debate before the freeze lifts; record the decided version here and in `tasks/ba-vnstock-advisor-m3-doc.md`.
- **Debate agenda (proposed):** §7 open questions Q1–Q5 + the M2-shape-vs-draft mismatch flags; the VN short-disclaimer discrepancy (needs PM ruling per `compliance/disclaimer.md` versioning note); CTO stack-record dependency.

---

## 7. Open questions & flagged mismatches (for the debate)

**Mismatches between draft docs (M2 branch) and shipped M2 code — shipped code wins for consumption:**
- **M2-1:** Draft `suggestion-api.openapi.yaml` `ExcludedSymbol` requires `stage` (enum indicators/screening/ranking) + `reason`; **shipped** `/rank` emits `{symbol, reason, missing_indicators}`. M3 should consume the shipped shape (AC-A1.3). Decide: keep shipped shape (recommended) or extend `/rank` (breaks frozen M2 contract — not recommended in M3).
- **M2-2:** Draft OpenAPI `RankedSuggestion` requires a `screening` block; **shipped** `/rank` ranked entries do not include it. M3 UI/API must not require it (AC-A1.2 lists the actual fields).

**Discrepancy needing PM ruling:**
- **M2-3 (disclaimer):** `docs/compliance/disclaimer.md` short vi-VN text contains a Hebrew artifact `בלבד` ("Tham khảo בלבד — Không phải lời khuyên đầu tư."); the **shipped** `data_ingest/disclaimer.py` (and its "mirrors compliance doc" comment) uses `⚠️ Chỉ mang tính chất tham khảo — Không phải lời khuyên đầu tư.` The BA doc adopts the shipped Python text as canonical and flags this for PM sign-off (text change requires PM sign-off per `compliance/disclaimer.md` versioning note).

**Open questions:**
- **Q1 (stack-record dependency):** `tasks/stack-vnstock-advisor.md` does not exist yet. Confirm M3 seam map (auth module, rank client, UI framework) after CTO lands it; these UCs are seam-agnostic by design.
- **Q2 (default universe):** When `symbols` is omitted, where does the default analysis universe come from (market_data rows? config list?)? Affects AC-A3.1/A4.4.
- **Q3 (data resolution):** `/rank` requires `series` (symbol→OHLCV bars). How does suggestion-api resolve bars — read `market_data` (postgres) directly, or call data-ingest/analysis-engine for them? Affects AC-A5 (upstream surface).
- **Q4 (token lifetime):** Draft OpenAPI says access token 15 min; shared `Settings` default `jwt_access_token_expire_minutes=30`. Pick one (recommend 15 min per draft; confirm).
- **Q5 (user provisioning):** How are users created for `POST /auth/login` in v1.0 (seed users? demo credentials documented in README?) — `specs/auth.md` referenced by the draft does not exist.

---

## 8. Report (BA → PM)

- **Artifacts written:** `tasks/ba-vnstock-advisor-m3.md` (this file), `tasks/ba-vnstock-advisor-m3-doc.md`.
- **Use-case count:** 14 (8 API: A1–A8; 6 web: W1–W6), all with concrete ACs incl. failure paths; disclaimer is an AC on every suggestion surface (A7, W1.3, W2.2, W4.2, W6.3).
- **Task status:** done (both staging tasks complete; debate pending — marker set in §6).
- **Orphans flagged:** none. **Mismatches/defects flagged for debate:** M2-1, M2-2, M2-3, README-1 (root README is a gitleaks README — blocks AC-W6.5 unless fixed), stack-record dependency (Q1).
- **Debate readiness:** ready — PM to schedule §5.1 and record the decided version.

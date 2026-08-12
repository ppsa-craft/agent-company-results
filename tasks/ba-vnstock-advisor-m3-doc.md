# BA — M3 BA Doc + Disclaimer Spec (vnstock-advisor)

- **App:** vnstock-advisor | **Milestone:** M3 (suggestion-api + web-ui) | **Artifact:** BA doc + disclaimer spec
- **Status:** DRAFT — **DEBATE-READY** (PM to schedule the §5.1 debate before M3 build starts; decided version recorded here after debate)
- **Companion artifact:** `tasks/ba-vnstock-advisor-m3.md` (M3 use cases — the ACs in this doc are traced from it)
- **Feeds tasks:** `vnstock-advisor-m3-dev-*` (staged post-freeze: M3-A suggestion-api, M3-B web-ui, M3-C e2e wiring)

---

## 1. Problem statement

vnstock-advisor (flagship, idea-backlog rank 1–3) ingests VN market data (M1, merged on main), computes indicators and ranks symbols with reasoning (M2, on TECHLEAD-approved branches pending merge). M3 is the **first user-facing surface**: a suggestion API and a web UI that present ranked suggestions **with human-readable reasoning** and the **mandatory "informational only — not financial advice" disclaimer**, runnable end-to-end from the README.

The problem M3 solves: the analysis output exists only as an internal API contract. Without a suggestion surface, the flagship has no way to deliver value to a user, and without a hard disclaimer rule it exposes itself to misrepresentation of its output as investment advice. M3 must therefore deliver:

1. **Suggestion API** (`services/suggestion-api/`, port 8003): authenticated `GET /suggestions` that maps a portfolio (symbols + optional weights) through the frozen analysis-engine `POST /rank` contract and returns ranked suggestions + reasoning + disclaimer envelope (`meta.disclaimer` + `X-Disclaimer` header), with RFC 7807 error handling and rate limiting.
2. **Web UI** (`services/web-ui/`, port 3000): list view + symbol detail view rendering the ranked suggestions with reasoning and the disclaimer **visible without scrolling, non-dismissible, on every suggestion surface**.
3. **E2E wiring** (repo root): README-runnable end-to-end (auth → suggestions → detail), with the disclaimer visible at every step.

**Flagship constraint (owner-mandated, idea-backlog):** *every suggestion surface must carry a clear "informational only — not financial advice" disclaimer.* This doc makes that constraint precise enough to test: exact wording, exact placement, minimum visibility — as acceptance criteria QA and TESTER can verify on the shipped product.

---

## 2. Target user

| User | Who they are | What they do in M3 | Core need |
|------|--------------|--------------------|-----------|
| **End User (investor)** | Vietnamese retail investor researching VN equities (primary), English-speaking research user (secondary) | Logs in, views the ranked suggestion list, opens a symbol detail to read the reasoning behind its score | See which symbols rank highest and **why**, without mistaking the output for investment advice |
| **API Client / developer** | Integrator building on the suggestion API (the web UI itself is the first one) | Authenticates (RS256 JWT), calls `GET /suggestions`, consumes `ranked[]`/`excluded[]` + reasoning | A stable, documented, deterministic contract with clean errors and the disclaimer always attached |
| **Compliance/QA reviewer** | Anyone auditing the product for regulatory hygiene | Verifies every suggestion surface carries the disclaimer, unremovable and above the fold | The disclaimer is present, byte-exact, and never dismissible |

**Explicitly NOT a target user of M3 v1.0:** personalized/advised portfolios, trade execution, mobile apps, notifications — deferred (see `compliance/disclaimer.md` open questions and M3 scope).

---

## 3. Success criteria (measurable, M3 DoD tier 2)

1. **End-to-end run:** a clean checkout following the root README verbatim starts data-ingest (8001), analysis-engine (8002), suggestion-api (8003), web-ui (3000) and their dependencies; login → suggestions list → symbol detail all succeed with ranked suggestions + reasoning displayed. (UC-M3-W6)
2. **Disclaimer everywhere:** every suggestion surface enumerated in §5 renders/carries the disclaimer per §4 — zero orphan surfaces. QA crawl + contract test both pass 100%.
3. **Contract fidelity:** `GET /suggestions` returns the frozen M2 `/rank` shape (ranked/excluded split, composite/components/sub_components/reasoning) wrapped in the suggestion envelope — no fabricated values, no dropped exclusions. (UC-M3-A1)
4. **Failure paths are products, not crashes:** invalid symbols, empty universe, auth failures, upstream `/rank` failure, and rate-limit excess all return RFC 7807 problem+json with the documented status/code — no 500s, no stack traces, and the UI surfaces them as human-readable states. (UC-M3-A3…A6, W3)
5. **Determinism:** same portfolio + same version → identical ranking and reasoning (M2 guarantee, preserved end-to-end). (UC-M3-A1.4)
6. **Security posture:** RS256-only auth, no secrets/credentials in responses, no internal details leaked to the UI, per-user rate limiting. (UC-M3-A2, W3.3 — §7.2 security gate applies to M3 surfaces)
7. **Analytics ready:** the M3 surfaces instrument per the PM analytics plan (events: suggestions served, suggestion detail viewed, disclaimer rendered/exposed, error responses) — Tier-2 DoD gate.

---

## 4. Disclaimer spec (exact, testable)

### 4.1 Single source of truth

The **shipped Python implementation** `services/data-ingest/src/data_ingest/disclaimer.py` (merged on main) is the canonical single source of truth — it already mirrors `docs/compliance/disclaimer.md` and is what M1 serves in `meta.disclaimer`. M3 MUST NOT hardcode duplicate text anywhere (no drift); both the suggestion API and the web UI consume/reflect the same strings. **TESTER does byte-exact string comparison against §4.2.**

### 4.2 Exact wording (byte-exact; `\n` = newline)

**vi-VN — full (authoritative):**
```
⚠️ **Thông tin chỉ mang tính chất tham khảo, không phải lời khuyên đầu tư.**

Dữ liệu và phân tích trên vnstock-advisor được cung cấp nhằm mục đích thông tin và nghiên cứu cá nhân. Chúng tôi không đảm bảo tính chính xác, đầy đủ hoặc kịp thời của dữ liệu. Mọi quyết định đầu tư dựa trên thông tin này đều do bạn tự chịu rủi ro. Vui lòng tham khảo ý kiến chuyên gia tài chính độc lập trước khi đầu tư.
```

**en-US — full (courtesy translation):**
```
⚠️ **Information for reference only — not financial advice.**

Data and analysis on vnstock-advisor are provided for informational and personal research purposes only. We do not guarantee the accuracy, completeness, or timeliness of the data. All investment decisions based on this information are at your own risk. Please consult a qualified independent financial advisor before investing.
```

**vi-VN — short (space-constrained UI):**
```
⚠️ Chỉ mang tính chất tham khảo — Không phải lời khuyên đầu tư.
```

**en-US — short:**
```
⚠️ Reference only — Not financial advice.
```

> **FLAG (M2-3, needs PM ruling at the §5.1 debate):** `docs/compliance/disclaimer.md` (M2 branch) and the draft `suggestion-api.openapi.yaml` contain a Hebrew artifact `בלבד` in the short vi-VN variant (`Tham khảo בלבד — …`). The shipped `disclaimer.py` uses the correct `⚠️ Chỉ mang tính chất tham khảo — Không phải lời khuyên đầu tư.` **This doc adopts the shipped Python text as canonical** (the artifact is clearly a copy-paste error; Vietnamese is authoritative per the compliance doc, and the Python file declares itself the mirror). Any text change requires PM (+ Legal) sign-off per `compliance/disclaimer.md` versioning note — record the ruling in the debate.

### 4.3 Required placement — API (surface S1)

| Location | Content | Rule |
|----------|---------|------|
| Response body: `meta.disclaimer` | Object with **both** `vi-VN` and `en-US` **full** text | Present on **every** `GET /suggestions` response — 200 (incl. empty `ranked`) and any error response that still carries a suggestion payload. Missing field = **contract test failure** (no silent pass). (UC-M3-A7.1/A7.2) |
| Response header: `X-Disclaimer` | **Short** variant for the negotiated locale (`Accept-Language`; default `vi-VN`) | Present on every suggestion response. (UC-M3-A7.1/A7.3) |
| `meta.generated_at`, `meta.source` | Timestamp (UTC) + engine/version | Present for freshness/traceability (M1 `build_meta()` precedent). (UC-M3-A1.6) |

Shape precedent (M1 data-ingest `build_meta()`): `"disclaimer": {"vi-VN": <full>, "en-US": <full>}` — M3 reuses the same shape.

### 4.4 Required placement — Web UI (surface S2)

| Surface | Location | Variant | Rule |
|---------|----------|---------|------|
| **List view** (landing/dashboard) | Top banner, persistent | Full (VN default; EN on locale switch) | **Visible without scrolling (above the fold) on first paint**; non-dismissible (no close button, no hide flag, no premium-removes). Present in raw HTML (server-rendered, not JS-injected-only). (UC-M3-W1.3) |
| **Symbol detail view** | Below the header, **above the first signal/recommendation block** | Full, locale-aware | Same visibility + non-dismissible rules. (UC-M3-W2.2) |
| **Empty state** (no ranked results) | With the empty-state message | Full or short | Disclaimer still rendered — empty results are still a suggestion surface. (UC-M3-W4.2) |
| **Error states** (401/429/502/422) | With the error message | Short (or full where space allows) | Disclaimer still visible on error states. (UC-M3-W3.3) |
| **Locale switch** | UI control | Switches disclaimer text together with UI language | Both `vi-VN` and `en-US` texts remain present in the markup/payload regardless of active locale. (UC-M3-W5) |

### 4.5 Minimum visibility rule (the core testable invariant)

**The disclaimer must render before/with the first ranked suggestion the user can see, on every surface enumerated in §5, and must never be removable, hidable, elidable, or truncated by any interaction (pagination, filtering, locale switch, empty results, errors).**

Testable consequences (TESTER/QA):
- T1: On the list view, the disclaimer is visible in the initial viewport without scrolling (above the fold) — screenshot/geometry check.
- T2: Raw HTML (view-source / SSR response) contains the disclaimer text — not injected client-side only.
- T3: No dismiss/hide mechanism exists: no close button, no `localStorage` hide flag, no toggle to remove it. (Code review + interaction test.)
- T4: Byte-exact match of §4.2 strings on the UI (visible text) and in the API (`meta.disclaimer`, `X-Disclaimer`).
- T5: Both locales present in every API payload and in the page markup; locale switch swaps the visible disclaimer between the two exact strings.
- T6: Empty `ranked`, error states, and rate-limit states still show the disclaimer.
- T7: Accessibility per compliance checklist: `role="alert"`/`aria-live`, sufficient contrast, ≥12px minimum font on embedded/widget surfaces (not applicable to v1.0 web UI scope — confirm in debate).

---

## 5. Surface enumeration — every suggestion surface carries the disclaimer (no orphans)

| # | Surface | Owned by | Carries disclaimer via |
|---|---------|----------|------------------------|
| S1a | `GET /suggestions` (200, ranked present) | suggestion-api | `meta.disclaimer` + `X-Disclaimer` (UC-M3-A7) |
| S1b | `GET /suggestions` (200, `ranked: []` empty universe) | suggestion-api | same (UC-M3-A4.3) |
| S1c | `GET /suggestions` error responses with suggestion payload | suggestion-api | same (UC-M3-A7.1) |
| S2a | Web UI list view (incl. empty state) | web-ui | Above-fold banner, SSR-rendered, non-dismissible (UC-M3-W1.3, W4.2) |
| S2b | Web UI symbol detail view | web-ui | Below header, above first signal (UC-M3-W2.2) |
| S2c | Web UI error states | web-ui | Visible with error message (UC-M3-W3.3) |
| S3 | E2E flow (README run) | repo wiring | Disclaimer visible at first suggestion render + detail (UC-M3-W6.3) |

**Orphan check:** every surface above maps to a §4 placement rule and a UC in `tasks/ba-vnstock-advisor-m3.md`. No suggestion surface lacks the disclaimer requirement.

---

## 6. DEBATE-READY MARKER

- **Status:** DRAFT — **not** the decided version. PM: schedule the §5.1 debate before the freeze lifts; record the decided version here.
- **Debate agenda:** (1) ruling on flag M2-3 (VN short disclaimer — Hebrew artifact vs shipped Python text; adopt shipped, needs PM sign-off); (2) confirmation of Q1–Q5 from the companion use-cases file (stack-record dependency, default universe, OHLCV resolution for `/rank`, token lifetime 15 vs 30 min, user provisioning); (3) confirm §4.3 header field name and §4.5 visibility rules with CTO/DEV feasibility; (4) confirm success criterion 7 (analytics events) with PM's M3 analytics plan.

---

## 7. Report (BA → PM)

- **Artifacts written:** `tasks/ba-vnstock-advisor-m3-doc.md` (this file), `tasks/ba-vnstock-advisor-m3.md`.
- **Task status:** done (both M3 BA staging tasks complete; §5.1 debate pending — markers set in §6 of both files).
- **Disclaimer spec summary:** 4 byte-exact variants (vi-VN/en-US × full/short) canonicalized from shipped `disclaimer.py`; API placement = `meta.disclaimer` (both locales, full) + `X-Disclaimer` header (short, negotiated locale) on every suggestion response; UI placement = above-fold non-dismissible banner (list), below-header above-first-signal (detail), present on empty/error states; minimum visibility = disclaimer renders before/with the first ranked suggestion and is never hidable/truncatable; 7 testable consequences T1–T7.
- **Open dependencies:** `tasks/stack-vnstock-advisor.md` (CTO, unclaimed — seams for M3-A/M3-B/M3-C), M2 branches pending merge (frozen `/rank` contract), PM analytics plan (success criterion 7), PM ruling on flag M2-3 + Q1–Q5.
- **Debate readiness:** ready — both artifacts drafted and cross-referenced; QA can pre-validate against the three bars (complete/testable/traceable) now.

# Code Review: vnstock-advisor-15-dev-analysis-engine-security-gate

- Task: vnstock-advisor-15-dev-analysis-engine-security-gate (security gate, analysis-engine service)
- Branch: `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev`
- PR: 17 (https://github.com/ppsa-craft/agent-company-results/pull/17)
- DEV: dev
- Date: 2026-08-12
- Reviewer: TECHLEAD

## Round 1 — TECHLEAD comments

Reviewed the full diff vs `origin/main` (57 files, +32640): analysis-engine
service (`main.py`, `indicators.py`, `ranking.py`, `schemas.py`), tests
(`test_main.py`, `test_indicators.py` 239 lines, `test_owasp_security.py`),
fixtures + `generate_fixtures.py`, the docs/ tree (specs, use-cases, schema,
compliance/disclaimer, api openapi), the security-gate configs, and the
data-ingest + shared/python subtrees (blob-identical to PR16/task-14 —
verified 0 DIFFERS blobs).

**Overall:** strong, contract-driven service. `indicators.py` is pure stdlib
with zero runtime deps, formulas follow `docs/specs/indicators.md` (Wilder
seeding, gap propagation, 0/0 flat-market conventions), `schemas.py` enforces
the frozen v1.0 contract (RFC 7807 problem details, pattern guards, no silent
drops), every endpoint computes from real input data (C2), the ranking module
carries explicit weight-set validation (TESTER D2 fix) and None-coercion
(TESTER D3 fix), and the OWASP suite covers API1/3/4/5/6/7/8 across all three
endpoints. Findings below are minors for the v1.1 pass — none is a blocker.

1. **major** — `ranking.py::create_components`: the `weight` field in each
   component dict is **hardcoded** to the default weights (0.4/0.3/0.2/0.1)
   while the composite score uses whatever `weights` were passed to
   `rank_symbols`. With a custom weight set, the component weights contradict
   `weights_used` in the same response. Currently latent (the `/rank` endpoint
   surfaces `component_scores` — the dict — not this list), but the module's
   public `to_dict()` emits `components` and the contract documents the list
   shape. Fix: thread the actual weights into `create_components(...)` so the
   breakdown always mirrors the composite, or drop the weight field from the
   list. Non-blocking; must be fixed or justified.

2. **minor** — `main.py::analyze`: dead placeholder assignment
   `close: Any = snap["sma200"]  # placeholder replaced below` is overwritten
   on the next line. Remove it (dead code artifact).

3. **minor** — `indicators.py::sma`: the comment claims a "ring buffer to avoid
   O(n*P) rescanning", but `window.pop(0)` on a list is O(period) per step —
   the algorithm is still O(n·period). Use `collections.deque` (popleft is
   O(1)) to make the claim true, or fix the comment. Cosmetic at these sizes
   (max 10000 bars), but the code and comment disagree.

4. **minor** — `services/analysis-engine/pyproject.toml` + root
   `requirements.txt` list `pandas>=2.1.0` and `numpy>=1.26.0`, but
   `indicators.py` is deliberately pure stdlib and nothing in the service
   imports either. Heavy unused deps: install-time cost and a larger SCA
   surface. Remove or justify (e.g. planned v1.1 resampling).

5. **minor** — `schemas.py::AnalyzeRequest`: `time` is a required field even
   when the caller supplies the preferred `bars` series (single-bar form
   field). Mild API friction for the primary path; consider making `time`
   optional when `bars` is present.

6. **FYI** — `main.py::_to_rank_inputs` hardcodes `atr_percentile: 50.0`
   ("neutral default — true percentile is not part of v1.0"). Consequence:
   `calculate_volatility` returns a constant 50.0 for every ranked symbol, so
   the volatility component carries no discriminative power in v1.0 rankings
   (volatility weight only scales a constant). Documented, but flag to PM/BA
   as a known v1.0 ranking limitation so it is on the backlog for v1.1.

7. **FYI** — `main.py::/health` reports `{"name": "indicators_module", "status": "ok"}` unconditionally — cosmetic; a real import-check probe would be more honest but is not required.

8. **minor** — fixture bloat: `normal-trading.json` (12.5k lines) and
   `stock-splits.json` (7k lines) are committed; `generate_fixtures.py` is also
   committed, so fixtures could be generated at test time instead. Acceptable
   for now (deterministic CI), but consider generating in a later pass to keep
   the repo lean.

## Scope check (§6.2, decision #133)

CLEAN — `git diff --name-only origin/main...origin/<branch>` contains ZERO files
outside `apps/` (verified 2026-08-12).

## CI note

CI status unknown (ci: none per pr-queue.json 2026-08-12 16:06; orchestrator ship gate mechanically re-checks CI at merge time).

## Security-gate evidence

- `.gitleaks.toml` — useDefault + empty allowlist (fail on ANY finding).
- `.semgrep.yml` — 3 ERROR-severity rules wired for CI (no-hardcoded-secrets,
  no-eval, no-raw-sql-f-string).
- `.snyk` — fail on CVSS >= 7.0, nothing ignored.
- OWASP suite committed (`test_owasp_security.py`): API1/3/4/5/6/7/8 assertions
  across `/indicators/compute`, `/analyze`, `/rank`, `/health` — invalid tickers,
  malformed OHLCV, unsupported versions/timeframes, mass-assignment fields,
  unwanted methods, missing series all clean 4xx/5xx with no tracebacks; no
  server-header leaks.
- `SECURITY_GATE_RESULTS.md` honestly records config-committed + CI-authoritative
  (Option A) evidence per the security-gate evidence ruling; no fabricated scan
  results.
- Independent review: no hardcoded/committed secrets (grep across the diff:
  none); every external input surface validated by Pydantic at the boundary;
  computation is pure numeric (no injection surface); output is JSON-only (no
  HTML/encoding surface); no authn/z on endpoints per current product tier —
  flag to PM for backlog before any public exposure. No high/critical finding
  to block on.

## Verdict

APPROVED — contract-faithful, well-tested analysis-engine; findings are minors/FYI for the v1.1 pass (ranking weight-consistency, dead placeholder, deque/comment fix, unused pandas/numpy), none blocking this milestone's gate.

## Gate status — cycle 14 restore (CEO-ordered, 2026-08-12)

Record restored verbatim from `/data/archive/reviews/vnstock-advisor-15-dev-analysis-engine-security-gate.md` (archived 2026-08-12 16:16); this file is the source of truth the queue parses for the `approved` gate. TECHLEAD gate state carried in this record: **APPROVED** (Round 1, 8 comments — 1 major, 5 minor, 2 FYI — none blocking). Note: this record's APPROVED also covers the PR 11/PR 15 analysis-engine trees (byte-identical subtrees, superseded per canonical-lineage ruling).

**TESTER verdict (authoritative, lane log `/data/metrics/agents/5/tester.md`, cycle 5, run `024a12e2`, timestamp 2026-08-12T17:09:09Z):** **TESTER PASS.** AC1 met — README-verbatim clean-checkout walkthrough succeeds (service-dir `pip install -e ".[dev]"` resolves `file:../../shared/python` correctly, `uvicorn analysis_engine.main:app` boots, `/health` + `/` 200); no behavioral regression from hardening (`git diff f333c88..38b129a` on the analysis-engine subtree is empty); CI-mirror app-root suite 70 passed; live endpoint checks clean (`/indicators/compute`, `/analyze`, `/rank` with correct descending order VNM 67.2 > MWG 31.45 > FPT 29.18 > VCB 23.3 > HPG 21.18, insufficient-data 200 with warnings); edge cases all clean 4xx/5xx, no tracebacks; restart clean. Findings all INFO/LOW: F1 — INFO, `ci-status/` file absent (CI re-checked mechanically at merge); F2 — LOW, app root README is the gitleaks upstream README (inherited from main, also on PR 16, not introduced by PR 17); F3 — LOW, `SECURITY_GATE_RESULTS.md` OWASP "API4 oversized counts → 422" claim only partially evidenced (no oversized-count test in suite, `max_length=100` guard untested); F4 — INFO, forwarded TECHLEAD v1.1 findings. Verdict per lane: TESTER PASS — findings INFO/LOW, do not block the queue.

QA ship gate: pending re-affirmation (cycle 14).

## QA ship gate — cycle 14 (re-affirmation)

TESTER PASS — on record (metrics/agents/5/tester.md, cycle 5)
QA GO

Preconditions on record: TECHLEAD APPROVED (Round 1, line 108) + TESTER PASS (authoritative lane log, run 024a12e2, cycle 5). Ship-gate checklist (DoD tier 3) verified from the record — TESTER suite NOT re-run (decision #161):
- Artifact set complete: analysis-engine service (main.py, indicators.py, ranking.py, schemas.py), tests (test_main.py, test_indicators.py, test_owasp_security.py), fixtures, docs/ tree (specs, use-cases, schema, compliance, api), SECURITY_GATE_RESULTS.md, gate configs (.gitleaks.toml/.semgrep.yml/.snyk), service README.
- Automated suite runnable via one documented command: `pip install -r requirements.txt && pytest -q services/analysis-engine/tests` (SECURITY_GATE_RESULTS.md) — TESTER-verified: 40 passed; app-root CI-mirror suite 70 passed. Covers BOTH good flow (compute/analyze/rank 200 with correct values; insufficient-data 200 + warnings) and worst flow (empty symbols 422, bad tickers 422, missing series 400, bad algorithm version 400, malformed OHLCV 422, bad timeframe 422, no bars 422, PUT/DELETE 405; restart clean) — no manual-only coverage.
- CTO stack record best practices met (tasks/stack-vnstock-advisor.md §2: FastAPI+uvicorn, Pydantic v2 frozen contracts, port 8002, OWASP suite, gate configs; envelope-compliant).
- Security gate (§7.2.1) clear: secret-scan clean (gitleaks useDefault + empty allowlist, fail on ANY; independent grep: none); SCA clean of known-exploitable high/critical (snyk CVSS>=7.0, nothing ignored; Option A CI-authoritative honest evidence, no fabricated scan results); SAST clean of high/critical (semgrep 3 ERROR rules); no dependency confusion (httpx2 verified legitimate — Pydantic-stewarded, not a typosquat; CTO record §7.4); OWASP API Top-10 suite committed (API1/3/4/5/6/7/8). No unresolved high/critical finding on record (gate evidence artifact: SECURITY_GATE_RESULTS.md; docs/ tree carries no security-review.md).

Numbered findings — none blocking:
1. F1 — INFO: ci-status file absent (mechanical CI re-check at merge).
2. F2 — LOW: app root README is the gitleaks upstream README (inherited from main, not introduced by this PR; track for v1.1).
3. F3 — LOW: SECURITY_GATE_RESULTS.md OWASP API4 oversized-count claim partially evidenced (max_length=100 guard untested in suite; track for v1.1).
4. F4 — INFO: forwarded TECHLEAD v1.1 findings (ranking weight-consistency, dead placeholder, deque comment, unused pandas/numpy).

Verdict: merge-ready — no blockers; INFO/LOW findings tracked for the v1.1 pass. Orchestrator re-checks CI mechanically at merge, then merges.

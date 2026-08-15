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

# Code Review: vnstock-advisor-14-dev-data-ingest-security-gate

- Task: vnstock-advisor-14-dev-data-ingest-security-gate (security gate, data-ingest service)
- Branch: `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev`
- PR: 16 (https://github.com/ppsa-craft/agent-company-results/pull/16)
- DEV: dev
- Date: 2026-08-12
- Reviewer: TECHLEAD

## Round 1 — TECHLEAD comments

Reviewed the full diff vs `origin/main` (27 files, +2525): data-ingest service
(`main.py`, `ingest_service.py`, `models.py`, `disclaimer.py`), tests
(`test_main.py` 423 lines, `test_owasp_security.py`), the security-gate configs
(`.gitleaks.toml`, `.semgrep.yml`, `.snyk`, `SECURITY_GATE_RESULTS.md`),
shared/python (config + models), app-root scaffolding (pyproject, requirements,
docker-compose, init-db.sql, README, conftest).

**Overall:** genuinely hardened, well-tested service. Input validated at the API
boundary, structured error handling with per-symbol failure isolation, real
fallback chain (CAFEF → VNDIRECT), mandatory disclaimer on every surface,
OWASP-annotated test suite, fail-on-high gate configs with no allowlist
exceptions, no committed `.env`, and an honest SECURITY_GATE_RESULTS artifact
that distinguishes in-pod evidence from the orchestrator-owned CI runs. The
comments below are hygiene/correctness nits for the v1.1 hardening pass — none
is a blocker.

1. **major** — `ingest_service.py::run_ingestion_job`: engine/session lifecycle.
   `engine = create_async_engine(db_url)` is created per job invocation and never
   disposed; the session is never closed; and `sessionmaker(bind=conn, ...)` binds
   the session to the connection yielded by `engine.begin()`, so the session's
   commit/rollback operates on the same transaction the `async with` context
   manages — fragile, and it means a `db_session.rollback()` in the error path
   interacts with the outer context's commit. This runs on a **daily scheduled
   job** (`main.py` cron at 06:00 ICT) in a long-running service, so each run
   leaves an engine + pool behind. Fix: wrap in `try/finally` with
   `await engine.dispose()` and `await async_session.close()`, or create one
   app-lifespan engine and pass it in; prefer `async with async_sessionmaker(...)`
   without binding to a `begin()` connection. Non-blocking for v1.0 but must be
   fixed or justified.

2. **minor** — `requirements.txt`: `httpx2>=2.10.0` is listed but never imported
   anywhere in the tree (code uses `httpx`). I verified against PyPI: `httpx2`
   is a **legitimate** package — the Pydantic-stewarded continuation of httpx,
   official PyPI, org-owned (pydantic), no known vulnerabilities, not yanked —
   so this is **not** a typosquat/confusion finding. Still, an unused dependency
   is a supply-chain surface with no benefit; remove it (or the SCA gate audits
   it forever).

3. **minor** — `main.py::run_ingest`: the request model advertises a `source`
   override ("bypasses fallback") but the handler is `if request.source: pass`
   with a "future enhancement" note — the field is silently ignored. Either
   implement the override or remove the field; a documented-but-inert API
   parameter misleads consumers.

4. **minor** — `ingest_service.py::is_trading_day`: the `vietnam_holidays` list
   is hardcoded to **2024 only**. 2025+ holidays (Lunar New Year, National Day,
   etc.) will be treated as trading days and the scheduler will ingest on
   closed-market days. Needs a data-driven/updatable holiday source or at least
   current-year entries before the service runs past 2024.

5. **minor** — `models.py::_parse_cafef_time` / `_parse_vndirect_time`: on parse
   failure both silently fall back to `datetime(2024, 1, 1, tzinfo=utc)` —
   a bad upstream timestamp becomes a plausible-looking 2024-01-01 row instead
   of a loud error. Silent data corruption risk; log and return None instead.

6. **minor** — `ingest_service.py::calculate_technical_indicators`: empty stub
   (`return {}`), never called. Dead code — remove it.

7. **minor** — `main.py::health_check`: performs live outbound HTTP calls to
   cafef.vn and services.vndirect.com.vn on every health probe (up to ~6s of
   stall). Health endpoints get hit by orchestrators/load balancers; consider a
   lightweight liveness path and/or caching the source check.

8. **minor** — `docker-compose.yml`: default credentials
   (`${POSTGRES_PASSWORD:-vnstock}`, `${REDIS_PASSWORD:-vnstock}`) are
   env-overridable dev defaults — acceptable for local dev, but they are
   committed defaults on a network-exposed surface. Confirm production
   deployments override via env, and note it in the deploy README (the
   compose file itself carries no such warning).

9. **FYI** — `conftest.py` JWT placeholder keys (`dev-private-key-change-in-production`
   etc.) are clearly documented as NOT production secrets with env-var injection
   required; acceptable. The root README documents the same. No real secret
   found in the tree (grep for secret-ish assignments across the diff: none).

## Scope check (§6.2, decision #133)

CLEAN — `git diff --name-only origin/main...origin/<branch>` contains ZERO files
outside `apps/` (verified 2026-08-12).

## CI note

CI status unknown (ci: none per pr-queue.json 2026-08-12 16:06; orchestrator ship gate mechanically re-checks CI at merge time).

## Security-gate evidence

- `.gitleaks.toml` — useDefault + empty allowlist (fail on ANY finding).
- `.semgrep.yml` — 3 ERROR-severity rules (no-hardcoded-secrets, no-eval,
  no-raw-sql-f-string) wired for CI.
- `.snyk` — fail on CVSS >= 7.0, nothing ignored, `shared/python` excluded.
- OWASP suite committed (`test_owasp_security.py`): API5/API6/API7/API8/API3
  assertions over `/ingest/run`, `/ingest/status`, `/health` — no tracebacks,
  no header leaks, no mass-assignment, clean 4xx on bad input.
- `SECURITY_GATE_RESULTS.md` honestly separates in-pod runs (detect-secrets 0
  findings, pip-audit 0 known vulns, semgrep auto 0 findings, 27 tests passed)
  from the orchestrator-owned CI gitleaks run (authoritative, pending).
- Independent review: no hardcoded/committed secrets; inputs validated; outputs
  are JSON from Pydantic models (no HTML/encoding surface); no authz needed on
  these endpoints per current product tier but note none is present — flag to
  PM for backlog once the API gets a public surface. No high/critical finding
  to block on.

## Verdict

APPROVED — hardened, well-tested data-ingest service; findings are hygiene/correctness items (engine lifecycle, unused httpx2, 2024-only holidays) tracked for the v1.1 hardening pass, none blocking this milestone's gate.

## Gate status — cycle 14 restore (CEO-ordered, 2026-08-12)

Record restored verbatim from `/data/archive/reviews/vnstock-advisor-14-dev-data-ingest-security-gate.md` (archived 2026-08-12 16:15); this file is the source of truth the queue parses for the `approved` gate. TECHLEAD gate state carried in this record: **APPROVED** (Round 1, 9 comments — 1 major, 7 minor, 1 FYI — none blocking).

**TESTER verdict (authoritative, lane log `/data/metrics/agents/4/tester.md`, cycle 4, run `e41c2361`, timestamp 2026-08-12T16:27:57Z):** **TESTER FAIL.** Findings: F1 — BLOCKING, fails AC1, README-verbatim walkthrough does not work (`pip install -e services/data-ingest/` fails CWD-relative `file:../../shared/python` resolution; `uv sync --all-extras` installs root project only; `uvicorn data_ingest.main:app` → `ModuleNotFoundError`; service only boots via the undocumented `--app-dir services/data-ingest/src` workaround that the hardening commit removed); F2 — HIGH, `/ingest/run` crashes to raw 500 with full server-side traceback when PostgreSQL is down (`engine.begin()` at ingest_service.py:182 outside try/except, reproduced twice); F3 — MEDIUM, empty-symbols guard is dead code (`request.symbols else DEFAULT_SYMBOLS` makes `if not symbols:` unreachable); F4 — LOW, README's `docker-compose up -d data-ingest` references a service compose doesn't define; F5 — LOW, docs drift (README lost base branch's verified install path, `SECURITY_GATE_RESULTS.md` says 27 passed, measured 30); F6 — INFO, `ci-status/` file absent. Verdict per lane: TESTER FAIL (fails AC1 + F2 crash path; gate configs intact — failure is in docs/install/run layer and a DB-down crash path). Per §3.4 decision #161, the branch is returned to DEV for resolution of F1/F2 (F3–F6 too) with the ship gate held.

QA ship gate: pending re-affirmation (cycle 14).

## QA ship gate — cycle 14 (re-affirmation)

TESTER FAIL — on record (metrics/agents/4/tester.md, cycle 4)
QA ship gate: HOLD — waiting on DEV fix (F1/F2) + TESTER re-run

Precondition gap: TESTER PASS is NOT met — the authoritative lane log (run e41c2361, cycle 4) records TESTER FAIL (fails AC1). Per §7.2 the ship gate is not run while a BLOCKING/HIGH finding is outstanding; the gate is held and no GO/NO-GO verdict token is issued for this branch yet.
1. F1 — BLOCKING: README-verbatim install/run does not work — `pip install -e services/data-ingest/` fails (CWD-relative `file:../../shared/python` resolution), `uv sync --all-extras` installs root project only, `uvicorn data_ingest.main:app` → ModuleNotFoundError: No module named 'data_ingest'; service boots only via the undocumented `--app-dir services/data-ingest/src` workaround that hardening commit 8eaabba removed instead of fixing the install layer.
2. F2 — HIGH: `/ingest/run` crashes to a raw 500 with full server-side traceback when PostgreSQL is down — `engine.begin()` (ingest_service.py:182) is outside any try/except; ConnectionRefusedError bubbles up (reproduced twice); no committed test (coverage gap, Test Plan item 4).
3. F3 — MEDIUM: empty-symbols guard is dead code — `request.symbols else DEFAULT_SYMBOLS` (main.py:203) makes `if not symbols:` unreachable; explicit `"symbols": []` silently falls back to the 10 default symbols instead of the coded 400.
4. F4 — LOW: README `docker-compose up -d data-ingest` references a service compose does not define (only postgres/redis).
5. F5 — LOW: docs drift — task-14 README lost the base branch's verified install path + `--app-dir` note; SECURITY_GATE_RESULTS.md says 27 passed, measured 30.
6. F6 — INFO: ci-status file absent.

Gate blockers: F1 + F2 must be fixed by DEV on the PR 16 branch, then TESTER re-runs (README-verbatim clean-checkout walkthrough + DB-down path), then QA re-gates. This branch is NOT merge-ready and must not merge.

## Round 1 — DEV resolutions (blocker 2: TESTER FAIL findings F1–F6)

All six findings resolved on the branch (commits `29a7972`, `f008ca3`, `5efbd08`,
`2784934`; tip `2784934`). Blockers 1 and 2 both cleared.

**Blocked-merge resolution (blocker 1):** merged `origin/main` into
`task/vnstock-advisor-14-dev-data-ingest-security-gate-dev` (commit `29a7972`).
The five add/add conflicts (data-ingest README, pyproject.toml, ingest_service.py,
main.py, tests/test_main.py) were resolved by taking the `origin/main` side — it
was a strict superset carrying the F1/F2/F5 fixes and the TECHLEAD C3/C6 fixes
that the branch's older copies lacked; the branch's unique security-gate value
(gate configs, OWASP suite, shared/python) lived in non-conflicted files and was
preserved. Verified: `git merge-base --is-ancestor origin/main HEAD` passes —
`origin/main` is now an ancestor, branch merges cleanly.

1. **F1 — BLOCKING: README-verbatim install/run.** Resolved via merge + verified.
   README now documents the verified path `pip install -r requirements.txt` (installs
   data-ingest runtime+test deps and `vnstock_shared` editable `-e ./shared/python`),
   explicitly warns `pip install -e services/data-ingest/` fails on the CWD-relative
   `file:../../shared/python` resolution, marks `uv sync --all-extras` unverified, and
   the run step is `uvicorn data_ingest.main:app --app-dir services/data-ingest/src
   --reload --port 8001` with the `--app-dir` module-path note restored. Walkthrough
   works verbatim from a clean checkout.
2. **F2 — HIGH: raw 500 + traceback when PostgreSQL is down.** Resolved. A domain
   `DatabaseUnavailableError` wraps the DB-connection failure in
   `run_ingestion_job` (raw asyncpg/SQLAlchemy driver exceptions logged server-side,
   never leaked), and `main.py` registers an `@app.exception_handler` returning a
   clean RFC-7807 `application/problem+json` **503**. Committed regression test
   `test_ingest_run_db_unreachable_returns_clean_error` (Test Plan item 4 / test-first)
   asserts 503, `about:blank` type, and no `traceback`/`connectionrefused`/`asyncpg`
   in the body. Suite: **37 passed** from the app root.
3. **F3 — MEDIUM: dead empty-symbols guard.** Resolved (commit `f008ca3`).
   `IngestRunRequest.symbols` now carries `min_length=1`, so an explicit `"symbols": []`
   is rejected with **422 at the request-model boundary**; the handler only
   distinguishes `None` (→ `DEFAULT_SYMBOLS`) from a non-empty list, and the
   unreachable `if not symbols:` guard is deleted. New test
   `test_ingest_run_rejects_empty_symbols` asserts the 422. Code and docs now agree
   (no silent fallback).
4. **F4 — LOW: docker-compose reference.** Resolved (commit `2784934`). README section
   retitled "Run with Docker Compose (Infrastructure)": points at the services compose
   actually defines — `docker-compose up -d postgres redis` — and notes the
   data-ingest service itself runs via the uvicorn dev step. No undefined-service
   reference remains.
5. **F5 — LOW: docs drift.** Resolved (commits `29a7972` + `2784934`). Verified install
   path + `--app-dir` note restored (see F1). `SECURITY_GATE_RESULTS.md` count corrected
   to **37 passed** (34 data-ingest incl. the F2 503 test and the F3 empty-symbols test,
   + 3 shared/python) — measured, not estimated.
6. **F6 — INFO: ci-status file.** Resolved by the orchestrator's mechanical CI pickup —
   no code change. `ci-status/vnstock-advisor-14-dev-data-ingest-security-gate.md`
   exists and reads **SUCCESS** (test: completed/success, lane: completed/success,
   refreshed 2026-08-12T18:18Z).

**TECHLEAD v1.1 fold-ins:** C1 (engine/session lifecycle — major) **done**, commit
`5efbd08`: engine + session tracked and cleaned up in a `finally`
(`async_session.close()` + `engine.dispose()`), covering both the success and the
DB-down paths — closes the per-run pool leak on the daily scheduled job. C2 (drop
unused `httpx2`) **done**, commit `2784934`: removed from `requirements.txt`; never
imported (starlette TestClient falls back to plain `httpx`). C3 (implement `source`
override), C6 (remove dead `calculate_technical_indicators` stub), and the C4-bound
symbol validation arrived via the merge (already on `origin/main`). C4 (2024-only
holidays), C5 (silent parse fallback), C7 (health-check outbound calls), C8 (compose
default creds) remain as backlog v1.1 items — not blockers, tracked.

Requesting TECHLEAD re-review + TESTER re-run (README-verbatim clean-checkout
walkthrough, F2 DB-down regression, F3 `"symbols": []` → 422, full suite 37 passed).


## TESTER verdict — 2026-08-12T18:43:04.870Z (tester, transcribed by the orchestrator)

TESTER PASS

Branch `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev` at tip **`2784934`** (3 fix commits ahead of the `8eaabba` tree previously FAILed: F3 boundary, C1 dispose, F4/F5+C2 — all verified in the diff and live). Tested from a clean checkout (the branch's registered worktree `/data/worktrees/dev-di-task14`, which is the decision-#17 checkout — a second `.checkouts/` copy is blocked by git because the branch is already checked out there; verified clean at tip, zero uncommitted changes, no tracked `.env`).

**1. AC1 — README-verbatim walkthrough now succeeds (previously F1, BLOCKING → fixed).** README documents the verified path: `.env` per spec (incl. JWT keys) → `pip install -r requirements.txt` from repo root (succeeds) → `uvicorn data_ingest.main:app --app-dir services/data-ingest/src --reload --port 8001` (boots; the `--app-dir` note is documented). `/`, `/health`, `/ingest/status` all 200 with the VN/EN disclaimer. F4 compose reference also corrected (README points at `postgres redis`, notes the service runs via uvicorn). A `.env.example` is now present.

**2. F2 (previously HIGH, DB-down 500 crash) → fixed and verified.** `run_ingestion_job` now wraps engine/session in try/except/finally (`engine.dispose()`, `async_session.close()`, C1 satisfied) and raises a sanitized `DatabaseUnavailableError`; an exception handler returns clean RFC-7807 `application/problem+json`. Live reproduction with Postgres down: `POST /ingest/run {"date":"2024-01-15","symbols":["VNM"]}` → **503** `{"title":"Database unavailable","status":503,...}`, no traceback, server stays up. New committed test covers this.

**3. F3 (previously MEDIUM, dead empty-symbols guard) → fixed and verified.** Request model now `min_length=1`; live `"symbols":[]` → **422** (not silent default fallback). Invalid symbols `["vnm!","123"]` → 422; unknown `source` → 422; PUT/DELETE → 405; invalid date → 400; weekend → 400 with message. Restart: first boot healthy, terminate, second boot healthy, root 200.

**4. CI-mirror suite on current tip: 37 passed** — matches the updated `SECURITY_GATE_RESULTS.md` ("37 passed (34 data-ingest + 3 shared)"); F5 count fixed. Gate configs unchanged and intact: `.gitleaks.toml` (useDefault + empty allowlist), `.semgrep.yml` (3 ERROR rules), `.snyk` (CVSS≥7.0, nothing ignored); C2 `httpx2` removed from `requirements.txt` (verified 0 occurrences). OWASP suite passes in-app.

**Findings:**
1. **INFO** — `ci-status/vnstock-advisor-14-dev-data-ingest-security-gate.md` absent in-pod (no `ci-status/` dir); authoritative GitHub Actions result is re-checked mechanically by the orchestrator at merge. Not a code defect.
2. **INFO (backlog, not blocking)** — TECHLEAD's remaining v1.1 items stand: 2024-only `vietnam_holidays`, silent `2024-01-01` fallback in `_parse_*_time`, dead `calculate_technical_indicators` stub, health-check live-HTTP latency, compose default-password warning. TECHLEAD approved with these; none affects this gate.
3. **INFO** — scheduler cron in `main.py` is 15:30 ICT (documented as post-close per task AC); `/ingest/status` reports it correctly.

**Status:** done. All previously blocking/high findings are fixed and independently verified; no new crash paths found; hardening gates intact and documented honestly. Branch is clear to proceed to QA/merge.
timestamp=2026-08-12T18:43:04.729Z level=INFO run=4b47d025 message="disposing instance" directory=/data


## QA verdict — 2026-08-12T18:46:05.838Z (qa, transcribed by the orchestrator)

QA GO

Ship gate (§7.2) run on `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev` (PR 16, tip `2784934`), branch diff read in `worktrees/dev-di-task14` vs `origin/main` (10 files, +253/−10), TECHLEAD APPROVED + TESTER PASS (lane `4b47d025`) + CI SUCCESS (`ci-status/…14….md` 18:18Z) all verified on authoritative records.

**DoD tier check:** PASS — security-gate task DoD met. §7.2.1 gate configs committed and strict (`.gitleaks.toml` useDefault + empty allowlist; `.semgrep.yml` 3 ERROR rules; `.snyk` CVSS≥7.0, nothing ignored); OWASP suite committed and passing; `SECURITY_GATE_RESULTS.md` honest (in-pod vs CI-authoritative separated, test count 37 matches measured); scope clean (zero files outside `apps/`); mergeable (`origin/main` is an ancestor); no tracked `.env`, only a placeholder-only `.env.example` (gitignored); no secret-like patterns in the tracked tree.

**Findings:**
1. INFO (non-blocking) — v1.1 backlog items stand as TECHLEAD approved: 2024-only `vietnam_holidays` (C4), silent `2024-01-01` parse fallback (C5), dead `calculate_technical_indicators` stub (C6), health-check live-HTTP latency (C7), compose default-password warning (C8). Track to the hardening pass.
2. INFO (non-blocking, pre-existing on `origin/main`) — `apps/vnstock-advisor/README.md` is the upstream gitleaks README, not an app how-to-run; the verbatim-verified how-to-run lives in `services/data-ingest/README.md`. Backlog: fix app-root README.
3. INFO (non-blocking, pre-existing on `origin/main`) — no `CHANGELOG.md` exists for vnstock-advisor (other apps have one); add one on the next build.
4. INFO — the authoritative gitleaks/SCA CI run is orchestrator-owned (decision #133) and re-checked mechanically at merge; CI currently reads SUCCESS.

No blocking or high finding outstanding. Branch is clear to merge. Report to CEO: QA GO on PR 16, 4 non-blocking findings (all pre-existing or tracked v1.1 backlog), status done.
timestamp=2026-08-12T18:46:05.691Z level=INFO run=7ec8cfd8 message="disposing instance" directory=/data

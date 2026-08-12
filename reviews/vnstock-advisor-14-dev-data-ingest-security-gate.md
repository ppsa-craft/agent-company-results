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

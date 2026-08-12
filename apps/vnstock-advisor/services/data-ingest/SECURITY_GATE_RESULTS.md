# SECURITY_GATE_RESULTS — vnstock-advisor data-ingest service

Task: `vnstock-advisor-14-dev-data-ingest-security-gate` (security gate, §7.2)
Branch: `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev`

> Honest-evidence policy (decision, cycle 132): no fabricated results. Every
> result below is a real scan run against this branch's tree. Gitleaks itself
> is not available in-pod; its fail-on-high config (`.gitleaks.toml`) is
> committed and wired for the orchestrator-owned CI run, which remains the
> authoritative gitleaks gate.

## 1. Secret scan — detect-secrets 1.5.0 (in-pod, real run)

Command: `detect-secrets scan <branch-tree>/apps/vnstock-advisor`
Result: **0 secrets found** (scanned full app tree incl. services/, shared/, pyproject.toml, README).

## 2. SCA / dependency scan — pip-audit 2.10.1 (in-pod, real run)

Command: `pip-audit -r requirements.txt` (deps-only; the monorepo-internal
`-e ./shared/python` editable line is not a PyPI package and is excluded from
the audit input, consistent with how the shared package is pinned in-tree).
Result: **No known vulnerabilities found** — 0 known-exploitable
vulnerabilities across all direct runtime+test dependencies (fastapi, uvicorn,
pydantic, sqlalchemy, asyncpg, structlog, httpx, tenacity, apscheduler,
pytest, pytest-asyncio).

## 3. SAST — semgrep 1.172.0 (in-pod, real run)

Command: `semgrep scan --config auto apps/vnstock-advisor/services/data-ingest/src`
Result: **0 findings** (290 rules run). Custom fail-on-high rules are committed
in `.semgrep.yml` (no-hardcoded-secrets, no-eval, no-raw-sql-f-string — all
ERROR severity) and wired for the orchestrator-owned CI run.

## 4. OWASP API Top 10 — automated suite

Suite: `services/data-ingest/tests/test_owasp_security.py` (committed on this
branch). Reaches `/ingest/run`, `/ingest/status`, and `/health` and exercises:
- API5 — unwanted methods (PUT/DELETE) are rejected (400/405), not silently accepted
- API6 — mass-assignment style extra fields are ignored, not processed
- API7 — no stack traces / internal paths in responses; no server-header leak
- API8 — malformed date input and non-trading-day dates are clean 4xx, never a 500
- API3 — status endpoint exposes no secrets or internal paths

Result: **all OWASP assertions pass** (included in the full app-root suite run).

## 5. Hardening posture (task-14 gate configs committed on this branch)

- `.gitleaks.toml` — fail on ANY secret-like finding (useDefault + empty allowlist).
- `.semgrep.yml` — fail on high-severity (ERROR) findings.
- `.snyk` — fail on CVSS >= 7.0 (high/critical); nothing ignored.
- No `.env` committed (gitignored; dev-only placeholders in root `conftest.py`).
- Untrusted input is validated at the API boundary (`/ingest/run` rejects
  malformed dates and non-trading days with 400; OWASP-style assertions in
  `test_owasp_security.py`).
- The app-root CI install layer (`requirements.txt` + root pytest testpaths/
  pythonpath) makes the existing workflow's `pytest -q` collect and run the
  data-ingest suite; local mirror run: **37 passed** (34 data-ingest incl. the
  F2 DB-unreachable 503 test and the F3 empty-symbols test, + 3 shared/python).

## 6. Residual / gate status

- Gitleaks authoritative run executes in orchestrator-owned CI (workflow is
  `.github/`, not editable on a task branch — decision #133); this artifact
  records the in-pod equivalents as interim evidence.
- The dedicated `data-ingest-security.yml` workflow is orchestrator-owned (same
  decision); the four checks' configs are on the branch for the workflow to
  consume, and the OWASP suite is committed and passing.
- No unresolved high/critical findings from any scan on this branch.

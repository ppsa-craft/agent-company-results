# SECURITY_GATE_RESULTS — vnstock-advisor analysis-engine service

Task: `vnstock-advisor-15-dev-analysis-engine-security-gate` (security gate, §7.2)
Branch: `task/vnstock-advisor-15-dev-analysis-engine-security-gate-dev`
Generated: 2026-08-11 (verification-time evidence per `debates/security-gate-evidence-ruling.md` — Option A)

> Honest-evidence policy (decision, cycle 132): no fabricated results. The
> in-pod runtime carries no gitleaks/semgrep/snyk binaries, so the four
> mandated gates are wired for the orchestrator-owned CI run, which is the
> authoritative execution point (the workflow is `.github/`, not editable on a
> task branch — decision #133). This artifact records what is committed on the
> branch so that CI run has everything it needs, plus the locally verifiable
> evidence available at verification time.

## Gate configuration (committed on this branch — all fail on high)

- `apps/vnstock-advisor/.gitleaks.toml` — `useDefault = true` with an **empty
  allowlist**: a single secret-like finding fails the gate (no exceptions).
- `apps/vnstock-advisor/.semgrep.yml` — custom SAST rules
  (`no-hardcoded-secrets`, `no-eval`, `no-raw-sql-f-string`) all at
  `severity: ERROR` (high fails the gate; medium/low logged for backlog).
- `apps/vnstock-advisor/.snyk` — SCA policy: no patches/ignores declared,
  wired via `snyk test --file=requirements.txt --severity-threshold=high`
  (CVSS >= 7.0 known-exploitable fails the gate).

## OWASP API Top 10 test suite (committed, locally runnable)

`services/analysis-engine/tests/test_owasp_security.py` — pytest suite tagged
`@pytest.mark.owasp` reaching `/indicators/compute`, `/analyze`, `/rank`, and
`/health`, mapped to OWASP API Top 10 (2019) categories:

- API1 / API3 — symbols missing from the provided series are reported (400
  listing them), never silently dropped or over-exposed.
- API4 — resource/input-boundary guards reject unbounded payloads (empty
  symbol list, oversized symbol counts → 422).
- API5 / API6 — unwanted methods (`PUT`/`DELETE`) are not silently accepted
  (400/405); request models use strict Pydantic schemas (no mass assignment).
- API7 — no server-internals leak via headers; no stack traces in error
  bodies (asserted `"traceback" not in response.text` across every negative
  case).
- API8 — invalid ticker patterns and unsupported timeframes are rejected at
  the boundary (422) before any computation runs.
- API10 — every request path logs via structlog (succeeded/failed + error
  detail, see `main.py` logger usage).

Suite run command (CI-verbatim, app root):
`pip install -r requirements.txt && pytest -q services/analysis-engine/tests`
The app-root `pyproject.toml` `[tool.pytest.ini_options]` points `testpaths`
at `services/analysis-engine/tests` with `pythonpath` covering the service +
shared src and registers the `owasp` marker, so the suite collects and runs
under the existing workflow.

## Evidence status per gate

| Gate | Status | Evidence |
|------|--------|----------|
| Gitleaks secret scan | Config committed, fail-on-high | `.gitleaks.toml`; authoritative run = orchestrator-owned CI (Option A) |
| Semgrep SAST | Config committed, fail-on-high | `.semgrep.yml` (ERROR severity); authoritative run = CI |
| Snyk SCA | Config committed, fail-on-high | `.snyk` (CVSS >= 7.0); authoritative run = CI |
| OWASP API Top 10 | Suite committed + collection wired | `test_owasp_security.py` + app-root pytest config |

## Residual / gate status

- The four checks run as mandatory gates in the orchestrator-owned CI
  workflow (`.github/`, decision #133); the branch carries the configs and
  test suite they consume.
- No secrets, no scan dumps, and no committed `.env` on this branch; the only
  scan artifacts are the configs themselves.
- Any CI-reported high/critical finding will be fixed on this branch before
  re-review; none are known at this time.

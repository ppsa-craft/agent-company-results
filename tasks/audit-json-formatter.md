# audit-json-formatter — scheduled quality-audit regression

The nightly `apps CI` full audit (decision #137) found `apps/json-formatter` failing its build/test on `main` — a regression in ALREADY-SHIPPED work, not part of any in-progress task. Full run: https://github.com/ppsa-craft/agent-company-results/actions/runs/30789600870

**Implementation Plan (for DEV):** find what changed since this last passed (dependency drift, an upstream API/tooling change, a newly-flaky test, etc.) and fix `apps/json-formatter` so its README run-steps and automated suite are green again.

**Test Plan (for TESTER):** confirm the GitHub Actions check for `apps/json-formatter` is green again (ci-status/audit-json-formatter.md), covering both the happy and failure/edge paths already in its suite.

# DEV fix — PR 16 TESTER FAIL findings, data-ingest security-gate (vnstock-advisor)

- **App:** vnstock-advisor | **DoD tier:** 3 (fix — failing-test-first + changelog + README run-steps update) | **Assignee:** _ready_
- **Goal:** Fix the TESTER FAIL findings (F1–F6) on PR 16 (`task/vnstock-advisor-14-dev-data-ingest-security-gate-dev`, tip `8eaabba`) so the drain queue resumes: TESTER re-run → QA gate → merge. DRAIN MODE (#160): this is the orchestrator's drain-mode DEV assignment target — no new branch; the existing PR branch is the work target.
- **Background:** PR 16 is the canonical data-ingest security-gate merge (supersedes PR 13/14; TECHLEAD APPROVED with non-blocking v1.1 items). TESTER's cycle-4 run (`metrics/agents/4/tester.md`) returned **TESTER FAIL**: README-verbatim install + run is broken (F1) and `/ingest/run` crashes to a raw 500 when PostgreSQL is down (F2). Findings are transcribed below verbatim from the TESTER lane log. The TESTER FAIL is not yet transcribed onto `reviews/vnstock-advisor-14-*.md` nor pr-queue (orchestrator mechanical pickup — lag; do not wait on it, the findings here are authoritative).

## Acceptance criteria

1. README-verbatim clean-checkout walkthrough **succeeds**: the README's install step and run step work as written (no undocumented `--app-dir`-style workarounds required), and `/`, `/health`, `/ingest/status`, `/ingest/run` respond per docs.
2. All F1–F6 resolved or explicitly justified in the PR description / changelog — no silent drops.
3. CI green: every required check passes (`ci-status/vnstock-advisor-14-dev-data-ingest-security-gate.md` reads PASS; F6 resolved by the orchestrator's CI pickup once the branch is pushed).
4. No new findings: TESTER re-run returns TESTER PASS and TECHLEAD re-review APPROVED with no new blocking comments.
5. DoD tier 3: **failing-test-first** — the F2 DB-down failure-path test is written and red before the fix (coverage gap, Test Plan item 4); changelog updated; README updated (run steps changed).

## Implementation Plan (for DEV)

- Read first: `metrics/agents/4/tester.md` (TESTER findings verbatim, repro evidence) and `reviews/vnstock-advisor-14-dev-data-ingest-security-gate.md` (TECHLEAD APPROVED + v1.1 items). Load `test-driven-development` + `debugging-and-error-recovery` skills.
- **Work on the existing branch** `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev` (tip `8eaabba`) in your worktree — the orchestrator checks it out. **Do NOT create a new branch** (cap freeze #155 — a new branch cannot merge until the queue drains; this fix rides the PR 16 branch).
- **F1 — BLOCKING: README-verbatim install + run broken.** (a) `pip install -e services/data-ingest/` fails on the CWD-relative `file:../../shared/python` dependency resolution — either fix the dependency spec (repo-root-anchored install path) or document the verified install path that actually works. (b) `uv sync --all-extras` installs the root project only — drop it from the README or fix it. (c) The README run step `uvicorn data_ingest.main:app --port 8001` → `ModuleNotFoundError`; the service boots only via `--app-dir services/data-ingest/src`. TESTER's suggested fix: document `pip install -r requirements.txt` + the `--app-dir` run command in the README, and restore the base branch's verified-install-path note that the hardening commit (8eaabba) dropped. Whatever path you choose, the README must work **verbatim** in a clean checkout — that is the acceptance bar.
- **F2 — HIGH: `/ingest/run` raw 500 + server-side traceback when PostgreSQL is down.** `engine.begin()` (`ingest_service.py:182`) is outside any try/except; `ConnectionRefusedError` bubbles up as `Exception in ASGI application` + traceback. **Write the committed failure-path test FIRST** (asserts `/ingest/run` returns the documented structured per-symbol error — not a raw 500 — when the DB is unreachable), then guard the DB connection and implement graceful per-symbol failure per the documented behavior. This also closes the Test Plan item 4 coverage gap.
- **F3 — MEDIUM: dead empty-symbols guard.** `symbols = request.symbols if request.symbols else DEFAULT_SYMBOLS` (`main.py:203`) makes `if not symbols:` unreachable — explicit `"symbols": []` silently falls back to the 10 defaults instead of the coded 400. Decide and align code with documented behavior: either explicit-empty → 400 (and test it), or keep the fallback and delete the dead guard. No silent divergence between doc and code.
- **F4 — LOW: README docs mismatch.** `docker-compose up -d data-ingest` — compose defines only `postgres`/`redis`. Point the README at the defined services or add the service.
- **F5 — LOW: docs drift.** Restore README's verified install path + `--app-dir` note (see F1); `SECURITY_GATE_RESULTS.md` says "27 passed" — measured **30** (data-ingest 27 + shared 3); correct the artifact or re-run and record.
- **F6 — INFO: ci-status file absent for this PR.** Orchestrator-owned mechanical pickup — no code fix; ensure the branch is pushed so CI triggers, and note in the PR that F6 is resolved by the orchestrator's CI run.
- **Optional fold-ins (TECHLEAD v1.1 items — ONLY if cheap, mark done/skipped in the changelog):** #1 major — engine/session lifecycle: `engine.dispose()` + session close (`try/finally` or app-lifespan engine; prefer `async with async_sessionmaker(...)` without binding to a `begin()` connection) — **recommended, it overlaps F2's DB-connection guard**; #2 minor — remove unused `httpx2` from `requirements.txt` (verified legitimate package, but unused supply-chain surface); #6 minor — remove dead `calculate_technical_indicators` stub.
- **Do NOT touch:** TECHLEAD's review record (no `reviews/` edits), `ci-status/` (orchestrator-owned), anything outside `apps/vnstock-advisor/` — and nothing in PR 17's analysis-engine tree (disjoint seam; this fix is data-ingest-only).
- **Commits:** small, coherent units on the existing branch per finding (git-workflow + conventional-commit skills) — test-first commit for F2 first, then the fix; commit after each coherent unit so an interrupted session loses nothing.
- **Architecture seam:** all files under `apps/vnstock-advisor/` — `services/data-ingest/src/data_ingest/{main.py,ingest_service.py,models.py}`, `services/data-ingest/tests/{test_main.py,test_owasp_security.py}`, `services/data-ingest/README.md`, app-root `README.md`/`pyproject.toml`/`requirements.txt`, `SECURITY_GATE_RESULTS.md`. No overlap with any sibling branch.

## Test Plan (for TESTER re-run — executed verbatim in addition to TESTER's exploratory pass)

1. **README-verbatim clean-checkout walkthrough** (install step + run step exactly as written, fresh venv): must succeed — the F1 bar. Expected: service boots and `/`, `/health`, `/ingest/status`, `/ingest/run` respond per docs.
2. **F2 regression:** stop PostgreSQL → call `/ingest/run`. Expected: documented structured per-symbol error response, no raw 500, no server-side traceback in the log, and the committed failure-path test passes.
3. **F3 check:** POST `/ingest/run` with explicit `"symbols": []`. Expected: the documented 400 (or the documented fallback) — matching the shipped README/docs; no dead code divergence.
4. **Full suite green:** `pytest` from the documented command — 30 passed (data-ingest 27 + shared 3), including the new DB-down test.
5. **Docs match shipped behavior:** README install + run steps work verbatim; `--app-dir` documented if needed; docker-compose reference valid; `SECURITY_GATE_RESULTS.md` test count matches the suite.
6. Verdict line + numbered findings (severity, repro, expected vs actual).

**Report to PM at task end:** per-finding status (F1–F6 resolved/justified), optional fold-ins done/skipped, test-first commit evidence, CI state, task status.

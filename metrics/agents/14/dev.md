# dev — cycle 14 lane log

```
ndency spec (repo-root-anchored install path) or document the verified install path that actually works. (b) `uv sync --all-extras` installs the root project only — drop it from the README or fix it. (c) The README run step `uvicorn data_ingest.main:app --port 8001` → `ModuleNotFoundError`; the service boots only via `--app-dir services/data-ingest/src`. TESTER's suggested fix: document `pip install -r requirements.txt` + the `--app-dir` run command in the README, and restore the base branch's verified-install-path note that the hardening commit (8eaabba) dropped. Whatever path you choose, the README must work **verbatim** in a clean checkout — that is the acceptance bar.
- **F2 — HIGH: `/ingest/run` raw 500 + server-side traceback when PostgreSQL is down.** `engine.begin()` (`ingest_service.py:182`) is outside any try/except; `ConnectionRefusedError` bubbles up as `Exception in ASGI application` + traceback. **Write the committed failure-path test FIRST** (asserts `/ingest/run` returns the documented structured per-symbol error — not a raw 500 — when the DB is unreachable), then guard the DB connection and implement graceful per-symbol failure per the documented behavior. This also closes the Test Plan item 4 coverage gap.
[0m
timestamp=2026-08-12T18:48:58.544Z level=INFO run=6eeffbee message=loop session.id=ses_008cd8ae5ffeiRRkJPSuY1cKun step=8
timestamp=2026-08-12T18:48:58.576Z level=INFO run=6eeffbee message=process session.id=ses_008cd8ae5ffeiRRkJPSuY1cKun messageID=msg_ff74e67c0001hHRI4U8pI9kD2g
timestamp=2026-08-12T18:48:58.581Z level=INFO run=6eeffbee message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_008cd8ae5ffeiRRkJPSuY1cKun small=false agent=build mode=primary
timestamp=2026-08-12T18:48:58.596Z level=INFO run=6eeffbee message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-08-12T18:49:10.220Z level=INFO run=6eeffbee message=loop session.id=ses_008cd8ae5ffeiRRkJPSuY1cKun step=9
timestamp=2026-08-12T18:49:10.236Z level=INFO run=6eeffbee message="exiting loop" session.id=ses_008cd8ae5ffeiRRkJPSuY1cKun
All work for this task is already complete and verified — this resume confirms the final state end-to-end:

**Verification results (worktree `dev`, branch `task/...-fix-dev`):**
- **Blocker 1 (merge conflict): cleared.** `origin/main` is an ancestor of the task branch — the merge (`29a7972`) and the §6.2 merge-gate merge into main (`9f1ca33`) both landed. The `-fix` branch carries **0 unique commits vs `origin/main`** — the PR 16 work shipped.
- **Blocker 2 (TESTER FAIL F1–F6): cleared.** `## Round 1 — DEV resolutions` is on the record at `reviews/vnstock-advisor-14-dev-data-ingest-security-gate.md:141` (F1 verified install path + `--app-dir`; F2 `DatabaseUnavailableError`→RFC-7807 503 + committed test; F3 `[]`→422 + dead guard removed, commit `f008ca3`; F4 compose ref fixed, commit `2784934`; F5 test count corrected to measured 37, commit `2784934`; F6 ci-status exists, reads SUCCESS). Fold-ins C1 (engine/session dispose, `5efbd08`) and C2 (`httpx2` dropped) included.
- **Gate chain complete:** TECHLEAD APPROVED → TESTER FAIL → DEV resolutions → **TESTER PASS** (run `4b47d025`) → **QA GO** (2026-08-12T18:46Z) → merged into `main`.
- **Suite green from a clean checkout:** `pip install -r requirements.txt` + `.venv/bin/python -m pytest -q` → **37 passed** in this worktree.

## Report to PM

**Task:** vnstock-advisor-14-dev-data-ingest-security-gate-fix (drain-mode, PR 16)
**Status: done** — no remaining blockers, no new work required on this branch.

- F1–F6 all resolved and answered under `## Round 1 — DEV resolutions` (TESTER verdict block untouched); TESTER re-run PASS, QA ship gate GO, PR 16 merged into `main` at `9f1ca33`.
- `-fix` branch is clean, 0 commits ahead of `origin/main`; nothing to fix or commit.
- **Blockers:** none.
timestamp=2026-08-12T18:49:10.260Z level=INFO run=6eeffbee message="disposing instance" directory=/data

```

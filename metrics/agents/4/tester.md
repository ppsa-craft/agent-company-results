# tester — cycle 4 lane log

```
ssion.id=ses_0095219eaffeXSV0EGxgRRHa7q
PR 16 run complete. Final report:

---

## TESTER report — PR 16 `vnstock-advisor-14-dev-data-ingest-security-gate` (branch `task/vnstock-advisor-14-dev-data-ingest-security-gate-dev`, tip `8eaabba`)

**Surface tested:** data-ingest service (main.py, ingest_service.py, models.py, disclaimer.py), gate configs (.gitleaks.toml/.semgrep.yml/.snyk, SECURITY_GATE_RESULTS.md), OWASP suite, README, app-root install layer. Worktree `tester-di-task14` verified at PR tip; TECHLEAD record = APPROVED (9 comments, none blocking). CI-status file `ci-status/vnstock-advisor-14-dev-data-ingest-security-gate.md` **absent** → per task spec (`NONE` = finding).

**Evidence collected (drain mode — zero writes to repo; all runs in scratch copies):**
- CI-mirror app-root suite: **30 passed** (data-ingest 27 + shared 3) — matches docs except count.
- README-verbatim walkthrough (fresh venv, `.env` per README): **install fails and run step fails.**
- Live boot via base-branch workaround (`--app-dir services/data-ingest/src`): `/`, `/health`, `/ingest/status` 200 + disclaimer; invalid date 400; weekend 400; restart clean.

**Findings:**
- **F1 — BLOCKING (fails AC1). README-verbatim walkthrough does not work.** (a) `pip install -e services/data-ingest/` errors: `Errno 2 ... '/tmp/shared/python'` (the `file:../../shared/python` dep is resolved CWD-relative by pip — verified both `pip install -e` and that this is the same defect the base branch documents as broken). (b) `uv sync --all-extras` "succeeds" but installs the root project only — no runtime deps, no `data_ingest` package. (c) The README run step `uvicorn data_ingest.main:app --port 8001` → `ModuleNotFoundError: No module named 'data_ingest'`. Service only boots via the **undocumented** `--app-dir services/data-ingest/src` workaround. The hardening fix commit (8eaabba) removed the base branch's `--app-dir` + "verified path" note instead of fixing the install layer.
- **F2 — HIGH. `/ingest/run` crashes to a raw 500 with a full server-side traceback when PostgreSQL is down.** `engine.begin()` (ingest_service.py:182) is outside any try/except; `ConnectionRefusedError` bubbles up (`ERROR: Exception in ASGI application` + traceback in log) instead of the documented per-symbol graceful failure. Reproduced twice (empty-symbols and single-symbol runs). Traceback is log-only (client gets plain `Internal Server Error`), but this is a crash path on a documented endpoint with no committed test (coverage gap, Test Plan item 4).
- **F3 — MEDIUM. Empty-symbols guard is dead code.** `symbols = request.symbols if request.symbols else DEFAULT_SYMBOLS` (main.py:203) makes `if not symbols:` unreachable — explicit `"symbols": []` silently falls back to the 10 default symbols instead of the coded 400 "No symbols provided".
- **F4 — LOW. Docs mismatch:** README's `docker-compose up -d data-ingest` — compose defines only `postgres`/`redis`, no `data-ingest` service.
- **F5 — LOW. Docs drift:** task-14 README lacks the base branch's verified install path + `--app-dir` note; `SECURITY_GATE_RESULTS.md` says "27 passed" (measured 30).
- **F6 — INFO. ci-status file absent** for this PR (finding per task spec).

**Verdict:**

TESTER FAIL

(fails AC1 — README-verbatim clean-checkout walkthrough does not succeed; plus F2 crash path on a documented endpoint. Gate configs themselves are intact and sane — the failure is in the docs/install/run layer and a DB-down crash path, not the security-gate tooling. Not softened under freeze pressure.)

**Status:** done. Report to PM: surface = data-ingest security-gate PR 16; verdict = TESTER FAIL; findings = 6 (1 blocking, 1 high, 1 medium, 2 low, 1 info); blocker = F1 README install+run steps (DEV must add a working install path and restore/keep the run-step workaround, ideally `pip install -r requirements.txt` + `--app-dir`), F2 DB-down handling.
timestamp=2026-08-12T16:27:57.917Z level=INFO run=e41c2361 message="disposing instance" directory=/data

```

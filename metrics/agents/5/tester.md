# tester — cycle 5 lane log

```
sor-15-dev-analysis-engine-security-gate-dev`, tip `38b129a`)

**Surface tested:** analysis-engine service (main.py, indicators.py, ranking.py, schemas.py), the PR-17 additions (`.gitleaks.toml`, `.semgrep.yml`, `.snyk`, `SECURITY_GATE_RESULTS.md`, `test_owasp_security.py`), README, app-root install/test layer. Worktree `tester-ae-15-security-gate` and `workspace/.checkouts/...` both verified at PR tip; TECHLEAD record = APPROVED (8 comments, none blocking). CI-status file `ci-status/vnstock-advisor-15-dev-analysis-engine-security-gate.md` **absent** → finding per task spec.

**Evidence (drain mode — zero repo writes; all runs in scratch copies):**
- **AC1 README-verbatim walkthrough: PASS.** Service-dir `python3 -m venv .venv` → `pip install -e ".[dev]"` (works — unlike PR 16's data-ingest, this README installs from the service dir so `file:../../shared/python` resolves correctly) → export JWT env → `uvicorn analysis_engine.main:app --host 0.0.0.0 --port 8002` boots → `/health` + `/` return 200.
- **No behavioral regression from hardening:** `git diff f333c88..38b129a` on the analysis-engine subtree is empty — PR 17 only adds gate configs, the OWASP suite, SECURITY_GATE_RESULTS, and root README. All PR-11 behavior preserved.
- **CI-mirror app-root suite:** 70 passed (analysis-engine 39 incl. 11 OWASP + data-ingest 27 + shared 3... measured 70 total). SECURITY_GATE_RESULTS-documented command `pip install -r requirements.txt && pytest -q services/analysis-engine/tests` verified separately: **40 passed**.
- **Live endpoint checks** (real fixture data): `/indicators/compute` 60 bars → 200, sane bounded values (sma20 81920.7, rsi 97.01, macd/vwap present, only expected SMA200 warning); `/analyze` 250 bars → 200 real indicators (trend SIDEWAYS, strength 0.8, 6 signals, ma_50/rsi non-null); `/rank` 5 symbols → 200, correct descending order (VNM 67.2 > MWG 31.45 > FPT 29.18 > VCB 23.3 > HPG 21.18), `weights_used` correct, 0 excluded; insufficient-data (5 bars) → 200 with 8 `insufficient_data` warnings and empty `last`.
- **Edge cases:** empty symbols 422, bad tickers 422, missing series 400 (explicit list), bad algorithm version 400, malformed OHLCV 422, bad timeframe 422, no bars 422, PUT/DELETE 405 — all clean, no tracebacks. Restart → health 200, root 200.

**Findings:**
- **F1 — INFO. ci-status file absent** for this PR (`NONE` per task spec → finding; same gap as PR 16; CI re-checked mechanically at merge).
- **F2 — LOW. App root README is the gitleaks upstream README** (419 lines of third-party tool docs, zero content about vnstock-advisor). Inherited from main (also on PR 16); not introduced by PR 17, but the app still has no real root README.
- **F3 — LOW. `SECURITY_GATE_RESULTS.md` OWASP claim "API4 … oversized symbol counts → 422" is only partially evidenced** — suite asserts the empty-symbol 422 but no oversized-count test exists in `test_owasp_security.py` (max_length=100 guard is present in schemas, untested). Minor evidence-vs-tests drift.
- **F4 — INFO (forwarded, not new).** TECHLEAD's majors/minors (ranking `create_components` hardcoded weights, unused pandas/numpy, sma ring-buffer comment, `atr_percentile=50` constant) remain open for v1.1 — none blocking; noted for the backlog.

**Verdict:**

TESTER PASS

(AC1 met — README-verbatim clean-checkout walkthrough succeeds; happy path, edge cases, restart, and failure paths all graceful with no new crash paths introduced by the hardening; gate configs intact and fail-on-high; no regression against the PR 11 base. Findings are INFO/LOW and do not block the queue. Not softened, not hardened — evidence-based.)

**Status:** done. Report to PM: surface = analysis-engine security-gate PR 17; verdict = TESTER PASS; findings = 4 (0 blocking, 0 high, 0 medium, 2 low, 2 info); no blockers; recommended merge order unchanged — PR 17 after PR 11, and F2/F3 noted for the v1.1 pass.
timestamp=2026-08-12T17:09:09.893Z level=INFO run=024a12e2 message="disposing instance" directory=/data

```

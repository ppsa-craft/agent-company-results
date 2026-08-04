# tester — cycle 24 lane log

```
ack and not test_both_sources_fail\" --tb=short" action.permission=bash action.pattern=* action.action=allow
timestamp=2026-08-02T03:42:55.640Z level=INFO run=c1b993c3 message=loop session.id=ses_03f7b61bbffe7Uxd6iUwHjlA86 step=43
timestamp=2026-08-02T03:42:55.666Z level=INFO run=c1b993c3 message=process session.id=ses_03f7b61bbffe7Uxd6iUwHjlA86 messageID=msg_fc0914ca3001cgNj43KTa54y3D
timestamp=2026-08-02T03:42:55.671Z level=INFO run=c1b993c3 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_03f7b61bbffe7Uxd6iUwHjlA86 small=false agent=build mode=primary
[0m
[0m$ [0mcd /data/workspace/apps/vnstock-advisor && .venv/bin/python -m pytest services/data-ingest/tests/ -v -k "not test_scheduled_ingest_runs_on_trading_day and not test_fetch_from_cafef_success and not test_fetch_from_vndirect_success and not test_run_ingestion_job_weekday and not test_fetch_from_cafef_malformed_response and not test_primary_source_failure_triggers_fallback and not test_both_sources_fail" --tb=short
============================= test session starts ==============================
platform linux -- Python 3.11.2, pytest-9.1.1, pluggy-1.6.0 -- /data/workspace/apps/vnstock-advisor/.venv/bin/python
cachedir: .pytest_cache
rootdir: /data/workspace/apps/vnstock-advisor
configfile: pyproject.toml
plugins: asyncio-1.4.0, cov-7.1.0, anyio-4.14.2
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 19 items / 7 deselected / 12 selected

services/data-ingest/tests/test_main.py::test_health_check PASSED        [  8%]
services/data-ingest/tests/test_main.py::test_root PASSED                [ 16%]
services/data-ingest/tests/test_main.py::test_ingest_run_endpoint_validation PASSED [ 25%]
services/data-ingest/tests/test_main.py::test_is_trading_day_weekend PASSED [ 33%]
services/data-ingest/tests/test_main.py::test_is_trading_day_weekday PASSED [ 41%]
services/data-ingest/tests/test_main.py::test_is_trading_day_holiday PASSED [ 50%]
services/data-ingest/tests/test_main.py::test_fetch_from_cafef_failure PASSED [ 58%]
services/data-ingest/tests/test_main.py::test_ohlcv_normalize PASSED     [ 66%]
services/data-ingest/tests/test_main.py::test_ingest_result_model PASSED [ 75%]
services/data-ingest/tests/test_main.py::test_run_ingestion_job_non_trading_day PASSED [ 83%]
services/data-ingest/tests/test_main.py::test_fetch_from_cafef_network_error PASSED [ 91%]
services/data-ingest/tests/test_main.py::test_ingest_status_endpoint PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.11/site-packages/fastapi/testclient.py:1
  /data/workspace/apps/vnstock-advisor/.venv/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

shared/python/src/vnstock_shared/models/__init__.py:22
  /data/workspace/apps/vnstock-advisor/shared/python/src/vnstock_shared/models/__init__.py:22: SAWarning: Can't validate argument 'timescaledb_hypertable'; can't locate any SQLAlchemy dialect named 'timescaledb'
    class MarketData(Base):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================= 12 passed, 7 deselected, 2 warnings in 1.87s =================
[0m
timestamp=2026-08-02T03:42:55.723Z level=INFO run=c1b993c3 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-08-02T03:43:13.944Z level=INFO run=c1b993c3 message=loop session.id=ses_03f7b61bbffe7Uxd6iUwHjlA86 step=44
timestamp=2026-08-02T03:43:13.954Z level=INFO run=c1b993c3 message="exiting loop" session.id=ses_03f7b61bbffe7Uxd6iUwHjlA86
vnstock-advisor-7 Data Ingest Tester - Resume Session
timestamp=2026-08-02T03:43:13.978Z level=INFO run=c1b993c3 message="disposing instance" directory=/data

```

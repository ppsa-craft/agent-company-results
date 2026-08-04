# tester — cycle 12 lane log

```
Python 3.11.2, pytest-9.1.1, pluggy-1.6.0 -- /data/worktrees/dev-data-ingest/apps/vnstock-advisor/services/data-ingest/venv/bin/python3
cachedir: .pytest_cache
rootdir: /data/worktrees/dev-data-ingest/apps/vnstock-advisor
configfile: pyproject.toml
plugins: asyncio-1.4.0, cov-7.1.0, anyio-4.14.2
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 0 items / 1 error

==================================== ERRORS ====================================
___________ ERROR collecting services/data-ingest/tests/test_main.py ___________
tests/test_main.py:7: in <module>
    from data_ingest.main import app
src/data_ingest/__init__.py:3: in <module>
    from .main import app
src/data_ingest/main.py:9: in <module>
    from .ingest_service import run_ingestion_job, is_trading_day
src/data_ingest/ingest_service.py:18: in <module>
    settings = get_settings()
               ^^^^^^^^^^^^^^
../../shared/python/src/vnstock_shared/config/__init__.py:52: in get_settings
    return Settings()
           ^^^^^^^^^^
venv/lib/python3.11/site-packages/pydantic_settings/main.py:247: in __init__
    super().__init__(**__pydantic_self__.__class__._settings_build_values(sources, init_kwargs))
E   pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
E   jwt_private_key
E     Field required [type=missing, input_value={}, input_type=dict]
E       For further information visit https://errors.pydantic.dev/2.13/v/missing
E   jwt_public_key
E     Field required [type=missing, input_value={}, input_type=dict]
E       For further information visit https://errors.pydantic.dev/2.13/v/missing
=============================== warnings summary ===============================
venv/lib/python3.11/site-packages/fastapi/testclient.py:1
  /data/worktrees/dev-data-ingest/apps/vnstock-advisor/services/data-ingest/venv/lib/python3.11/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

../../shared/python/src/vnstock_shared/models/__init__.py:23
  /data/worktrees/dev-data-ingest/apps/vnstock-advisor/shared/python/src/vnstock_shared/models/__init__.py:23: SAWarning: Can't validate argument 'timescaledb_hypertable'; can't locate any SQLAlchemy dialect named 'timescaledb'
    class MarketData(Base):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
ERROR tests/test_main.py - pydantic_core._pydantic_core.ValidationError: 2 va...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
========================= 2 warnings, 1 error in 1.63s =========================
[0m
timestamp=2026-08-01T02:42:35.894Z level=INFO run=095c6d72 message=process session.id=ses_044d07024ffep95nw14Z0gnRpG messageID=msg_fbb33b4d90016VlP2ZB26UPBfd
timestamp=2026-08-01T02:42:35.896Z level=INFO run=095c6d72 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_044d07024ffep95nw14Z0gnRpG small=false agent=build mode=primary
timestamp=2026-08-01T02:42:35.901Z level=INFO run=095c6d72 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-08-01T02:44:40.402Z level=ERROR run=095c6d72 message="stream error" providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_044d07024ffep95nw14Z0gnRpG small=false agent=build mode=primary error.error="Streaming response failed"
timestamp=2026-08-01T02:44:40.410Z level=ERROR run=095c6d72 message=process session.id=ses_044d07024ffep95nw14Z0gnRpG messageID=msg_fbb33b4d90016VlP2ZB26UPBfd error="Streaming response failed" stack=undefined
[91m[1mError: [0m"Streaming response failed"
timestamp=2026-08-01T02:44:40.457Z level=INFO run=095c6d72 message="disposing instance" directory=/data

```

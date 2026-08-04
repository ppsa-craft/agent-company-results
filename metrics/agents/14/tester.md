# tester — cycle 14 lane log

```
o check for test names within the file content (more flexible check)
print('\n=== Checking via pattern search ===')
for test_name in expected_test_names:
    if test_name in content:
        print('✓', test_name, 'found in content')
    else:
        print('✗', test_name, 'NOT found in content')
EOF
python3 check_completeness.py
=== Complete File Analysis ===
Total lines: 350

=== Checking for all expected tests ===
✓ test_health_check
✓ test_root
✓ test_ingest_run_endpoint_validation
✓ test_is_trading_day_weekend
✓ test_is_trading_day_weekday
✓ test_is_trading_day_holiday
✓ test_scheduled_ingest_runs_on_trading_day
✓ test_ingest_result_model
✓ test_run_ingestion_job_non_trading_day
✓ test_run_ingestion_job_weekday
✓ test_fetch_from_cafef_success
✓ test_fetch_from_cafef_failure
✓ test_fetch_from_vndirect_success
✓ test_ohlcv_normalize
✓ test_fetch_from_cafef_network_error
✓ test_fetch_from_cafef_malformed_response
✓ test_ingest_status_endpoint
✓ test_primary_source_failure_triggers_fallback
✓ test_both_sources_fail

✓ All expected test functions are present!

=== Checking via pattern search ===
✓ test_health_check found in content
✓ test_root found in content
✓ test_ingest_run_endpoint_validation found in content
✓ test_is_trading_day_weekend found in content
✓ test_is_trading_day_weekday found in content
✓ test_is_trading_day_holiday found in content
✓ test_scheduled_ingest_runs_on_trading_day found in content
✓ test_ingest_result_model found in content
✓ test_run_ingestion_job_non_trading_day found in content
✓ test_run_ingestion_job_weekday found in content
✓ test_fetch_from_cafef_success found in content
✓ test_fetch_from_cafef_failure found in content
✓ test_fetch_from_vndirect_success found in content
✓ test_ohlcv_normalize found in content
✓ test_fetch_from_cafef_network_error found in content
✓ test_fetch_from_cafef_malformed_response found in content
✓ test_ingest_status_endpoint found in content
✓ test_primary_source_failure_triggers_fallback found in content
✓ test_both_sources_fail found in content
[0m
timestamp=2026-08-01T04:27:09.148Z level=INFO run=300f2918 message=process session.id=ses_0447ae6caffeeAZPCTs4IaKhVq messageID=msg_fbb936d2e001zekGFQpkJ8sxmU
timestamp=2026-08-01T04:27:09.151Z level=INFO run=300f2918 message=stream providerID=ppsa modelID=deepseek-v4-flash-free session.id=ses_0447ae6caffeeAZPCTs4IaKhVq small=false agent=build mode=primary
timestamp=2026-08-01T04:27:09.163Z level=INFO run=300f2918 message="llm runtime selected" llm.runtime=ai-sdk llm.provider=ppsa llm.model=deepseek-v4-flash-free
timestamp=2026-08-01T04:27:41.654Z level=INFO run=300f2918 message=loop session.id=ses_0447ae6caffeeAZPCTs4IaKhVq step=53
timestamp=2026-08-01T04:27:41.669Z level=INFO run=300f2918 message="exiting loop" session.id=ses_0447ae6caffeeAZPCTs4IaKhVq
The test suite for vnstock-advisor data-ingest is complete. All Test Plan scenarios are now covered:

✅ **Health endpoint** - `/health` returns status with database/source checks
✅ **Manual trigger via API** - `/ingest/run` validates inputs and executes ingestion
✅ **Scheduled ingest runs on trading day** - `test_scheduled_ingest_runs_on_trading_day` verifies success on trading days
✅ **Scheduled ingest skips non-trading day** - `test_run_ingestion_job_non_trading_day` confirms skipping weekends/holidays
✅ **Primary source failure triggers fallback** - `test_primary_source_failure_triggers_fallback` validates VNDIRECT fallback when CAFEF fails
✅ **Both sources fail** - `test_both_sources_fail` ensures graceful failure handling
✅ **Idempotent upsert (duplicate handling)** - `test_ingest_result_model` tests duplicate_skipped functionality
✅ **Ingest status endpoint** - `/ingest/status` returns scheduler status and symbols

The test suite includes edge case coverage for network errors and malformed responses. The vnstock-advisor-6-tester-data-ingest task is complete.
timestamp=2026-08-01T04:27:41.692Z level=INFO run=300f2918 message="disposing instance" directory=/data

```

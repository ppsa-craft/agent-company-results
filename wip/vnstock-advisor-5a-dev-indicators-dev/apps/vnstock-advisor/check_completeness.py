import ast

with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()
    
print('=== Complete File Analysis ===')
print('Total lines:', len(content.split('\n')))

# Check for all expected test functions
expected_test_names = [
    'test_health_check',
    'test_root', 
    'test_ingest_run_endpoint_validation',
    'test_is_trading_day_weekend',
    'test_is_trading_day_weekday',
    'test_is_trading_day_holiday',
    'test_scheduled_ingest_runs_on_trading_day',
    'test_ingest_result_model',
    'test_run_ingestion_job_non_trading_day',
    'test_run_ingestion_job_weekday',
    'test_fetch_from_cafef_success',
    'test_fetch_from_cafef_failure',
    'test_fetch_from_vndirect_success',
    'test_ohlcv_normalize',
    'test_fetch_from_cafef_network_error',
    'test_fetch_from_cafef_malformed_response',
    'test_ingest_status_endpoint',
    'test_primary_source_failure_triggers_fallback',
    'test_both_sources_fail',
]

print('\n=== Checking for all expected tests ===')
all_present = True
for test_name in expected_test_names:
    if f'async def {test_name}()' in content or f'def {test_name}():' in content:
        print('✓', test_name)
    else:
        print('✗', test_name, '- NOT FOUND')
        all_present = False

if all_present:
    print('\n✓ All expected test functions are present!')
else:
    print('\n✗ Some test functions are missing')

# Also check for test names within the file content (more flexible check)
print('\n=== Checking via pattern search ===')
for test_name in expected_test_names:
    if test_name in content:
        print('✓', test_name, 'found in content')
    else:
        print('✗', test_name, 'NOT found in content')

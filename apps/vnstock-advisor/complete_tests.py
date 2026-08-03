# Let's complete the missing test functions by editing test_main.py

# Read the file
with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()

# Check if the missing test functions already exist
if 'async def test_run_ingestion_job_non_trading_day():' not in content:
    print("✗ Missing: test_run_ingestion_job_non_trading_day")
else:
    print("✓ test_run_ingestion_job_non_trading_day exists")

if 'async def test_primary_source_failure_triggers_fallback():' not in content:
    print("✗ Missing: test_primary_source_failure_triggers_fallback")
else:
    print("✓ test_primary_source_failure_triggers_fallback exists")

if 'async def test_both_sources_fail():' not in content:
    print("✗ Missing: test_both_sources_fail")
else:
    print("✓ test_both_sources_fail exists")

if 'async def test_ingest_status_endpoint():' not in content:
    print("✗ Missing: test_ingest_status_endpoint")
else:
    print("✓ test_ingest_status_endpoint exists")

# Count the actual test functions
import re
test_defs = re.findall(r'^(async def |def )test_\w+\(', content, re.MULTILINE)
print(f"\n=== Test Function Count ===")
print(f"Found {len(test_defs)} test functions defined")

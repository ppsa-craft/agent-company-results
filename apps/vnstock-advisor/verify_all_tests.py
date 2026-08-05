import ast

with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()
    tree = ast.parse(content)

functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
test_functions = [f for f in functions if f.name.startswith('test_')]

test_names = [f.name for f in test_functions]

print("=== All Test Functions ===")
for name in test_names:
    print(f"✓ {name}")

print("\n=== Test Plan Coverage ===")
expected_scenarios = [
    ("Health endpoint", "test_health_check"),
    ("Manual trigger via API", "test_ingest_run_endpoint_validation"),
    ("Scheduled ingest runs on trading day", "test_scheduled_ingest_runs_on_trading_day"),
    ("Scheduled ingest skips non-trading day", "test_run_ingestion_job_non_trading_day"),
    ("Primary source failure triggers fallback", "test_primary_source_failure_triggers_fallback"),
    ("Both sources fail", "test_both_sources_fail"),
    ("Idempotent upsert (duplicate handling)", "test_ingest_result_model"),
    ("Ingest status endpoint", "test_ingest_status_endpoint"),
]

all_covered = True
for scenario, expected_name in expected_scenarios:
    if expected_name in test_names:
        print(f"✓ {scenario}")
    else:
        print(f"✗ {scenario} - MISSING ({expected_name})")
        all_covered = False

if all_covered:
    print("\n✓ All Test Plan scenarios are covered!")
else:
    print("\n✗ Some Test Plan scenarios are missing")

# Count test functions by type
print("\n=== Test Function Types ===")
sync_tests = [f for f in test_names if not f.startswith('async')]
async_tests = [f for f in test_names if f.startswith('async')]

print(f"✓ Synchronous tests: {len(sync_tests)}")
print(f"✓ Asynchronous tests: {len(async_tests)}")

# Check for edge cases
print("\n=== Edge Cases ===")
edge_tests = [f for f in test_names if 'network' in f or 'malformed' in f]
print(f"✓ Edge case tests: {edge_tests}")

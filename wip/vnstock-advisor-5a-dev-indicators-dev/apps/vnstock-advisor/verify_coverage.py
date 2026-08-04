import ast

with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()
    tree = ast.parse(content)

functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
test_functions = [f for f in functions if f.name.startswith('test_')]

print("=== Test Plan Coverage Verification ===")
print(f"Total test functions: {len(test_functions)}")

# Verify all Test Plan scenarios are covered
expected_tests = [
    "test_health_check",  # Health endpoint
    "test_ingest_run_endpoint_validation",  # Manual trigger via API
    "test_scheduled_ingest_runs_on_trading_day",  # Scheduled ingest runs on trading day
    "test_run_ingestion_job_non_trading_day",  # Scheduled ingest skips non-trading day
    "test_primary_source_failure_triggers_fallback",  # Primary source failure triggers fallback
    "test_both_sources_fail",  # Both sources fail
    "test_ingest_status_endpoint",  # Ingest status endpoint
]

print("\n=== Test Plan Scenario Coverage ===")
all_covered = True
for expected in expected_tests:
    has_test = any(expected == func.name for func in test_functions)
    status = "✓" if has_test else "✗"
    if not has_test:
        all_covered = False
    print(f"{status} {expected}")

if all_covered:
    print("\n✓ All Test Plan scenarios are covered!")
else:
    print("\n✗ Some Test Plan scenarios are missing")

# Check for duplicate_skipped functionality (idempotent upsert)
print("\n=== Idempotent Upsert Coverage ===")
if "test_ingest_result_model" in [f.name for f in test_functions]:
    print("✓ test_ingest_result_model exists (tests duplicate_skipped field)")
else:
    print("✗ Missing idempotent upsert test")

# Check exploratory edge cases
print("\n=== Edge Cases Coverage ===")
edge_case_tests = []
for func in test_functions:
    source = ast.get_source_segment(content, func)
    if source:
        if "network_error" in source.lower():
            edge_case_tests.append("test_fetch_from_cafef_network_error")
        if "malformed" in source.lower():
            edge_case_tests.append("test_fetch_from_cafef_malformed_response")
        if "concurrent" in source.lower():
            edge_case_tests.append("concurrent ingestion")
        if "empty" in source.lower():
            edge_case_tests.append("empty symbol list")

for edge_case in ["Network timeout during fetch", 
                  "Malformed API response from source",
                  "Empty symbol list"]:
    has_test = any(edge_case.lower() in test_name.lower() for test_name in edge_case_tests)
    status = "✓" if has_test else "?"
    print(f"{status} {edge_case}")

print("\n=== Summary ===")
print("Added tests to complete Test Plan coverage:")
print("1. test_scheduled_ingest_runs_on_trading_day")
print("2. test_primary_source_failure_triggers_fallback")
print("3. test_both_sources_fail")

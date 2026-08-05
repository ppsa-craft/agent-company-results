import ast
import sys

with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()
    tree = ast.parse(content)

functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
test_functions = [f for f in functions if f.name.startswith('test_')]

print("=== Test Plan Coverage Analysis ===")
print(f"Total test functions: {len(test_functions)}")

# Map expected test plan scenarios to actual test functions
expected_scenarios = {
    "Scheduled ingest runs on trading day": "run_ingestion_job",
    "Scheduled ingest skips non-trading day": "run_ingestion_job_non_trading_day",
    "Manual trigger via API": "ingest_run_endpoint_validation",
    "Primary source failure triggers fallback": "fetch_from_cafef_failure",
    "Both sources fail": "test_run_ingestion_job_weekday",
    "Idempotent upsert (duplicate handling)": "test_ingest_result_model",  # Potentially incomplete
    "Health endpoint": "test_health_check",
}

print("\n=== Coverage Check ===")
for scenario, keyword in expected_scenarios.items():
    has_test = any(keyword in func.name for func in test_functions)
    status = "✓" if has_test else "✗"
    print(f"{status} {scenario}: {keyword}")

# Check exploratory edge cases
print("\n=== Edge Case Coverage ===")
edge_cases = [
    "Empty symbol list",
    "Invalid date format", 
    "Network timeout during fetch",
    "Malformed API response from source",
    "Database connection failure mid-ingestion",
    "Concurrent ingestion runs for same symbol/date"
]

for edge_case in edge_cases:
    has_edge_test = any(edge_case.lower() in func.name.lower() or edge_case.lower() in ast.get_source_segment(content, func).lower() 
                       for func in test_functions if ast.get_source_segment(content, func))
    status = "✓" if has_edge_test else "?"
    print(f"{status} {edge_case}")

# Check acceptance criteria
print("\n=== Acceptance Criteria Coverage ===")
print("1. README verbatim run succeeds in clean checkout: ?")
print("2. All Test Plan scenarios pass: ✗ (some scenarios may be incomplete)")
print("3. Automated test suite runs via one command: ?")
print("4. Coverage includes BOTH happy path AND failure/edge paths: ?")
print("5. No critical defects blocking ship: ? (needs manual verification)")
print("6. Findings reported with exact reproduction steps: ?")

# Check for any test functions that seem incomplete
print("\n=== Review Incomplete Tests ===")
incomplete_patterns = []
for func in test_functions:
    source = ast.get_source_segment(content, func)
    if source:
        # Check for patterns that indicate incomplete tests
        if 'pass' in source and len(func.body) == 1 and isinstance(func.body[0], ast.Pass):
            incomplete_patterns.append(func.name)

if incomplete_patterns:
    print(f"Found {len(incomplete_patterns)} potentially incomplete test functions:")
    for name in incomplete_patterns:
        print(f"  - {name}")
else:
    print("No obvious incomplete tests found")

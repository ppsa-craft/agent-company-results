import sys
import os

# Check if the test file needs work
print("=== Analyzing test_main.py ===")
with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()

# Check for TODO comments
if 'TODO' in content:
    print("✓ Found TODO comments - more work needed")
    # Count them
    todo_count = content.count('TODO')
    print(f"  - {todo_count} TODO comments")
else:
    print("✓ No TODO comments found")

# Check if all test functions are complete
import ast
with open('services/data-ingest/tests/test_main.py', 'r') as f:
    tree = ast.parse(f.read())

# Count test functions
functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
test_functions = [f for f in functions if f.name.startswith('test_')]
print(f"✓ Found {len(test_functions)} test functions")

# Check for incomplete test functions (pass statements or early returns)
incomplete = []
for func in test_functions:
    func_source = ast.get_source_segment(content, func)
    if func_source and ('pass' in func_source or 'return' in func_source):
        # Check if it looks like an incomplete test
        if 'pass' in func_source and not func.name.endswith('_pass'):
            incomplete.append(func.name)

if incomplete:
    print(f"⚠ {len(incomplete)} potentially incomplete test functions: {incomplete}")
else:
    print("✓ All test functions appear complete")

# Check for assertions or checks
assert_count = content.count('assert')
print(f"✓ {assert_count} assertion statements")

# Check for edge cases mentioned in the test plan
if 'fetch_from_cafef' in content:
    print("✓ Found CAFEF mocking tests")
if 'fetch_from_vndirect' in content:
    print("✓ Found VNDIRECT mocking tests")
if 'is_trading_day' in content:
    print("✓ Found trading day tests")
if 'run_ingestion_job' in content:
    print("✓ Found ingestion job tests")

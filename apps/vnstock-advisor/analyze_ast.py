import ast

with open('services/data-ingest/tests/test_main.py', 'r') as f:
    content = f.read()

print("=== First 500 characters ===")
print(content[:500])
print("\n=== Last 500 characters ===")
print(content[-500:])

# Try parsing
tree = ast.parse(content)
functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
test_functions = [f for f in functions if f.name.startswith('test_')]

print(f"\n=== AST Parsed Successfully ===")
print(f"Total functions: {len(functions)}")
print(f"Test functions: {len(test_functions)}")

for func in test_functions:
    print(f"- {func.name} (defined at line {func.lineno})")

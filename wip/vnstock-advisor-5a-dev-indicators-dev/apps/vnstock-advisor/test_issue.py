import sys
from pathlib import Path

# Check the current state of the test file
test_file = Path("services/data-ingest/tests/test_main.py")
if test_file.exists():
    print(f"Test file exists: {test_file}")
    print(f"Size: {test_file.stat().st_size} bytes")
    
    # Read and check key sections
    content = test_file.read_text()
    if "vnstock-advisor-6-tester-data-ingest" in content:
        print("Found task reference in test file")
    else:
        print("WARNING: Test file does not reference the expected task")
        print("This suggests the test file may not be the correct version")
else:
    print("ERROR: Test file does not exist")

# Check the current working directory
print(f"\nWorking directory: {Path.cwd()}")

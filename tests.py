from functions.run_python import *

test_cases = [
    ("calculator", "main.py", []),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py", []),
    ("calculator", "../main.py", []),
    ("calculator", "nonexistent.py", []),
]

for working_directory, file, args in test_cases:
    print(f"Result for '{file} {args}' command:")
    result = run_python_file(working_directory, file, args)
    print(result)
    print("-" * 40)
from functions.write_files import *

test_cases = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ispum"),
    ("calculator", "pkg/morelorem.txt", "lorem ispum dolor sit amet"),
    ("calculator", "/tmp/temps.txt", "this should not be allowed"),
]

for working_directory, file, content in test_cases:
    print(f"Result for '{file}' file:")
    result = write_files(working_directory, file, content)
    print(result)
    print("-" * 40)
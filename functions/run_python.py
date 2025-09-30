import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(file_path):
        return f'Error: File "{file_path}" not found.'
    elif not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        args = ["python3", full_path] + args
        result = subprocess.run(args, capture_output=True, text=True, timeout=30, cwd=os.path.abspath(working_directory))
        string_result = "STDOUT: " + result.stdout + "\nSTDERR: " 
        if result.stderr:
            string_result += result.stderr + "\n"
        if result.returncode != 0:
            string_result += f"Process exited with code {result.returncode}"
        if not result.stdout:
            string_result += "No output produced"
        return string_result
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
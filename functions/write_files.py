import os
from google.genai import types


schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Writes content to a specified file, creating directories as needed, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_files(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    full_dir_path = os.path.abspath(os.path.dirname(full_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(file_path):
        try:
            os.makedirs(full_dir_path, exist_ok=True)
        except Exception as e:
            return f"Error: {str(e)}"

    try:
        with open(full_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"

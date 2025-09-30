import os
from config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:

        contents = os.listdir(full_path)
        content = ""
        for file in contents:
            file_path = os.path.join(full_path, file)
            content += f"- {file}: file_size={os.path.getsize(file_path)} bytes"
            if os.path.isdir(file_path):
                content += ", is_dir=True\n"
            else:
                content += ", is_dir=False\n"
        return content
    except Exception as e:
        return f"Error: {str(e)}"

def get_files_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_path, "r") as file:
            file_content = file.read()
            if len(file_content) > MAX_CHARS:
                file_content = file_content[:MAX_CHARS] + f"[...File \"{file_path}\" truncated at 10000 characters]"
            return file_content
    except Exception as e:
        return f"Error: {str(e)}"

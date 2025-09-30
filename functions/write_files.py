import os

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

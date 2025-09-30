import os
from sys import argv, exit
from dotenv import load_dotenv
from google import genai
from google.genai import types
import functions.get_files as get
import functions.write_files as write
import functions.run_python as run

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    verbose = ""
    if len(argv) < 2:
        print("Usage: python main.py '<your prompt here>'")
        exit(1)
    elif len(argv) > 2 and argv[2] == "--verbose":
        verbose = f"User prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\n"

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    user_prompt = argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            get.schema_get_files_info,
            get.schema_get_files_content,
            write.schema_write_files,
            run.schema_run_python_file,
        ]
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.function_calls: 
        for funct in response.function_calls:
            print(f"{verbose}Calling function: {funct.name}({funct.args})")
    else:
        print(f"{verbose}Response: {response.text}")


if __name__ == "__main__":
    main()

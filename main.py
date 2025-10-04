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
    is_verbose = False
    if len(argv) < 2:
        print("Usage: python main.py '<your prompt here>'")
        exit(1)


    user_prompt = argv[1]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
    try:
        for i in range(20):  # Limit to 20 iterations to avoid infinite loops
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )

            if len(argv) > 2 and argv[2] == "--verbose":
                is_verbose = True
                verbose = f"User prompt: {user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}\n"

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if response.function_calls: 
                for funct in response.function_calls:
                    call_content = call_function(funct, is_verbose)
                    messages.append(call_content)
                    if not call_content.parts or not call_content.parts[0].function_response.response:
                        raise Exception("FATAL: No response from function call")
                    if is_verbose:
                        print(f"-> {call_content.parts[0].function_response.response}")
                        

            if response.text and not response.function_calls:
                print(f"{verbose}Final Response: {response.text}")
                break  # Exit if we get a direct text response
    except Exception as e:
        print(f"Error during API call: {str(e)}")


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    working_directory = os.path.abspath("./calculator")
    function_map = {
        "get_files_info": get.get_files_info,
        "get_file_content": get.get_file_content,
        "write_files": write.write_files,
        "run_python_file": run.run_python_file,
    }
    if function_call_part.name not in function_map:
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    result = function_map[function_call_part.name](working_directory, **function_call_part.args)
    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

if __name__ == "__main__":
    main()

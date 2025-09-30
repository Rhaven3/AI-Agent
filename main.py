import os
from sys import argv, exit
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

    user_prompt = argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    print(f"{verbose}Response: {response.text}")


if __name__ == "__main__":
    main()

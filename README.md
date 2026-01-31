# AI Agent in Python with [boot.dev](https://www.boot.dev/u/rhaven)
I built this project to dive into a few key areas I’m excited about:

**Multi-directory** Python projects: I wanted to get hands-on experience structuring a Python project across multiple directories—something I know I’ll encounter in real-world development.

**Under the hood of AI tools**: Since I’ll likely use AI tools in my future career, I was curious to understand how they actually work when building something from scratch.

**Python & functional programming:** This is a chance to sharpen my Python skills and explore functional programming concepts in a practical way.
Important note: This isn’t about building an LLM from scratch. Instead, it’s about using a pre-trained LLM (like Google’s Gemini API) to create a custom agent—step by step, function by function.

---

## What Does the Agent Do?

This program is a **CLI tool** that:
- Accepts a coding task (e.g., *"strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽"*).
- Chooses from a set of predefined functions to work on the task, such as:
  - Scanning files in a directory
  - Reading a file's contents
  - Overwriting a file's contents
  - Executing the Python interpreter on a file
- Repeats the process until the task is complete (or it fails, which is possible).

### Example Use Case
For instance, if you have a buggy calculator app, you can use the agent to fix the code:

```bash
uv run main.py "fix my calculator app, it's not starting correctly"
```
The agent will then:

- Call ``get_files_info``
- Call ``get_file_content``
- Call ``write_file``
- Call ``run_python_file``

Repeat steps as needed

Final response:
*"Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way."*

## How to build it

### Prerequisites

- Python 3.10+ installed
- uv project/package manager (see [installation docs](https://github.com/astral-sh/uv#installation))
- An API key from [Google's Gemini API](https://ai.google.dev/gemini-api/docs/pricing)

---

(optional if you already have your own api key)
1. Create an account on [Google AI Studio](aistudio.google.com/api-keys) if you don't already have one.
2. Click the "Create API Key" button. Here are the [docs](https://ai.google.dev/gemini-api/docs/api-key) if you get lost.

3. Clone the repository and navigate to the project directory.
```bash
git clone https://github.com/Rhaven3/AI-Agent
```

4. Configure your API key in the ``.env`` file:
```bash
GEMINI_API_KEY="your_api_key_here"
```










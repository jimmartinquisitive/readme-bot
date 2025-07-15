# ai_generator.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables and configure the API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY in your .env file.")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-2.5-pro')

def generate_readme(repo_name: str, file_contents: dict) -> str:
    """
    Generates a README.md file content using the Gemini API.

    Args:
        repo_name: The name of the repository.
        file_contents: A dictionary of file paths and their content.

    Returns:
        A string containing the generated README.md content.
    """
    print("\n🤖 AI is analyzing the code and generating the README...")

    # Consolidate all the code into a single string for the prompt
    code_context = ""
    for path, content in file_contents.items():
        code_context += f"--- File: {path} ---\n{content}\n\n"

    # If the context is too large, we might need to truncate it,
    # but for now, we'll send it as is.
    # A more advanced version could summarize files first.

    if not code_context:
        print("⚠️ No code content was provided to the AI. Cannot generate README.")
        return "# README\n\nProject description could not be generated as no code was found."

    prompt = f"""
    You are an expert technical writer. Your task is to generate a comprehensive and professional README.md file for a GitHub repository.

    Analyze the following code context from the repository named '{repo_name}'. The context contains the content of multiple files.

    **Code Context:**
    {code_context}

    **Instructions:**
    Based on the code provided, create a complete README.md file. The README should be well-structured, easy to understand, and include the following sections:

    1.  **Project Title:** Use the repository name `{repo_name}` as the main title.
    2.  **Description:** A detailed explanation of what the project does. Infer the primary purpose from the code.
    3.  **Features:** A bulleted list of the key features or capabilities of the project.
    4.  **Getting Started:**
        * **Prerequisites:** List any languages, frameworks, or tools that need to be installed. Mention the `requirements.txt` if present.
        * **Installation:** Provide a simple, step-by-step guide on how to set up the project locally.
    5.  **Usage:** Explain how to run the application or use the library. Provide code examples if applicable.
    6.  **File Structure (Optional):** Briefly describe the purpose of the most important files and directories.

    Use Markdown formatting. Do not include any introductory phrases like "Here is the README I generated for you." Only output the raw Markdown content for the README.md file starting with the `# {repo_name}` title.
    """

    try:
        response = model.generate_content(prompt)
        print("✅ README content generated successfully!")
        return response.text
    except Exception as e:
        print(f"❌ An error occurred with the AI generation: {e}")
        return f"# {repo_name}\n\nError generating README. The AI model failed to produce a response."

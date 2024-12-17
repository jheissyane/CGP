import json
import openai
from core.config import settings
from modules.token_counter import count_tokens

openai.api_key = settings["openai_api_key"]

def determine_exclusions(filenames: list) -> dict:
    """
    Receives a list of filenames and determines the extensions and names to exclude.
    Uses OpenAI to generate `extensions_to_exclude` and `exclude_names` based on the file list.
    """
    prompt = f"""
You are an expert software architect with over 10 years of experience.
You have been provided with the following list of filenames from a project:

{json.dumps(filenames, indent=2)}

### Task ###
Analyze the provided filenames and determine:
1. `extensions_to_exclude`: A list of file extensions that should be excluded from processing. These are usually files like compiled binaries, temporary files, or non-code assets.
2. `exclude_names`: A list of specific directory or file names that should be excluded from processing, such as build directories or IDE configuration files.

### Instructions ###
- Respond strictly with a valid JSON object.
- The JSON object must contain two keys:
  - `extensions_to_exclude`: An array of file extensions to exclude (e.g., [".class", ".tmp", ".log"]).
  - `exclude_names`: An array of file or directory names to exclude (e.g., ["build", "node_modules", ".git"]).
- Do NOT include any explanations, text, or formatting such as triple backticks (` ``` `).

### Example Response ###
{{
  "extensions_to_exclude": [".class", ".tmp", ".log"],
  "exclude_names": ["build", "node_modules", ".git"]
}}

### Additional Considerations ###
- Ensure the suggestions align with best practices for the language or framework commonly used in projects containing these filenames.
- Focus on excluding irrelevant or redundant files to streamline processing.
"""

    prompt_tokens = count_tokens(prompt)
    if prompt_tokens > 16000:
        raise Exception("Prompt too long. Please provide a shorter list of filenames.")

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a software architecture expert."},
                  {"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=16383,
    )

    try:
        # Extract the raw response from OpenAI
        raw_response = response["choices"][0]["message"]["content"].strip()
        
        # Parse the JSON response
        parsed_response = json.loads(raw_response)

        return parsed_response
    except json.JSONDecodeError as e:
        print(f"Error interpreting JSON response: {e}")
        return {"extensions_to_exclude": [], "exclude_names": []}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"extensions_to_exclude": [], "exclude_names": []}
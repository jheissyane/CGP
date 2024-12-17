"""
Agent for analyzing business rules and determining necessary changes.
"""

import openai
from core.config import settings
from modules.token_counter import count_tokens
import json

openai.api_key = settings["openai_api_key"]

def analyze_business_rule(directory_structure: str, rule: str) -> list:
    """
    Receives a directory structure and a business rule.
    Uses OpenAI to determine the files and the order of modifications.
    Ensures that the output contains only pure file names without prefixes or folder paths.
    """
    prompt = f"""
You are a software engineering expert with more than 10 years of experience. 
**You will receive a directory structure of a project**
And have received the following business rule:
{rule}

### Task ###
Analyze the existing directory structure and determine:
1. Which files need to be modified or created.
2. The order in which these modifications or creations should occur.

### Instructions ###
- Respond strictly with a valid JSON array.
- Do NOT include any explanations, text, or formatting such as triple backticks (` ``` `).
- Ensure the JSON contains objects with the following fields:
  - "file": The path to the file that needs to be modified or created.
  - "order": The order in which the files should be modified or created.
  - "action": Either "create" or "modify" to indicate the action to take on each file.
- Do not include any other text, metadata, or information outside the JSON array.

### Example Response ###
[
    {{"file": "D:/jheis/Documents/FindUs/TCC-FindUs/src/main/java/com/findus/models/Admin.java", "order": 1, "action": "create"}},
    {{"file": "D:/jheis/Documents/FindUs/TCC-FindUs/src/main/java/com/findus/models/Usuario.java", "order": 2, "action": "modify"}}
]

### Additional Considerations ###
- Include only files relevant to implementing the business rule.
- Follow best practices and ensure consistency with the existing structure.
- If the business rule requires creating new entities, ensure they integrate logically with the existing files.
"""
    

    prompt_tokens = count_tokens(prompt)
    if prompt_tokens > 16000:
        raise Exception("Prompt too long. Please provide a shorter prompt.")
    

    print(directory_structure)
    print(rule)

    messages = [{"role": "system", "content": prompt}]
    for chunk in directory_structure:
        messages.append({"role": "user", "content": json.dumps(chunk, indent=2)})


    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=messages,
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
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

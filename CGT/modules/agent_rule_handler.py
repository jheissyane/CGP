"""
Agent for analyzing business rules and determining necessary changes.
"""

import openai
from core.config import settings
from modules.token_counter import count_tokens

openai.api_key = settings["openai_api_key"]

def analyze_business_rule(directory_structure: str, rule: str) -> list:
    """
    Receives a directory structure and a business rule.
    Uses OpenAI to determine the files and the order of modifications.
    Ensures that the output contains only pure file names without prefixes or folder paths.
    """
    prompt = f"""
You are a software engineering expert with more than 10 years of experience. 
You have received the following directory structure of a project:

{directory_structure}

And the following business rule:

"{rule}"

Identify which files need to be modified and/or created, and in what order, to implement the business rule. 
Respond in JSON format with the fields: "file" (file name) and "order" (modification order).
DO NOT include any additional information or explanations.

### Task ###
Analyze the existing directory structure and determine:
1. Which files need to be modified or created.
2. The order in which these modifications or creations should occur.
3. Ensure consistency with the existing structure and best practices.

### Instructions ###
- Provide the response strictly in JSON format.
- Each JSON entry must include the fields:
  - "file": The pure file name (e.g., "UserService.java"). Do not include paths or prefixes.
  - "order": The sequence in which the modifications or creations should be executed.
- Consider creating new files if necessary to implement the rule properly.
- Do not include any prefixes or folder paths in the "file" field.
- Ensure that the "file" field contains only the file name.
- Provide the "order" field to indicate the sequence of modifications or creations.
- Do not provide additional explanations or any text outside the JSON format.
- Only provide the file names that *REALLY* need to be modified or created.

### Example Response ###
[
    {{"file": "AdminRole.java", "order": 1, "action": "create"}},
    {{"file": "UserController.java", "order": 2, "action": "modify"}},
]

### Additional Considerations ###
- If the business rule requires new entities, ensure they integrate logically with existing files.
- Maintain consistency with existing naming conventions and directory structures.
- Only list files that are truly necessary for the implementation.
"""
    
    prompt_tokens = count_tokens(prompt)
    if prompt_tokens > 8000:
        raise Exception("Prompt too long. Please provide a shorter prompt.")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a software architecture expert."},
                  {"role": "user", "content": prompt}],
    )
    
    try:
        # Extract the raw response from OpenAI
        raw_response = response["choices"][0]["message"]["content"]
        parsed_response = eval(raw_response)

        return parsed_response
    except Exception as e:
        print(f"Error interpreting response: {e}")
        return []

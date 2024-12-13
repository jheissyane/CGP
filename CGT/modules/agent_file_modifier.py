import openai
from core.config import settings

openai.api_key = settings["openai_api_key"]

def modify_file(filepath: str, content: str, rule: str, context: dict) -> str:
    """
    Receives a file, the content, the business rule, and the context.
    Uses OpenAI to modify the file according to the business rule, 
    maintaining consistency with previous changes.
    """
    previous_changes = "\n".join(context.get("changes", []))  # History of previous changes
    prompt = f"""
You are a senior software developer with more than 10 years of experienc helping to add changes to code files according to a business rule.

Business Rule: "{rule}"

File to be modified: {filepath}

Source code:
{content}

History of changes:
{previous_changes}

Now, based on the business rule, the provided source code (if provided), and the history of changes (if provided), 
generate the necessary code for the file {filepath}. 
Make sure that the generated code complies with previous modifications without breaking consistency.
Make sure to follow best practices and maintain the existing code structure.
Do not provide any additional information or context.
Do not provide incomplete or incorrect code.
Avoid any responses like "here's your code" or "here's a basic example". 
The response should be exclusively the code for the file,
without additional explanations or comments.

#Rules:
- *Never* provide additional information or comments.
- Maintain consistency with previous changes.
- If the history of changes is empty, disregard this rule.
- Make sure the code is a complete, standalone implementation for this specific file
- If the source code is empty, disregard this rule and provide the modification according to the business rule.
- If the source code is provided, make sure the modification is consistent with it.
- Never provide additional information about the context or business rule.
- Only provide the code for the current file.
- Do not provide incomplete or incorrect code.
- If the response is not correct, state that it was not possible to generate the modification.
- If no changes are necessary, do not provide code.
- It should return the complete file, not just the modification.
- Always follow best programming practices.
- Implement all the methods

Example response:
```
 public class HelloWorld {{
     public static void main(String[] args) {{
         System.out.println("Hello, World!");
     }}
 }}
 ```
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a software development assistant."},
                  {"role": "user", "content": prompt}],
    )
    
    try:
        implementation = response["choices"][0]["message"]["content"]
        
        # Adds the generated modification to the history of changes in the context
        context.setdefault("changes", []).append(f"File: {filepath}\n{implementation}")
        
        return implementation
    except Exception as e:
        print(f"Error interpreting response: {e}")
        return ""

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
generate the necessary and **complete code** for the file {filepath}.
Always provide the code as a **standalone implementation** **without placeholders, missing parts, or comments like "//implement this" or "TODO".**
Ensure the following:
- The code is consistent with previous modifications.
- Follow best practices and maintain the existing structure and style.
- Do not provide incomplete, incorrect, or placeholder code.
- Do not include comments explaining the changes or logic; only provide the code.
- If no changes are required, do not return any code.
- If the source code is empty, create the implementation entirely from the business rule.

Rules:
1. **Do not include placeholders or incomplete code.**
2. Always return the full, standalone implementation of the file.
3. Ensure consistency with any previous changes in the history.
4. Do not include any explanations or context beyond the code itself.
5. Return the entire file, not just the modified parts.
6. If it is not possible to generate a valid modification, return no code at all.
7. Each file must have a unique implementation. Follow the best practices and conventions of the language.

Example of valid response:
```
 public class HelloWorld {{
     public static void main(String[] args) {{
         System.out.println("Hello, World!");
     }}
 }}
 ```

Example of not valid response:
```
public class HelloWorld {{
    // Logic for the main method
}}
```
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
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

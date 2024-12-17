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
generate the necessary and **complete code** for the **file {filepath}**.
Always provide the code as a **standalone implementation** **without placeholders, missing parts, or comments like "//implement this" or "TODO".**
Ensure the following:
- The code is consistent with previous modifications.
- Follow best practices and maintain the existing structure and style.
- Do not provide incomplete, incorrect, or placeholder code.
- Do not include comments explaining the changes or logic; only provide the code.
- If no changes are required, do not return any code.
- If the source code is empty, create the implementation entirely from the business rule.
- Strictly follow all the rules provided.

**Strictly follow these rules:**
1. The file must contain **exactly one class**. Do not include more than one class, interface, or enum in the file.
2. The code must be consistent with previous modifications.
3. Follow best practices and maintain the existing structure and style.
4. Do not include incomplete, incorrect, or placeholder code.
5. Do not include comments explaining the changes or logic; only provide the code.
6. If no changes are required, do not return any code.
7. If the source code is empty, create the implementation entirely from the business rule.
8. Each file must have a unique implementation and only the code for **this specific file**: {filepath}.
9. Do not include any unrelated logic or classes that do not belong to this file.

Example of valid response:
```
 public class HelloWorld {{
     public static void main(String[] args) {{
         System.out.println("Hello, World!");
     }}
 }}
 ```

Example of NOT valid response:
```
public class HelloWorld {{
    // Logic for the main method
}}

public class AnotherClass {{
    // 
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

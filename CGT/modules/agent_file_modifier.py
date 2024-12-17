import openai
from core.config import settings

openai.api_key = settings["openai_api_key"]

def modify_file(filepath: str, content: str, rule: str, changes:list ) -> str:
    """
    Receives a file, the content, the business rule, and the context.
    Uses OpenAI to modify the file according to the business rule, 
    maintaining consistency with previous changes.
    """
    prompt = f"""
Act as a senior software developer with more than 10 years of experience. Your are supposed to add changes to code files according to a business rule.
 
Now, based on the business rule, the provided source code (if provided) and the context of changes : {changes},
you must generate all the necessary implementation and the **complete code** for the file: **{filepath}**.

#RULES
- Each file must contain *one and only one* class, interface, or enum.
- The code must be consistent with previous modifications.
- You must follow all the best practices and maintain the existing structure and coding style.
- Do not include incomplete or unimplemented methods or code placeholders.
- **To-Dos or Placeholders ARE NOT ALLOWED**
- No explanation is needed, only show me the code.
- If no changes are required, do not return any code.
- If the source code is empty, you must create the implementation entirely from the business rule.
- Each file must have an unique implementation and only the code for the specific file: **{filepath}**
- **Do not include any unrelated logic or classes that do not belong to this file.**
- Add a message at the ending indicating if all the code have been generated.
- Don't generate any kind of examples of usage.
- Generate only what I ask for.
- **Strictly follow all the rules I provided.**
"""
    
    prompt_user = f"""
#Business Rule: 
 {rule}

#File to be modified: 
{filepath}

#Source code:
{content}

 """
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": prompt_user}],
        temperature=0,
        max_tokens=16383,
    )

    try:
        implementation = response["choices"][0]["message"]["content"]
        
        # Adds the generated modification to the history of changes in the context
        # context.setdefault("changes", []).append(f"File: {filepath}\n{implementation}")
        
        return implementation
    except Exception as e:
        print(f"Error interpreting response: {e}")
        return ""

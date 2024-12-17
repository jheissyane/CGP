import openai
from core.config import settings

openai.api_key = settings["openai_api_key"]

def enrich_business_rule(rule: str) -> str:
    """
    Receives a business rule and enhances it with detailed context and structure.
    Uses OpenAI to generate a well-structured user story and additional details.

    Parameters:
        rule (str): The input business rule.

    Returns:
        str: A detailed and enriched business rule.
    """
    prompt = f"""
You are a software engineering and product management expert.

You have received the following business rule:

"{rule}"

Your task is to enhance this business rule by transforming it into a detailed and structured format that includes:

1. **User Story**: Write the user story with the format:
   - **As a** (role/persona),
   - **I want** (desired feature or functionality),
   - **So that** (benefit or goal).

2. **Acceptance Criteria**: List specific criteria that must be met for the implementation to be considered complete.

3. **Detailed Requirements**: Provide a breakdown of technical requirements, including:
   - Any classes or modules that need to be created or modified.
   - Relationships between entities (e.g., one-to-many, many-to-many).
   - Permissions or access control specifications.
   - User interface updates or considerations.
   - Security measures.

4. **Priority and Effort Estimate**: Specify the priority (e.g., High, Medium, Low) and provide a rough estimate of the implementation effort (e.g., Low, Medium, High).

Ensure the output is clear, concise, and adheres to best practices for software development and product management.

### Example Output ###
**User Story:**
As a product manager, I want to introduce an Admin role with specific permissions, so that administrators can efficiently manage user accounts within the system.

**Acceptance Criteria:**
1. Admin role must be able to view, edit, and delete all user accounts.
2. Ensure only admins have access to these functionalities.

**Detailed Requirements:**
- Create a new Admin class with defined permissions.
- Modify the existing Usuário class to accommodate the Admin role.
- Implement role-based access control (RBAC) for Admin functionalities.
- Update the UI to include admin-specific features.
- Conduct comprehensive testing for permissions and security.

**Priority:** High
**Effort Estimate:** Medium

"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a software development and product management expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=16383,
    )

    try:
        # Extract the enhanced rule from the AI response
        enhanced_rule = response["choices"][0]["message"]["content"]
        return enhanced_rule
    except Exception as e:
        print(f"Error interpreting response: {e}")
        return "Error generating enriched business rule."

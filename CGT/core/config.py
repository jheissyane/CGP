import os

"""
Configurações do projeto.
"""

settings = {
    "project_name": "Project Structure Manager",
    "version": "1.0.0",
    "debug": True,
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "path_to_project": os.getenv("PATH_TO_PROJECT"),
}

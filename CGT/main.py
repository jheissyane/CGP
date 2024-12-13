"""
Project entry point.
"""

from modules.directory_reader import get_files_tree
from modules.agent_rule_handler import analyze_business_rule
from modules.agent_file_modifier import modify_file
from modules.read_file_content import read_file_content
from modules.filter_unnecessary_files import filter_unnecessary_files
from modules.agent_rule_enricher import enrich_business_rule
from core.config import settings

def main():
    # Repository path
    path = settings["path_to_project"]

    # Reading the directory structure
    structure = get_files_tree(path)

    print("Directory Structure:")
    print(structure)

    extensions_to_exclude = [
        ".class", ".tmp", ".log", ".iml", ".bak"
    ]
    exclude_names = [
        "build", "target", ".gradle", "out", "node_modules", ".idea", ".DS_Store", "Thumbs.db"
    ]

    filtered_tree = filter_unnecessary_files(structure, extensions_to_exclude, exclude_names)

    filenames = []
    for item in filtered_tree:
        filenames.append(item["filename"])

    # Business rule
    rule = "Adicionar um usuário administrador com as seguintes permissões: visualizar todos os usuários, editar todos os usuários, excluir todos os usuários"

    rule = enrich_business_rule(rule)
    print(f"\nEnriched Business Rule: {rule}")

    # Rule analysis
    try:
        changes = analyze_business_rule(filenames, rule)
        print("\nFiles to be modified and order:")
        for change in changes:
            print(change)
    except Exception as e:
        print(f"Error analyzing business rule: {e}")
        return
    
    context = {}

    for change in changes:
        target_file = change["file"]
        print(f"\nProcessing file: {target_file}")
        
        file_path = None
        content = None
        file_found = False

        for item in filtered_tree:
            if target_file in item["filename"]:
                file_found = True
                try:
                    file_path = item["path"]
                    content = read_file_content(file_path)
                    implementation = modify_file(target_file, content, rule, context)
                    print(f"\n{target_file} updated:")
                    print(implementation)
                except Exception as e:
                    print(f"Error modifying file {file_path}: {e}")
                    break
                break
        
        if not file_found:
            try:
                implementation = modify_file(target_file, "", rule, context)
                print(f"\n{target_file} created:")
                print(implementation)
            except Exception as e:
                print(f"Error creating file {target_file}: {e}")


if __name__ == "__main__":
    main()

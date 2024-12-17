"""
Project entry point.
"""

from modules.directory_reader import get_files_tree
from modules.agent_rule_handler import analyze_business_rule
from modules.agent_file_modifier import modify_file
from modules.read_file_content import read_file_content
from modules.filter_unnecessary_files import filter_unnecessary_files
from modules.agent_rule_enricher import enrich_business_rule
from modules.agent_file_filter import determine_exclusions
from core.config import settings
from modules.split_structure_to_chunks import split_structure_to_chunks
import os

def main():
    # Repository path
    path = settings["path_to_project"]

    # Reading the directory structure
    structure, basenames = get_files_tree(path)

    print("Directory Structure:")
    print(structure)

    print("\nFormatted Basenames:")
    print(basenames)

    # Determining exclusions
    exclusions = determine_exclusions(basenames)
    
    extensions_to_exclude = exclusions["extensions_to_exclude"]
    exclude_names = exclusions["exclude_names"]

    
    filtered_tree = filter_unnecessary_files(structure, extensions_to_exclude, exclude_names)

    # Split the structure into chunks
    chunks = split_structure_to_chunks(filtered_tree, 8000)

    # Business rule
    rule = "Adicionar um usuário administrador com as seguintes permissões: visualizar todos os usuários, editar todos os usuários, excluir todos os usuários"

    rule = enrich_business_rule(rule)
    print(f"\nEnriched Business Rule: {rule}")

    # Rule analysis
    try:
        changes = analyze_business_rule(chunks, rule)
        print("\nFiles to be modified and order:")
        for change in changes:
            print(change)
    except Exception as e:
        print(f"Error analyzing business rule: {e}")
        return
    

    for change in changes:
        target_file = change["file"]
        file_name = os.path.basename(target_file)
        print(f"\nProcessing file: {target_file}")
        
        file_path = None
        content = None
        file_found = False

        for item in filtered_tree:
            if file_name in item["filename"]:
                file_found = True
                try:
                    file_path = item["path"]
                    content = read_file_content(file_path)
                    implementation = modify_file(file_path, content, rule, changes)
                    print(f"\n{target_file} updated:")
                    print(implementation)
                except Exception as e:
                    print(f"Error modifying file {file_path}: {e}")
                    break
                break
        
        if not file_found:
            try:
                implementation = modify_file(target_file, "implement the entire file", rule, changes)
                print(f"\n{target_file} created:")
                print(implementation)
            except Exception as e:
                print(f"Error creating file {target_file}: {e}")


if __name__ == "__main__":
    main()

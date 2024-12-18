import os 

def get_files_tree(directory_path):
    """
    Returns the structure of files and directories in a specific format,
    along with a separate list of basenames formatted hierarchically.

    Args:
        directory_path (str): The directory path to traverse.

    Returns:
        tuple: A tuple containing:
            - A list of dictionaries with the names and paths of the files and directories.
            - A formatted string of basenames in a hierarchical structure.
    """
    def recursive_list(path):
        tree = []
        basenames = []

        
        if os.path.isdir(path):
            basename = os.path.basename(path)
            tree.append({
                "filename": f"{basename}",
                "rel_path": os.path.relpath(path, directory_path).replace("\\", "/"),
                "path": path.replace("\\", "/")
            })

            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                sub_tree, sub_basenames = recursive_list(item_path)
                tree.extend(sub_tree)
                basenames.extend(sub_basenames)
        else:
            basename = os.path.basename(path)
            tree.append({
                "filename": basename.replace("\\", "/"),
                "rel_path": os.path.relpath(path, directory_path).replace("\\", "/"),
                "path": path.replace("\\", "/") 
            })
            basenames.append(f"{basename}")

        return tree, basenames

    tree, basenames = recursive_list(directory_path)
    
    # Join basenames with newlines to create a hierarchical structure
    formatted_basenames = "\n".join(basenames)
    
    return tree, formatted_basenames
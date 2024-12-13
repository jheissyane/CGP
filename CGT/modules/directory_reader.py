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
    def recursive_list(path, prefix="1."):
        tree = []
        basenames = []
        counter = 1

        if os.path.isdir(path):
            basename = os.path.basename(path)
            tree.append({
                "filename": f"{prefix} {basename}/",
                "path": path.replace("\\", "/") + "/"
            })
            basenames.append(f"{prefix} {basename}/")

            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                next_prefix = f"{prefix}{counter}."
                sub_tree, sub_basenames = recursive_list(item_path, next_prefix)
                tree.extend(sub_tree)
                basenames.extend(sub_basenames)
                counter += 1
        else:
            basename = os.path.basename(path)
            tree.append({
                "filename": f"{prefix} {path.replace('\\', '/').replace(directory_path.replace('\\', '/'), '')}",
                "path": path.replace("\\", "/")
            })
            basenames.append(f"{prefix} {basename}")

        return tree, basenames

    tree, basenames = recursive_list(directory_path)
    
    # Join basenames with newlines to create a hierarchical structure
    formatted_basenames = "\n".join(basenames)
    
    return tree, formatted_basenames
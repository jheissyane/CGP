import os

def get_files_tree(directory_path):
    """
    Returns the structure of files and directories in a specific format.

    Args:
        directory_path (str): The directory path to traverse.

    Returns:
        list: A list of dictionaries with the names and paths of the files and directories.
    """
    def recursive_list(path, prefix="1."):
        tree = []
        counter = 1

        if os.path.isdir(path):
            tree.append({
                "filename": f"{prefix} {os.path.basename(path)}/",
                "path": path.replace("\\", "/") + "/"
            })

            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                next_prefix = f"{prefix}{counter}."
                tree.extend(recursive_list(item_path, next_prefix))
                counter += 1
        else:
            tree.append({
                "filename": f"{prefix} {os.path.basename(path)}",
                "path": path.replace("\\", "/")
            })

        return tree

    return recursive_list(directory_path)

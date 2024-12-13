def filter_unnecessary_files(file_tree, extensions_to_exclude=None, exclude_names=None):
    """
    Filters out unnecessary files from the file tree based on specified criteria.

    Args:
        file_tree (list): List of dictionaries representing the file tree structure.
        extensions_to_exclude (list, optional): List of file extensions to exclude. Defaults to None.
        exclude_names (list, optional): List of filenames or substrings to exclude. Defaults to None.

    Returns:
        list: Filtered file tree with only necessary files and directories.
    """
    if extensions_to_exclude is None:
        extensions_to_exclude = []
    if exclude_names is None:
        exclude_names = []

    filtered_tree = []
    
    for item in file_tree:
        # Get the file name and extension
        filename = item["filename"].lower()
        path = item["path"].lower()

        # Check if it is a directory (ends with '/')
        is_directory = filename.endswith("/")

        # Exclude files based on extensions
        if not is_directory and any(filename.endswith(ext) for ext in extensions_to_exclude):
            continue

        # Exclude files or directories based on specific names
        if any(exclude_name in path for exclude_name in exclude_names):
            continue

        filtered_tree.append(item)

    return filtered_tree
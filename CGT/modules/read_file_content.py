def read_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The full path of the file.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading the file {file_path}: {e}"

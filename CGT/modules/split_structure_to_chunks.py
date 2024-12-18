def split_structure_to_chunks(structure, max_tokens):
    # Helper: Approximate token size for a given item
    def get_token_count(item):
        return (len(item['rel_path'])) // 4

    # Split the structure into chunks based on max_tokens
    chunks = []
    current_chunk = []
    current_tokens = 0

    for item in structure:
        item_tokens = get_token_count(item)
        if current_tokens + item_tokens > max_tokens:
            # Start a new chunk when the limit is exceeded
            chunks.append(current_chunk)
            current_chunk = [item]
            current_tokens = item_tokens
        else:
            # Add item to the current chunk
            current_chunk.append(item)
            current_tokens += item_tokens

    # Append the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
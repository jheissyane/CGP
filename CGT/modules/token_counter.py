import tiktoken

def count_tokens(content, model="gpt-4o"):
    """
    Count the number of tokens in the given content for the specified model.

    Args:
        content (str): The content to count the tokens for.
        model (str): The model to use for token counting. Defaults to "gpt-4o".

    Returns:
        int: The number of tokens in the content.

    """
    try:
        # Get the encoding for the specified model
        encoding = tiktoken.encoding_for_model(model)
        # Count the tokens in the content
        token_count = len(encoding.encode(content))
        return token_count
    except KeyError:
        raise ValueError(f"Model '{model}' not supported for token counting.")

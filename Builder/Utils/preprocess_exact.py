import re

def preprocess_ex(text):
    """
    Applies a basic text preprocessing pipeline:
    - Converts text to lowercase
    - Removes punctuation (excluding asterisks and hyphens temporarily)
    - Removes hyphens

    Args:
        text (str): The raw input string to preprocess.

    Returns:
        str: The cleaned and lowercased text.
    """

    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation (keep * and - initially), also remove underscores
    text = re.sub(r'[^\w\s*-]|_', ' ', text)

    # Remove hyphens explicitly
    text = text.replace("-", "")

    return text

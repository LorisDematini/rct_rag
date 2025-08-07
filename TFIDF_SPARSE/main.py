import re

def preprocess_ex(text):
    """
    Preprocesses the input text for exact keyword matching.

    Steps:
    1. Converts the text to lowercase for case-insensitive comparison.
    2. Removes punctuation except for hyphens (-) and asterisks (*), which may be used in wildcard queries.
    3. Removes hyphens explicitly (treats hyphenated words as single words).

    Args:
        text (str): The input string to preprocess.

    Returns:
        str: A cleaned and normalized version of the input text.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s*-]|_', ' ', text)  # Remove punctuation except * and -
    text = text.replace("-", "")
    return text

def preprocess_query_ex(query):
    """
    Preprocesses a query string using the exact preprocessing routine.

    Args:
        query (str): The user query to preprocess.

    Returns:
        str: The preprocessed version of the query.
    """
    query_cleaned = preprocess_ex(query)
    return query_cleaned

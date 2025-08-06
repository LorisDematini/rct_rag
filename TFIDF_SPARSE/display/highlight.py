import re

def highlight_text_sparse(text: str, raw_query: str, cleaned_query: str) -> str:
    """
    Highlights all keywords from the raw and cleaned queries within the given text by wrapping them in <mark> HTML tags.

    Args:
        text (str): The text in which to highlight keywords.
        raw_query (str): The original user query string.
        cleaned_query (str): The preprocessed/cleaned version of the query.

    Returns:
        str: The text with keywords highlighted using <mark> tags.
    """
    keywords = set()
    # Extract words from both queries, lowercase for case-insensitive matching
    keywords.update(re.findall(r"\b\w+\b", raw_query.lower()))
    keywords.update(re.findall(r"\b\w+\b", cleaned_query.lower()))

    # Sort keywords by length descending to highlight longer matches first (avoid partial overlap issues)
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        # Replace matched words with highlighted version
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text
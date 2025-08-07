import re

def highlight_text_sparse(text: str, raw_query: str, cleaned_query: str) -> str:
    """
    Highlights all keywords from the raw and cleaned queries within the given text by wrapping them in <mark> HTML tags.

    This function is typically used for highlighting matches in sparse vector search (e.g., TF-IDF),
    where both the original query and its cleaned (preprocessed) version are considered.

    Args:
        text (str): The text in which to highlight keywords.
        raw_query (str): The original user query string.
        cleaned_query (str): The preprocessed/cleaned version of the query.

    Returns:
        str: The text with keywords highlighted using <mark> tags.
    """
    keywords = set()
    # Extract keywords from both the raw and cleaned queries
    keywords.update(re.findall(r"\b\w+\b", raw_query.lower()))
    keywords.update(re.findall(r"\b\w+\b", cleaned_query.lower()))

    # Sort keywords by length in descending order to avoid partial overlapping (e.g., "air" inside "airway")
    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)  # Highlight matches using <mark>
    return text


def highlight_text_exact(text, query, mode="PHRASE"):
    """
    Highlights search terms in the text using HTML <mark> tags, depending on the query mode.

    This function is used for exact search highlighting, supporting phrase, AND, OR, and wildcard (*) queries.

    Args:
        text (str): The text to highlight.
        query (str): The user's original query.
        mode (str): The search mode - either "PHRASE", "AND", or "OR".

    Returns:
        str: The text with highlighted terms.
    """
    if mode == "PHRASE":
        if query.endswith("*"):
            # Highlight all words starting with the given prefix (wildcard search)
            prefix = re.escape(query[:-1])
            pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
        else:
            # Highlight exact phrase matches
            pattern = re.compile(rf"\b({re.escape(query)})\b", flags=re.IGNORECASE)
        return pattern.sub(r"<mark>\1</mark>", text)

    elif mode in ("AND", "OR"):
        # Split query into terms while ignoring the "and"/"or" operators
        terms = [t.strip() for t in re.split(r"\s+(and|or)\s+", query.lower()) if t.lower() not in {"and", "or"}]

        # Highlight each term individually
        for word in sorted(terms, key=len, reverse=True):
            if word.endswith("*"):
                prefix = re.escape(word[:-1])
                pattern = re.compile(rf"\b({prefix}\w*)\b", flags=re.IGNORECASE)
            else:
                pattern = re.compile(rf"\b({re.escape(word)})\b", flags=re.IGNORECASE)
            text = pattern.sub(r"<mark>\1</mark>", text)
    return text

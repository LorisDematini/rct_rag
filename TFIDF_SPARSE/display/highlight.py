import re

def highlight_text_sparse(text, raw_query, cleaned_query):
    keywords = set()
    keywords.update(re.findall(r"\b\w+\b", raw_query.lower()))
    keywords.update(re.findall(r"\b\w+\b", cleaned_query.lower()))

    for word in sorted(keywords, key=len, reverse=True):
        pattern = re.compile(rf"(\b{re.escape(word)}\b)", flags=re.IGNORECASE)
        text = pattern.sub(r"<mark>\1</mark>", text)
    return text
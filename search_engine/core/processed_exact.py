import re

def preprocess_ex(text):
    #minuscules
    text = text.lower()
    #ponctuation
    text = re.sub(r'[^\w\s*-]|_', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text.replace("-", "")

    return text

def preprocess_query_ex(query):
    query_cleaned = preprocess_ex(query)
    return query_cleaned
import re

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

def preprocess_ex(text):
    #minuscules
    text = text.lower()
    #ponctuation
    text = re.sub(r'[^\w\s*-]|_', ' ', text)
    text = text.replace("-", "")

    return text

def preprocess_query(query):
    query_cleaned = preprocess_ex(query)
    return query_cleaned
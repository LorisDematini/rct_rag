
import json
import re
import unicodedata
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

acronyms_file = "/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/final_acronyms.json"

def replace_acronyms(acronyms, text):
        for acronym, definition in acronyms.items():
            pattern = r'\b' + re.escape(acronym) + r'\b'
            text = re.sub(pattern, definition.lower(), text, flags=re.IGNORECASE)
        return text

def preprocess(text):

    #1. Remplace les acronymes
    with open(acronyms_file, 'r', encoding='utf-8') as f:
                acronyms = json.load(f)
    text = replace_acronyms(acronyms, text)
    
    #2. utf-8 : Sans accent/cédille/signe bizarre
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

    #3. Retire tout caractères autre que - lettres chiffres
    text = re.sub(r'[^\w\s+-]|_', ' ', text)
    text = text.replace("-", "")
    #Espace en trop
    text = re.sub(r'\s+', ' ', text).strip()

    #print("DEBUT : ",text)
    #4. Minusculise le texte
    text = text.lower()

    # Remplace d+chiffre par "day chiffre"
    text = re.sub(r'\bd(\d+)\b', r'day \1', text)
    # Remplace w+chiffre par "week chiffre"
    text = re.sub(r'\bw(\d+)\b', r'week \1', text)
    # Remplace m+chiffre par "month chiffre"
    text = re.sub(r'\bm(\d+)\b', r'month \1', text)
    
    
    #Stopwords
    words = text.split()
    words = [word for word in words if word not in stop_words and len(word)>=2]
    text = ' '.join(words)

    return text

#LEMMING

test = 'Happy_Birthday; hello-world/ \n , of the Duration of inclusions l ® ! ?  cdeis  m10 w5'

test = preprocess(test)
print("FIN : ",test)
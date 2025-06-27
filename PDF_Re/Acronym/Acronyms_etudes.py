import re
import json
from nltk.corpus import stopwords
import os 

STOPWORDS = set(stopwords.words('english'))

base_path = os.getcwd()

input_json = os.path.join(base_path,"final_output.json")
output_json = os.path.join(base_path, "Acronym", "acronyms_etude.json")

def extract_acronyms_with_definitions(text):
    results = {}
    
    #Parentheses sans espace
    for match in re.finditer(r'\((\S+?)\)', text):
        #Enleve les parentheses
        candidate = match.group(1)

        #exclut les candidats avec espaces ou chiffres ou pas de majuscule
        if ' ' in candidate or re.search(r'\d', candidate) or not re.search(r'[A-Z]', candidate):
            continue

        acronym = candidate

        if len(acronym) <= 1:
            continue

        start_pos = match.start()

        definition = None
        
        if acronym[-1] == 's' and len(acronym) > 1:
            # Version 1: acronyme avec 's' final => définition sur len(acronym)-1 mots précédents,
            # le dernier mot doit finir par un 's'
            # Extraire les n-1 mots avant la parenthèse
            words_before = get_words_before(text, start_pos, len(acronym)-1)
            definition = version_s_final(acronym, words_before)
        
        if not definition:
            # Version 2: correspondance stricte lettre par lettre avec mots précédents
            words_before = get_words_before(text, start_pos, len(acronym))
            definition = version_2(acronym, words_before)
        
        if not definition:
            # Version 3: premier mot avant parenthèse contient toutes les lettres dans l'ordre
            words_before = get_words_before(text, start_pos, 1)
            definition = version_3(acronym, words_before)
        
        if not definition:
            # Version 4: fenêtre élargie (2x acronyme), suppression stopwords, 
            # initiales des mots dans l'ordre correspondant à l'acronyme
            words_before = get_words_before(text, start_pos, len(acronym)*2)
            definition = version_4(acronym, words_before)
        
        if definition and acronym not in results:
            results[acronym] = ' '.join(definition)

    return results

def get_words_before(text, pos, window):
    """
    Récupère les mots précédant la position pos dans le texte,
    avec une fenêtre max.
    """
    text_before = text[:pos].strip()
    words = re.findall(r'\b\w+\b', text_before)
    return words[-window:]

def version_s_final(acronym, words):
    """
    acronyme finissant par 's' minuscule
    on prend len(acronym)-1 mots avant, le dernier doit finir par 's'
    """
    n = len(acronym) - 1
    if len(words) < n:
        return None
    candidate_words = words[-n:]
    last_word = candidate_words[-1]
    if not last_word.endswith('s'):
        return None
    
    # On vérifie que les initiales des n premiers mots correspondent aux n-1 premières lettres de l'acronyme
    for i in range(n - 1):
        if candidate_words[i][0].lower() != acronym[i].lower():
            return None
    # On vérifie que la dernière lettre avant le s final correspond à la lettre avant le s dans l'acronyme
    if last_word[0].lower() != acronym[-2].lower():
        return None

    return candidate_words

def version_2(acronym, words):
    """
    Correspondance stricte, chaque lettre de l'acronyme doit être
    la première lettre des mots précédents dans l'ordre
    """
    n = len(acronym)
    if len(words) < n:
        return None
    candidate_words = words[-n:]
    for i, letter in enumerate(acronym):
        if candidate_words[i][0].lower() != letter.lower():
            return None
    return candidate_words

def version_3(acronym, words):
    """
    Le premier mot avant la parenthèse contient toutes les lettres
    de l'acronyme dans l'ordre (lettres peuvent être non consécutives)
    """
    if not words:
        return None
    first_word = words[-1]
    a_idx = 0
    for char in first_word.lower():
        if a_idx < len(acronym) and char == acronym[a_idx].lower():
            a_idx += 1
    if a_idx == len(acronym):
        return [first_word]
    return None

def version_4(acronym, words):
    """
    Fenêtre élargie de 2*len(acronym) mots
    Suppression stopwords
    Vérifie que les initiales des mots contiennent l'acronyme (de droite à gauche)
    """
    window_size = 2 * len(acronym)
    if len(words) < window_size:
        window_words = words
    else:
        window_words = words[-window_size:]

    filtered_words = [w for w in window_words if w.lower() not in STOPWORDS]

    a_idx = len(acronym) - 1
    selected_words = []

    for w in reversed(filtered_words):
        if a_idx >= 0 and w[0].lower() == acronym[a_idx].lower():
            selected_words.insert(0, w)
            a_idx -= 1
        if a_idx < 0:
            break

    if a_idx < 0:
        return selected_words

    return None


if __name__ == "__main__":
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    acronyms_by_study = {}
    for study_id, study in data.items():
        text = " ".join(str(v) for v in study.values())
        acronyms = extract_acronyms_with_definitions(text)
        if acronyms:
            acronyms_by_study[study_id.upper()] = acronyms
    
    total_acro = sum(len(v) for v in acronyms_by_study.values())
    print(f"{total_acro} acronymes uniques avec définition trouvés dans {len(acronyms_by_study)} études :\n")
    
    for study_id, acronyms in acronyms_by_study.items():
        print(f"\nÉtude : {study_id}")
        for acro, definition in acronyms.items():
            print(f"  {acro}: {definition}")

    cleaned_ids = {study_id.split('_')[0]: acronyms for study_id, acronyms in acronyms_by_study.items()}

    with open(output_json, "w", encoding="utf-8") as f_out:
        json.dump(cleaned_ids, f_out, ensure_ascii=False, indent=2)
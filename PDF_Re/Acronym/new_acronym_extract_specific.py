import itertools
import re
import json

def extract_acronyms_with_definitions(text):
    results = {}

    # toutes les parentheses sans espaces
    for match in re.finditer(r'\((\S+?)\)', text):
        candidate = match.group(1)
        
        #On ignore si espace, pas de majuscule ou contient un chiffre
        if ' ' in candidate or not re.search(r'[A-Z]', candidate) or re.search(r'\d', candidate):
            continue

        acronym = candidate
        #index du début
        start = match.start()

        #window avant l'acronyme pour récupérer la définition
        window = text[max(0, start - 300):start]
        window_words = re.findall(r'\b\w+\b', window)

        # On ne garde que les derniers mots possibles + largeur au cas où (3)
        candidates = window_words[-(len(acronym) + 3):]

        first_letter = acronym[0].lower()
        if not any(w[0].lower() == first_letter for w in candidates):
            continue

        definition = try_hierarchical_match(acronym, candidates)

        if definition and acronym not in results:
            results[acronym] = ' '.join(definition)

    return results

def try_hierarchical_match(acronym, words):
    acronym = acronym.lower()
    acro_len = len(acronym)

    #Version 1 : Basique mot par mot pour lettre par lettre
    for i in range(len(words) - acro_len + 1):
        segment = words[i:i + acro_len]
        if all(segment[j][0].lower() == acronym[j] for j in range(acro_len)):
            return segment
    
    #Version 2 : On boucle sur les mots de la window en supprimant un par un pour voir si il n'y pas des mots parasites dedans
    if len(words) >= acro_len:
        indices = list(range(len(words)))
        for combo in itertools.combinations(indices, acro_len):
            if list(combo) != sorted(combo):
                continue
            segment = [words[i] for i in combo]
            initials = [w[0].lower() for w in segment]
            if ''.join(initials) == acronym:
                return segment

    #Version 3 : On boucle sur un ensemble de mots plus petits pour voir si un mot final ne comprend pas toutes les lettres restantes 
    for n in range(acro_len - 1, 0, -1):
        for i in range(len(words) - n + 1):
            segment = words[i:i + n]

            if len(segment) < 2:
                continue

            matched_letters = [w[0].lower() for w in segment]
            if acronym[:n] == ''.join(matched_letters):
                remaining = acronym[n:]
                last_word = segment[-1]

                a_idx = 0
                for char in last_word[1:].lower():
                    if a_idx < len(remaining) and char == remaining[a_idx]:
                        a_idx += 1

                if a_idx == len(remaining):
                    return segment  

    #Version 4 : Définition en 1 seul mot, on boucle sur les lettres d'un mot et de l'acronyme
    for word in reversed(words):
        if word[0].lower() not in acronym:
            continue
        w_idx = 0
        a_idx = 0
        while w_idx < len(word) and a_idx < len(acronym):
            if word[w_idx].lower() == acronym[a_idx]:
                a_idx += 1
            w_idx += 1
        if a_idx == len(acronym):
            return [word]

    return None




# Chargement du fichier JSON
with open("/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extraction par étude
acronyms_by_study = {}

for study_id, study in data.items():

    text = " ".join(str(value) for value in study.values())
    acronyms = extract_acronyms_with_definitions(text)

    if acronyms:
        acronyms_by_study[study_id.upper()] = acronyms

# Affichage
total_acronyms = sum(len(v) for v in acronyms_by_study.values())
print(f"{total_acronyms} acronymes uniques avec définition trouvés dans {len(acronyms_by_study)} études :\n")

for study_id, acronyms in acronyms_by_study.items():
    print(f"\nÉtude : {study_id}")
    for acro, definition in acronyms.items():
        print(f"  {acro}: {definition}")

cleaned_ids = {study_id.split('_')[0]: acronyms for study_id, acronyms in acronyms_by_study.items()}

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronyms_parenthese_clean.json", "w", encoding="utf-8") as f_out:
    json.dump(cleaned_ids, f_out, ensure_ascii=False, indent=2)

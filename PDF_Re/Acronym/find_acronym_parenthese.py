import re
import json

def extract_acronyms_with_definitions(text):
    results = {}

    for match in re.finditer(r'\((\b[A-Z]{2,7})\b[^)]*\)', text):
        acronym = match.group(1)
        start = match.start()
        
        window = text[max(0, start - 100):start]
        window_words = re.findall(r'\b\w+\b', window)[-len(acronym)-1:]

        definition_words = []
        acronym_index = 0
        for word in window_words:
            if acronym_index < len(acronym) and word[0].lower() == acronym[acronym_index].lower():
                definition_words.append(word)
                acronym_index += 1

        if acronym_index == len(acronym) and acronym not in results:
            results[acronym] = ' '.join(definition_words)

    return results

with open("/home/loris/Stage/STAGE/Test/PDF_RE/final_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

all_text = ""
for study in data.values():
    all_text += " ".join(str(value) for value in study.values()) + " "

acronym_dict = extract_acronyms_with_definitions(all_text)

print(f"{len(acronym_dict)} acronymes uniques avec définition trouvés :\n")
for acro, definition in acronym_dict.items():
    print(f"{acro}: {definition}")

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Acronym/acronyms_with_definitions.json", "w", encoding="utf-8") as f_out:
    json.dump(acronym_dict, f_out, ensure_ascii=False, indent=2)

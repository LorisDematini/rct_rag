import json
import re
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
words_dont = ["be", "day", "week", "month", 'year', "kg", "ml", "g", "mg", "ph", "ng", "cm", "mm", "nm", "min", "cal", "kcal", "ppm", "ppb", "mm2", "mm3"]
roman_to_arabic = {"i": "1","ii": "2","iii": "3","iv": "4"}
# ,"v": "5","vi": "6","vii": "7","viii": "8","ix": "9"
acronym_generaux = {"vs" : "versus"}

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    return 'n'

def lemmatize_text(tokens):
    pos_tags = pos_tag(tokens)
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token, get_wordnet_pos(pos)) for token, pos in pos_tags]

def replace_all_variants(text, acronym, definition):
    variants = {acronym, acronym.upper(), acronym.lower()}
    for variant in variants:
        text = re.sub(r'\(' + re.escape(variant) + r'\)', ' ', text)
        pattern = r'(?<!\w)' + re.escape(variant) + r'(?!\w)'
        text = re.sub(pattern, f' {definition.lower()} ', text)
    return text

def replace_acronyms(acronyms_all, study_id, text):
    acronyms_study = acronyms_all.get(study_id, {})
    for acronym, definition in acronyms_study.items():
        text = replace_all_variants(text, acronym, definition)
    return text

def trace_preprocessing(input_json_path, acronyms_path, output_txt="trace.txt", output_json="trace.json"):
    with open(input_json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    with open(acronyms_path, "r", encoding="utf-8") as f:
        acronyms_all = json.load(f)

    trace_result = {}

    for study_id, sections in raw_data.items():
        trace_result[study_id] = {}
        for section_name, entries in sections.items():
            original = " ".join(entries)
            trace = {
                "originale": original
            }
            step = original

            #3: Unicode
            step = unicodedata.normalize("NFKD", step).encode("ASCII", "ignore").decode("utf-8")
            trace["UTF_8"] = step

            
            for acro, defi in acronym_generaux.items():
                step = re.sub(rf'\b{acro}\b', f' {defi} ', step)
            trace["Acronymes generaux"] = step

            #1: Acronymes
            step = replace_acronyms(acronyms_all, study_id, step)
            trace["Acronymes"] = step

            tokens = word_tokenize(step)
            #2: Lemma
            tokens = lemmatize_text(tokens)
            trace["Lemma"] = tokens
            step = " ".join(tokens)

            #4: Lower
            step = step.lower()
            trace["Lower"] = step

            #5: ponctuation
            step = re.sub(r'[^\w\s-]|_', ' ', step)
            step = step.replace("-", "")
            step = re.sub(r'\s+', ' ', step).strip()
            trace["Ponctuation"] = step

            #6: stopwords et petits
            tokens = word_tokenize(step)
            tokens = [w for w in tokens if (w not in stop_words or w.isdigit()) and (len(w) > 1 or w.isdigit())]
            trace["stopword et lettre"] = tokens

            step = ' '.join(tokens)

            #7: chiffres romains
            for roman, arabic in sorted(roman_to_arabic.items(), key=lambda x: -len(x[0])):
                pattern = rf'(?<![a-zA-Z]){roman}(?=\s|[-.,/])'
                step = re.sub(pattern, f'{arabic}', step, flags=re.IGNORECASE)

            #7: phase
            step = re.sub(r'\bphase\s+(\d+)\b', r'phase\1', step)
            step = re.sub(r'\bgrade\s+(\d+)\b', r'grade\1', step)
            trace["Phase"] = step

            #8: dates et nombres
            step = re.sub(r'\bd(\d+)\b', " ", step)
            step = re.sub(r'\bw(\d+)\b', " ", step)
            step = re.sub(r'\bm(\d+)\b', " ", step)
            step = re.sub(r'\b\d+\b', " ", step)
            step = re.sub(r'\b\d+x\d+\b', ' ', step)
            trace["nombres et dates"] = step
            
            #9: unite et temporal
            tokens = word_tokenize(step)
            unit_pattern = re.compile(rf"^\d+(\.\d+)?({'|'.join(re.escape(u) for u in words_dont)})$", re.IGNORECASE)
            tokens = [w for w in tokens if w not in words_dont and not unit_pattern.match(w)]
            trace["unite et temporal"] = tokens
            trace["final"] = " ".join(tokens)

            trace_result[study_id][section_name] = trace

    #txt 
    with open(output_txt, "w", encoding="utf-8") as f:
        for study_id, sections in trace_result.items():
            f.write(f"\n==== {study_id} ====\n")
            for section, steps in sections.items():
                f.write(f"\n--- [{section}] ---\n")
                for step, content in steps.items():
                    f.write(f"\n// {step} \\\\\n")
                    f.write(content if isinstance(content, str) else " ".join(content))
                    f.write("\n")
    
    #Json
    final_result = {
        study_id: {
            section: trace["final"]
            for section, trace in sections.items()
        }
        for study_id, sections in trace_result.items()
    }
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(final_result, f, ensure_ascii=False, indent=2)

trace_preprocessing("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/debug_input.json", "/home/loris/Stage/STAGE/Test/PDF_RE/TFIDF_SearchEngine_V2/data/extracted_acronym_final.json", "/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/debug.txt", "/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/debug_output.json")
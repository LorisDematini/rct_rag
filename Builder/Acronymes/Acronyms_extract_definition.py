import os
import re
import json
from typing import Dict, List, Optional
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))

def extract_acronyms_with_definitions(text: str) -> Dict[str, str]:
    """
    Extract acronyms and their possible definitions from a given text.
    Uses different versions to connect acronyms to their definitions.
    """
    results = {}

    # Find all patterns like (ABC) in the text
    for match in re.finditer(r'\((\S+?)\)', text):
        candidate = match.group(1)

        # Skip if contains space, digits, or not uppercase letters
        if ' ' in candidate or re.search(r'\d', candidate) or not re.search(r'[A-Z]', candidate):
            continue

        acronym = candidate
        # Ignore single-character acronyms
        if len(acronym) <= 1:
            continue  

        start_pos = match.start()
        definition = None

        # Try plural form detection strategy
        if acronym[-1] == 's' and len(acronym) > 1:
            words_before = get_words_before(text, start_pos, len(acronym)-1)
            definition = acronym_s_final(acronym, words_before)

        # Try standard one-word-per-letter strategy
        if not definition:
            words_before = get_words_before(text, start_pos, len(acronym))
            definition = acronym_initials(acronym, words_before)

        # Try matching acronym within one long word like molecules
        if not definition:
            words_before = get_words_before(text, start_pos, 1)
            definition = acronym_long(acronym, words_before)

        # Try larger context window
        if not definition:
            words_before = get_words_before(text, start_pos, len(acronym)*2)
            definition = acronym_big_window(acronym, words_before)

        # If a definition was found and acronym is new, store it
        if definition and acronym not in results:
            results[acronym] = ' '.join(definition)

    return results

def get_words_before(text: str, pos: int, window: int) -> List[str]:
    """
    Extract the last 'window' number of words before the given position.
    """
    text_before = text[:pos].strip()
    words = re.findall(r'\b\w+\b', text_before)
    return words[-window:]

def acronym_s_final(acronym: str, words: List[str]) -> Optional[List[str]]:
    """
    Strategy for acronyms ending in 's' (plural)
    """
    n = len(acronym) - 1
    if len(words) < n:
        return None
    candidate_words = words[-n:]
    last_word = candidate_words[-1]
    if not last_word.endswith('s'):
        return None
    for i in range(n - 1):
        if candidate_words[i][0].lower() != acronym[i].lower():
            return None
    if last_word[0].lower() != acronym[-2].lower():
        return None
    return candidate_words

def acronym_initials(acronym: str, words: List[str]) -> Optional[List[str]]:
    """
    Each letter in acronym matches the first letter of a word.
    """
    if len(words) < len(acronym):
        return None
    candidate_words = words[-len(acronym):]
    for i, letter in enumerate(acronym):
        if candidate_words[i][0].lower() != letter.lower():
            return None
    return candidate_words

def acronym_long(acronym: str, words: List[str]) -> Optional[List[str]]:
    """
    The acronym letters are embedded in one long word
    """
    if not words:
        return None
    first_word = words[-1]
    a_idx = 0
    for char in first_word.lower():
        if a_idx < len(acronym) and char == acronym[a_idx].lower():
            a_idx += 1
    return [first_word] if a_idx == len(acronym) else None

def acronym_big_window(acronym: str, words: List[str]) -> Optional[List[str]]:
    """
    Match acronym letters to the initials of content words in a bigger window.
    """
    window_size = 2 * len(acronym)
    window_words = words[-window_size:] if len(words) >= window_size else words
    filtered_words = [w for w in window_words if w.lower() not in STOPWORDS]

    a_idx = len(acronym) - 1
    selected_words = []

    for w in reversed(filtered_words):
        if a_idx >= 0 and w[0].lower() == acronym[a_idx].lower():
            selected_words.insert(0, w)
            a_idx -= 1
        if a_idx < 0:
            break

    return selected_words if a_idx < 0 else None

def extract_acronyms_from_json(input_json_path: str, output_json_path: str) -> None:
    """
    Load a JSON file with study and contents, extract acronyms and their definitions,
    then save the results in a JSON file.
    """
    # Load the input JSON file
    with open(input_json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    acronyms_by_study = {}

    # Loop on each study
    for study_id, study in data.items():
        # Merge all fields into one large
        text = " ".join(str(v) for v in study.values())

        # Extract acronyms from the text
        acronyms = extract_acronyms_with_definitions(text)

        if acronyms:
            acronyms_by_study[study_id.upper()] = acronyms

    # Print
    total_acro = sum(len(v) for v in acronyms_by_study.values())
    print(f"{total_acro} acronymes trouvés dans {len(acronyms_by_study)} études.")

    # Keep prefix before _ or / of study's title
    cleaned_ids = {
        re.split(r'[_/]', study_id)[0]: acronyms
        for study_id, acronyms in acronyms_by_study.items()
    }

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Save output to JSON file
    with open(output_json_path, "w", encoding="utf-8") as f_out:
        json.dump(cleaned_ids, f_out, ensure_ascii=False, indent=2)

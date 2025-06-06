import json
from nltk.corpus import wordnet as wn
from collections import defaultdict
from nltk import word_tokenize

def build_canonical_map(tokens):
    canonical_map = {}
    canonical_corpus = defaultdict(list)

    for token in tokens:
        synsets = wn.synsets(token, pos=wn.NOUN)
        if not synsets:
            canonical_map[token] = token
            if token not in canonical_corpus[token]:
                canonical_corpus[token].append(token)
            continue

        lemmas = [lemma.name().replace('_', ' ') for lemma in synsets[0].lemmas()]
        found = False
        for lemma in lemmas:
            if lemma in canonical_corpus:
                canonical_map[token] = lemma
                if token not in canonical_corpus[lemma]:
                    canonical_corpus[lemma].append(token)
                found = True
                break

        if not found:
            canonical_map[token] = token
            if token not in canonical_corpus[token]:
                canonical_corpus[token].append(token)

    return canonical_map, canonical_corpus

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_preprocessed_lemma.json", "r", encoding="utf-8") as f:
    data = json.load(f)

output = {}

for study_id, sections in data.items():
    output[study_id] = {}
    for section_title, text in sections.items():
        tokens = word_tokenize(text)
        canonical_map, canonical_corpus = build_canonical_map(tokens)
        output[study_id][section_title] = {
            "canonical_map": canonical_map,
            "canonical_corpus": dict(canonical_corpus)
        }

with open("/home/loris/Stage/STAGE/Test/PDF_RE/Preprocess/sections_canonical.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

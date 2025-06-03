from nltk.corpus import wordnet as wn
from collections import defaultdict

def build_canonical_map(tokens):
    canonical_map = {}
    canonical_corpus = defaultdict(list)

    for token in tokens:
        # Get synsets (noun-only here)
        synsets = wn.synsets(token, pos=wn.NOUN)
        if not synsets:
            # No synsets: treat the token as its own canonical
            canonical_map[token] = token
            if token not in canonical_corpus[token]:
                canonical_corpus[token].append(token)
            continue

        # Use first synset as representative concept
        lemmas = [lemma.name().replace('_', ' ') for lemma in synsets[0].lemmas()]
        found = False
        for lemma in lemmas:
            if lemma in canonical_corpus:
                # This synonym is already a canonical key
                canonical_map[token] = lemma
                if token not in canonical_corpus[lemma]:
                    canonical_corpus[lemma].append(token)
                found = True
                break

        if not found:
            # No matching canonical, make this token canonical
            canonical_map[token] = token
            if token not in canonical_corpus[token]:
                canonical_corpus[token].append(token)

    return canonical_map, canonical_corpus

import nltk
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from preprocess_text import preprocess_text
from corpus_design import build_canonical_map
import json
nltk.download('averaged_perceptron_tagger_eng')

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # fallback

def lemmatize_with_pos(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    lemmas = [
        lemmatizer.lemmatize(word, get_wordnet_pos(tag))
        for word, tag in pos_tags
    ]
    return lemmas

if __name__ == "__main__":
    
    # text  ="Anti PD-1 monoclonal antibodies (nivolumab and pembrolizumab) alone or in association with antiCTLA4 (Ipilimumab) are established as indisputable treatment of metastatic melanoma, with unprecedented overall survival, and are indicated for first-line treatment including patients with BRAF mutation. Given their high molecular weight, their penetration in the brain sanctuary is uncertain and relies on disruption of the BBB which occurs occasionally. SonoCloud® is an implantable device delivering low intensity pulsed UltraSound (US). Along with systemic injection of an US resonator, SonoCloud® demonstrated safe and efficient at repetitively opening the BBB. We anticipate that BBB opening could help at increasing brain penetration of monoclonal antibodies and potentially boosting immunity in the brain. This could translate in controlling brain disease with the same magnitude as for extracranial disease. This would also open avenues for optimizing the treatment of brain metastases in combination with checkpoint inhibitors in many other cancers."
    # map, corpus = build_canonical_map(preprocess_text(text))
    # print(map)
    # print(corpus)

    with open('data/corpus_source.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    corpus = []
    for study in data.values():
        corpus.append(" ".join(study.values()))
    
    full_text = " ".join(study for study in corpus)

    print(len(full_text))

    map, corpus = build_canonical_map(preprocess_text(full_text))

    print(len(list(map.keys())))

    print(len(list(corpus.keys())))

    # # Get top 5 keys by length of list
    # top_5 = sorted(corpus.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    # # Output result
    # for key, value in top_5:
    #     print(f"{key} → {value} (length = {len(value)})")

    canonical_text = [map[word] for word in preprocess_text(full_text)]

    print(canonical_text[:100])
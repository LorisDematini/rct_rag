import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return "n"
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return 'n'

# Fonction principale de lemmatisation
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)

    lemmatized_tokens = []
    for token, pos in pos_tags:
        wordnet_pos = get_wordnet_pos(pos)
        lemma = lemmatizer.lemmatize(token, wordnet_pos)
        lemmatized_tokens.append(lemma)

    return lemmatized_tokens

# Texte de test
text = """The children adolescent were playing in the gardens and saw several geese flying over. 
          They have been happier since they started visiting nature more often."""

# Application
lemmatized = lemmatize_text(text)

# Résultat
print("Texte original:")
print(text)
print("\nTexte lemmatisé :")
print(" ".join(lemmatized))

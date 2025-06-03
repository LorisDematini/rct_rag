import string
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Ensure required downloads
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')

# Initialize components
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# POS mapping function
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
        return wordnet.NOUN  # Default to noun

# Main preprocessing function
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # POS tagging
    pos_tags = pos_tag(tokens)
    
    # Filter and lemmatize
    cleaned = []
    for token, tag in pos_tags:
        if token in stop_words:
            continue
        if token.isdigit():
            continue
        if len(token) < 2:
            continue
        wn_pos = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(token, pos=wn_pos)
        cleaned.append(lemma)
    
    return cleaned

if __name__ == "__main__":
    text  ="Anti PD-1 monoclonal antibodies (nivolumab and pembrolizumab) alone or in association with antiCTLA4 (Ipilimumab) are established as indisputable treatment of metastatic melanoma, with unprecedented overall survival, and are indicated for first-line treatment including patients with BRAF mutation. Given their high molecular weight, their penetration in the brain sanctuary is uncertain and relies on disruption of the BBB which occurs occasionally. SonoCloud® is an implantable device delivering low intensity pulsed UltraSound (US). Along with systemic injection of an US resonator, SonoCloud® demonstrated safe and efficient at repetitively opening the BBB. We anticipate that BBB opening could help at increasing brain penetration of monoclonal antibodies and potentially boosting immunity in the brain. This could translate in controlling brain disease with the same magnitude as for extracranial disease. This would also open avenues for optimizing the treatment of brain metastases in combination with checkpoint inhibitors in many other cancers."
    print(preprocess_text(text))
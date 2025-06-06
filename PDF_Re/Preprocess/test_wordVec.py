import json
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

with open("/home/loris/Stage/STAGE/Test/PDF_RE/sections_preprocessed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for study_name, study_content in data.items():
    contenu=""
    for section_name, section_content in study_content.items():
        contenu += section_content
    documents.append(contenu)
print(documents)


#Entraînement Word2Vec sur le contenu
tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]
w2v_model = Word2Vec(tokenized_docs, vector_size=100, window=5, min_count=1, workers=2)


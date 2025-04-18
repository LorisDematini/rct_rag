import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Comparaison/summary-title.json"

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

#Sections
def extract_sections(data, sections=None):
    sections = sections or ['Summary']
    texts = []
    labels = []

    for study_id, study in data.items():
        for section in sections:
            if section in study and isinstance(study[section], str) and study[section].strip():
                texts.append(study[section])
                labels.append((study_id, section))

    return labels, texts

#TF-IDF
def compute_tfidf(data):
    vectorizer = TfidfVectorizer(norm='l1')
    tfidf_matrix = vectorizer.fit_transform(data)
    return vectorizer, tfidf_matrix

#Sections similaires COSINUS
def search(query, vectorizer, tfidf_matrix, labels):
    query_vector = vectorizer.transform([query])
    distances = cosine_similarity(query_vector, tfidf_matrix)
    results = sorted(enumerate(distances[0]), key=lambda x: x[1], reverse=True)

    return [(labels[idx], dist) for idx, dist in results[:6]]


def main():
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)

    if not texts:
        print("Aucune section trouvée dans le fichier JSON.")
        return

    vectorizer, tfidf_matrix = compute_tfidf(texts)
    # Affichage de la matrice TF-IDF (format DataFrame pour lisibilité)


    while True:
        query = input("Entrez une requête de recherche (ou 'exit' pour quitter) : ")
        if query.lower() == 'exit':
            break
        results = search(query, vectorizer, tfidf_matrix, labels)
        print("\nRésultats de la recherche :")
        for (study_id, section), dist in results:
            print(f"Étude : {study_id}, Section : {section}, Similarité : {dist:.4f}")  # Affichage de la similarité au lieu de la distance car pas de -1

if __name__ == "__main__":
    main()
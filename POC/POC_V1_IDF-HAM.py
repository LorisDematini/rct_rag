import json
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import hamming
import numpy as np

json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def extract_sections(data, sections=None):
    sections = sections or ['SUMMARY', 'SCIENTIFIC JUSTIFICATION', 'OBJECTIVES', 'METHODOLOGY', 'PROCEDURE', 'ELIGIBILITY', 'DATA MANAGEMENT', 'STATISTICAL']
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
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data)
    return vectorizer, tfidf_matrix

#Binarisation
def binarize_tfidf(tfidf_matrix, threshold=0.1):
    binary_matrix = tfidf_matrix > threshold
    return binary_matrix.astype(int)

#Sections similaires
def search(query, vectorizer, tfidf_matrix, labels):
    query_vector = vectorizer.transform([query])

    binary_tfidf_matrix = binarize_tfidf(tfidf_matrix)
    binary_query_vector = binarize_tfidf(query_vector)
    
    distances = np.array([hamming(binary_query_vector.toarray()[0], binary_tfidf_matrix[i].toarray()[0]) for i in range(binary_tfidf_matrix.shape[0])])
    
    #Hamming
    results = sorted(enumerate(distances), key=lambda x: x[1])
    
    return [(labels[idx], dist) for idx, dist in results[:5]]

def main():
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)

    if not texts:
        print("Aucune section trouvée dans le fichier JSON.")
        return

    #TF_IDF
    vectorizer, tfidf_matrix = compute_tfidf(texts)

    while True:
        query = input("Entrez une requête de recherche (ou 'exit' pour quitter) : ")
        if query.lower() == 'exit':
            break
        results = search(query, vectorizer, tfidf_matrix, labels)
        print("\nRésultats de la recherche :")
        for (study_id, section), dist in results:
            print(f"Étude : {study_id}, Section : {section}, Distance de Hamming : {dist:.4f}")

if __name__ == "__main__":
    main()

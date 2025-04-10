import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances

json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

#Sections
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

#Sections similaires
def search(query, vectorizer, tfidf_matrix, labels):
    query_vector = vectorizer.transform([query])
    distances = euclidean_distances(query_vector, tfidf_matrix)
    results = sorted(enumerate(distances[0]), key=lambda x: x[1])
    return [(labels[idx], dist) for idx, dist in results[:5]]

def main():
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)

    if not texts:
        print("Aucune section trouvée dans le fichier JSON.")
        return

    vectorizer, tfidf_matrix = compute_tfidf(texts)

    while True:
        query = input("Entrez une requête de recherche (ou 'exit' pour quitter) : ")
        if query.lower() == 'exit':
            break
        results = search(query, vectorizer, tfidf_matrix, labels)
        print("\nRésultats de la recherche :")
        for (study_id, section), dist in results:
            print(f"Étude : {study_id}, Section : {section}, Distance : {dist:.4f}")

if __name__ == "__main__":
    main()

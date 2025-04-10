import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import manhattan_distances

json_file_path = "/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Extract/grouped_titles_preprocessed.json"

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

#Sections
def extract_sections(data, sections=None):
    sections = sections or [
        'SUMMARY', 'SCIENTIFIC JUSTIFICATION', 'OBJECTIVES',
        'METHODOLOGY', 'PROCEDURE', 'ELIGIBILITY',
        'DATA MANAGEMENT', 'STATISTICAL'
    ]
    texts, labels = [], []

    for study_id, study in data.items():
        for section in sections:
            content = study.get(section, "").strip()
            if content:
                texts.append(content)
                labels.append((study_id, section))

    return labels, texts

#TF-IDF
def compute_tfidf(corpus):
    vectorizer = TfidfVectorizer(
        max_df=0.9,
        min_df=2,
        ngram_range=(1, 2)
    )
    tfidf_matrix = vectorizer.fit_transform(corpus)
    
    vocab = list(vectorizer.vocabulary_.keys())
    print(" Vocabulaire appris (30):", vocab[:30])
    return vectorizer, tfidf_matrix

#Manhattan
def search(query, vectorizer, tfidf_matrix, labels, top_k=5):
    query_vec = vectorizer.transform([query])
    print(f"🔎 Vecteur TF-IDF de la requête '{query}' :\n{query_vec}")
    
    if not np.any(query_vec.toarray()):
        print("⚠️ Aucun mot de la requête n’a été reconnu par le modèle TF-IDF.")
        return []

    distances = manhattan_distances(query_vec, tfidf_matrix)[0]  #(1, N) -> [N]
    print("📏 Distances calculées :", distances)
    sorted_results = sorted(enumerate(distances), key=lambda x: x[1])
    return [(labels[i], d) for i, d in sorted_results[:top_k]]

#Main
def main():
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)

    if not texts:
        print("Aucune section trouvée dans le fichier JSON.")
        return

    vectorizer, tfidf_matrix = compute_tfidf(texts)

    while True:
        query = input("Requête (ou 'exit' pour quitter) : ")
        if query.lower() == 'exit':
            print("✅ Fin de la recherche.")
            break

        results = search(query, vectorizer, tfidf_matrix, labels)
        if results:
            print("\nRésultats :")
            for (study_id, section), dist in results:
                print(f" - Étude: {study_id}, Section: {section}, Distance de Manhattan: {dist:.4f}")
        else:
            print("Aucun résultat trouvé.")

if __name__ == "__main__":
    main()

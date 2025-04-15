import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

def compute_tfidf(data):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data)
    return vectorizer, tfidf_matrix

def save_tfidf_matrix(tfidf_matrix, vectorizer, labels, file_path='/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Train/tfidf_matrix.csv'):
    df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=pd.MultiIndex.from_tuples(labels, names=['StudyID', 'Section']))
    df.to_csv(file_path)
    print(f"Matrice TF-IDF sauvegardée dans : {file_path}")
    return df

def save_query_vector(query, vectorizer, file_path='/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Train/query_vector.csv'):
    query_vector = vectorizer.transform([query])
    df_query = pd.DataFrame(query_vector.toarray(), columns=vectorizer.get_feature_names_out())
    df_query.to_csv(file_path, index=False)
    print(f"Vecteur TF-IDF de la requête (complet) sauvegardé dans : {file_path}")
    return df_query

def main():
    data = load_data(json_file_path)
    labels, texts = extract_sections(data)

    if not texts:
        print("Aucune section trouvée dans le fichier JSON.")
        return

    vectorizer, tfidf_matrix = compute_tfidf(texts)
    print(f"\nDimensions de la matrice TF-IDF : {tfidf_matrix.shape[0]} sections x {tfidf_matrix.shape[1]} mots uniques")

    df_tfidf = save_tfidf_matrix(tfidf_matrix, vectorizer, labels)

    query = input("\nEntrez une requête pour générer le vecteur TF-IDF : ")
    df_query = save_query_vector(query, vectorizer)

if __name__ == "__main__":
    main()

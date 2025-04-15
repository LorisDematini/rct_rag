import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

json_path = '/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/summary_tables_gather.json'

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

study_ids = []
documents = []

for study_id, sections in data.items():
    text = " ".join(sections.values()).strip()
    if text:
        study_ids.append(study_id)
        documents.append(text)

#Requête
query_text = ["lung"]

#TF-IDF
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query_text)

doc_vectors = X_docs.toarray()
query_vector = X_query.toarray()[0]

#Distance cosinus
distances = pairwise_distances(doc_vectors, [query_vector], metric='cosine').flatten()


print("\n Résultats de Distance cosinus avec la requête :\n")
for i, (study_id, distance) in enumerate(zip(study_ids, distances)):
    print(f"{i+1}. Study ID: {study_id}")
    print(f"   ➤ Distance cosinus : {distance:.4f}")
    print()

#Distance croissante
sorted_results = sorted(zip(study_ids, distances), key=lambda x: x[1])
print("\n Études les plus proches de la requête :\n")
for rank, (study_id, dist) in enumerate(sorted_results[:5], 1):
    print(f"{rank}. Study ID: {study_id} — Distance : {dist:.4f}")

#TF-IDF des documents
tfidf_doc_df = pd.DataFrame(doc_vectors, index=study_ids, columns=vectorizer.get_feature_names_out())
tfidf_doc_df.to_csv('/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Description/tfidf_matrix_documents.csv')

#TF-IDF de la requête
tfidf_query_df = pd.DataFrame([query_vector], index=["Query"], columns=vectorizer.get_feature_names_out())
tfidf_query_df.to_csv('/home/loris/Stage/STAGE/Test/db_sortie_block/DOC/Summary/Description/tfidf_vector_query.csv')

print("\n Matrices TF-IDF exportées avec succès !")

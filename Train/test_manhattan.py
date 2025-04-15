from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import manhattan_distances
import numpy as np

#Données
documents = ["test salut comment ça va"]
query = ["salut"]

#TF-IDF vectorisation
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

#Affichage des vecteurs
print("Vecteur du texte :", doc_vector)
print("Vecteur de la requête :", query_vector)

#Calcul manuel de la distance de Manhattan
diff = np.abs(doc_vector - query_vector)
distance_manual = np.sum(diff)
print("\n Distance de Manhattan (manuelle) :")
print(f"  Somme des |doc_i - query_i| = {distance_manual:.4f}")

#Calcul avec sklearn
distance_sklearn = manhattan_distances([doc_vector], [query_vector])[0][0]
print("\n Distance de Manhattan (sklearn) :")
print(f"  Résultat sklearn = {distance_sklearn:.4f}")
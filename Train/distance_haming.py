from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import numpy as np

# Données
texte1 = "test salut comment ça va"
documents = [texte1]
query = ["salut"]
print("Texte 1 :", texte1)
print("Requête :", query)


# TF-IDF
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

print("\nVecteur du texte :", doc_vector)
print("Vecteur de la requête :", query_vector)

# === DISTANCE DE HAMMING ===

# Étape 1 : Binarisation des vecteurs
# On met à 1 si un mot est présent (TF-IDF > 0), sinon à 0
doc_binary = (doc_vector > 0).astype(int)
query_binary = (query_vector > 0).astype(int)

print("\nÉtape 1 : Vecteur binaire du texte")
print(f"  doc_binary = {doc_binary}")
print("Vecteur binaire du texte :", doc_binary)
print("Vecteur binaire de la requête :", query_binary)

# Étape 2 : Comparaison des vecteurs binaires (différence)
diff = doc_binary != query_binary
print("\nÉtape 2 : Différence entre les vecteurs binaires")
print(f"  diff = doc_binary != query_binary = {doc_binary} != {query_binary} = {diff}")

# Étape 3 : Calcul de la somme des différences
# La somme des éléments où les valeurs sont différentes (diff == 1)
hamming_manual = np.sum(diff) / len(diff)
print("\nÉtape 3 : Calcul de la distance de Hamming manuelle")
print(f"  hamming_manual = np.sum(diff) / len(diff) = {np.sum(diff)} / {len(diff)} = {hamming_manual}")

# Résultat de la distance de Hamming manuelle
print("\n📏 Distance de Hamming manuelle :", hamming_manual)

# === Calcul avec sklearn ===
hamming_sklearn = pairwise_distances([doc_binary], [query_binary], metric='hamming')[0][0]
print("📏 Distance de Hamming (sklearn) :", hamming_sklearn)

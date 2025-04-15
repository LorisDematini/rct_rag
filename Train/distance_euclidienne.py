from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

# Données
# texte1 = "test salut comment ça salut"
texte2 = "test coucou comment ça coucou salut"
# texte3 = "test comment ça coucou"
documents = [texte2]
query = ["salut"]

print("Texte 1 :", documents[0])
print("Requête :", query)

# TF-IDF
vectorizer = TfidfVectorizer(norm='l2')
X_docs = vectorizer.fit_transform(documents)
X_query = vectorizer.transform(query)

# Vecteurs du texte et de la requête
doc_vector = X_docs.toarray()[0]
query_vector = X_query.toarray()[0]

print("\nVecteur du texte :", doc_vector)
print("Vecteur de la requête :", query_vector)

# === DISTANCE EUCLIDIENNE ===

# Étape 1 : Calcul de la différence entre les vecteurs
diff = doc_vector - query_vector
print("\nÉtape 1 : Différence entre les vecteurs")
print(f"  diff = doc_vector - query_vector = {doc_vector} - {query_vector} = {diff}")

# Étape 2 : Carré de la différence
squared_diff = diff ** 2
print("\nÉtape 2 : Carré des différences")
print(f"  squared_diff = diff ** 2 = {squared_diff}")

# Étape 3 : Somme des carrés des différences
sum_squared_diff = np.sum(squared_diff)
print("\nÉtape 3 : Somme des carrés des différences")
print(f"  sum_squared_diff = np.sum(squared_diff) = {sum_squared_diff}")

# Étape 4 : Racine carrée de la somme des carrés (distance euclidienne)
euclidean_manual = np.sqrt(sum_squared_diff)
print("\nÉtape 4 : Calcul de la distance euclidienne manuelle")
print(f"  euclidean_manual = sqrt(sum_squared_diff) = sqrt({sum_squared_diff}) = {euclidean_manual}")

# Résultat de la distance euclidienne manuelle
print("\n Distance euclidienne manuelle :", euclidean_manual)

# === Calcul avec sklearn ===
euclidean_sklearn = euclidean_distances([doc_vector], [query_vector])[0][0]
print(" Distance euclidienne (sklearn) :", euclidean_sklearn)

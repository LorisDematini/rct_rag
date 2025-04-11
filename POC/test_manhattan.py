from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import manhattan_distances

documents = ["le chat mange le gateau"]
query = ["salut"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents + query)

doc_vector = X[0].toarray()
query_vector = X[1].toarray()

print("Vecteur du texte :", doc_vector)
print("Vecteur de la requête :", query_vector)

distance = manhattan_distances(doc_vector, query_vector)[0][0]
print(f"Distance de Manhattan : {distance}")

from gen_embedding import *
import faiss

if __name__ == "__main__":
    # Load the FAISS index
    index = faiss.read_index("faiss_index.bin")

    # Example query text
    query_text = "COVID-19 treatment protocols"

    query_vector = get_embedding(query_text).reshape(1, -1)

    #Search FAISS for the 2 most similar documents
    k = 2  # Number of results to retrieve
    distances, indices = index.search(query_vector, k)

    # Print results

    #load docuements here
    # Example documents
    documents = [
    "This protocol describes treatment for COVID-19 patients.",
    "The study focuses on lung disease and respiratory symptoms.",
    "Clinical trials have shown promising results for vaccine X."
    ]

    print("Query:", query_text)
    print("\nTop Matching Documents:")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. Document {idx} {documents[idx]} (Distance: {distances[0][i]})")
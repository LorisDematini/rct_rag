from gen_embedding import *
import faiss
import numpy as np
import pickle

def query_faiss(query, top_k=5):
    """Query FAISS and retrieve the top K closest pages."""
    
    # Load FAISS index
    index = faiss.read_index("/root/work/rct_rag/rag/vectordb/faiss_index.bin")
    
    # Load metadata for retrieval
    with open("/root/work/rct_rag/rag/vectordb/faiss_metadata.pkl", "rb") as f:
        metadata = pickle.load(f)

    # Convert query to numpy array (if it's not already)
    query_embedding = np.array(get_embedding(query), dtype="float32").reshape(1, -1)

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)

    # Retrieve corresponding file/page metadata
    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        file_name, page_number = metadata[idx]
        results.append({
            "file": file_name,
            "page": page_number,
            "distance": distances[0][i]  # Lower is better for L2 distance
        })

    return results

if __name__ == "__main__":
    # Example: Query with a new embedding
    query = "cluster analysis"
    top_matches = query_faiss(query)

    print(query)
    print(top_matches)

    # Print results
    for match in top_matches:
        print(f"File: {match['file']}, Page: {match['page']}, Distance: {match['distance']:.4f}")

import numpy as np
import faiss #Facebook AI Similarity Search #optimized for efficient similarity search,
from gen_embedding import *

if __name__ == "__main__":
    
    #load documents here
    # Example documents
    documents = [
    "This protocol describes treatment for COVID-19 patients.",
    "The study focuses on lung disease and respiratory symptoms.",
    "Clinical trials have shown promising results for vaccine X."
    ]

    # Convert all documents to vectors
    vectors = np.array([get_embedding(doc) for doc in documents])

    # Initialize FAISS index (L2 similarity)
    embedding_dim = vectors.shape[1]  # Should be 1536
    index = faiss.IndexFlatL2(embedding_dim)

    # Add vectors to FAISS index
    index.add(vectors)

    # Save FAISS index
    faiss.write_index(index, "faiss_index.bin")

    print(f"Stored {index.ntotal} embeddings in FAISS!")
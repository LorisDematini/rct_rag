import numpy as np
import faiss #Facebook AI Similarity Search #optimized for efficient similarity search,
# from gen_embedding import *
import pickle

if __name__ == "__main__":
    
##test

    with open("/root/work/rct_rag/rag/data/embeddings.pkl", "rb") as f:
        data = pickle.load(f)

    embedding_dim = 1536
    index_id_map = faiss.IndexFlatL2(embedding_dim)  # FAISS index for L2 distance (Euclidean) ; OpenAI embedding shape is 1536
    metadata = []  # Store (file_name, page_number)

    all_embeddings = []
    for file_name, pages in data.items():
        print(file_name)
        for page_number, embedding in pages.items():
            # if embedding_dim is None:
            #     embedding_dim = embedding.shape[0]  # Set embedding dimension dynamically
            all_embeddings.append(embedding)  # Collect embeddings
            metadata.append((file_name, page_number))  # Store metadata

    # Convert list to numpy array
    all_embeddings = np.vstack(all_embeddings).astype("float32")

    # Create a FAISS index with the correct dimensions
    index = faiss.IndexFlatL2(embedding_dim)  # L2 distance (Euclidean) index
    index.add(all_embeddings)  # Add embeddings to the index

    # Save the FAISS index for later use
    faiss.write_index(index, "vectordb/faiss_index.bin")

    # Save metadata for retrieval
    with open("vectordb/faiss_metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print(f"Stored {len(all_embeddings)} embeddings in FAISS!")

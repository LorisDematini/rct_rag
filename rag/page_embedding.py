import numpy as np
import pickle  # For saving the dictionary with filenames
from gen_embedding import *  # Assuming this file contains get_embedding function

def save_embeddings(documents_dict, output_path='embeddings.pkl'):
    embeddings_dict = {}

    for filename, pages in documents_dict.items():
        print(filename)
        embeddings_dict[filename] = {}  # Ensure we maintain {filename: {page_number: embedding}}

        for page_number, text in pages.items():
            # Generate embedding for each page
            page_embedding = np.array(get_embedding(text))

            # Store the embedding in the correct format
            embeddings_dict[filename][page_number] = page_embedding

    # Save the dictionary with embeddings to a pickle file
    with open(output_path, 'wb') as f:
        pickle.dump(embeddings_dict, f)

    print(f"Saved embeddings dictionary to {output_path}")

if __name__ == "__main__":

##test
#     documents_dict = {
#     "file1.pdf": {
#         1: "Text from page 1 of file1.pdf",
#         2: "Text from page 2 of file1.pdf",
#     },
#     "file2.pdf": {
#         1: "Text from page 1 of file2.pdf",
#         2: "Text from page 2 of file2.pdf",
#         3: "Text from page 3 of file2.pdf",
#     }
# }
    # save_embeddings(documents_dict, '/root/work/rct_rag/rag/data/embedings.pkl')

    text_dict = '/root/work/rct_rag/rag/data/pages.pkl'
    with open(text_dict, 'rb') as f:
        documents_dict = pickle.load(f)
    
    # Call the function to save embeddings
    save_embeddings(documents_dict, '/root/work/rct_rag/rag/data/embedings.pkl')
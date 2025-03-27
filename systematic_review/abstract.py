######################
 
import pandas as pd
import sys
import os
import numpy as np
from tqdm import tqdm
import pickle

####################

sys.path.append(os.path.abspath("../config"))
sys.path.append(os.path.abspath("../rag"))
from config import configure_openai
configure_openai()
from gen_embedding import *

#####################

df = pd.read_csv("C:/DonneesLocales/vsc/rag_project/rct_rag/systematic_review/data/dose_finding_review.csv")
max_window = 2048

### preprocessing
df.dropna(subset=["abstract"], inplace=True)
df["text"] = df["titre"] + df["abstract"]
df = df[["record_id", "text"]]

# ### visualizint the chunks
# chunks = chunk_text(df["text"].iloc[0])
# first_chunk = chunks[0]
# tokens = enc.encode(first_chunk)

# with open("data/tokenized_first_chunk.txt", "w", encoding="utf-8") as f:
#     f.write("--- Original Text ---\n")
#     f.write(first_chunk + "\n\n")
#     f.write("--- Token Breakdown ---\n")

#     for i, token in enumerate(tokens):
#         decoded = enc.decode([token])
#         f.write(f"Token {i+1}: '{decoded}' (ID: {token})\n")

embeddings_dict = {}
max_tokens=1000

for index, row in tqdm(df.iterrows()):

    embeddings_dict[row["record_id"]] = get_embedding_text(row["text"], max_tokens)

with open("data/embeddings.pkl", "wb") as f:
    pickle.dump(embeddings_dict, f)

print("completed db embedding")
"""
Framework for generating a dense embedding of an any sized text
It is based on 
- chunking the text
- embedding each chunk
- mean pooling the obtained embedding
"""

from openai import OpenAI
import numpy as np
import tiktoken

#OPENAI_API_KEY is stored in a .venv file at root
# can also be saved as an environment variable (export OPENAI_API_KEY="your_openai_api_key")
client = OpenAI()

#tiktoken is a fast BPE tokeniser for use with OpenAI's models 
#https://github.com/openai/tiktoken?tab=readme-ov-file
enc = tiktoken.encoding_for_model("text-embedding-ada-002") 

#Simple OpenAI embedding https://platform.openai.com/docs/guides/embeddings
def get_embedding_chunk(chunk):
    response = client.embeddings.create(
        input=chunk,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding)

def mean_pool(embeddings): #basic mean pooling
    return np.mean(embeddings, axis=0)

def chunk_text(text, max_tokens=1000): #to optimize
    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = enc.decode(tokens[i:i + max_tokens])
        chunks.append(chunk)
    return chunks

def get_embedding_text(text, max_tokens=1000) : #chunks the text, get embedding for each chunk and mean_pools the embeddings
    chunks = chunk_text(text, max_tokens)
    chunk_embeddings = [get_embedding_chunk(chunk) for chunk in chunks]
    text_embedding = mean_pool(chunk_embeddings)
    return text_embedding

if __name__ == "__main__":
    
    # Example document
    protocol_text = "This protocol describes treatment for COVID-19 patients."
    protocol_vector = get_embedding_chunk(protocol_text)
    print(protocol_vector)
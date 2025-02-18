from openai import OpenAI
import numpy as np

#Simple OpenAI embedding https://platform.openai.com/docs/guides/embeddings
#OPENAI_API_KEY was sstored as an environment variable (export OPENAI_API_KEY="your_openai_api_key")

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return np.array(response.data[0].embedding)

if __name__ == "__main__":
    
    # Example document
    protocol_text = "This protocol describes treatment for COVID-19 patients."
    protocol_vector = get_embedding(protocol_text)
    print(protocol_vector)

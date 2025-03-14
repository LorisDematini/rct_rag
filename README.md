# RCT RAG

Welcome to the **RCT RAG** project!

📖 **Read the full documentation here:**  
➡️ [RCT RAG Documentation](https://ohassanaly.github.io/rct_rag/)  

This project aims at offering a RAG architecture for Randomized Clinical Trials protocols made at URC Saint Louis.

A RAG architecture divides in several steps :

corpus text embedding  
embedding storage in a Vector Databse  
query embedding and retrieving most similar vectors in the DB

The scratch model is based on FAISS https://github.com/facebookresearch/faiss

![Alt text](assets/rag_illustration.png)

later improvements include preparing the RCT protocols text database ; scale the vector db storage ; LLM augmentation (using LangChain?) ; 
# What is this project?

This project offers multiple search engines to explore **Randomized Clinical Trial (RCT) protocols** created at **URC Saint Louis**.

![Project overview](assets/smart_image.jpg)

---
## Quick Start

You have two options to start using the RCT search engines:

### Use the Hosted Version

No setup is required. Simply visit the web application:
[RCT_Search_Engine](https://rct-rag.onrender.com/)

### Run Locally via Git and Docker

- **Clone the repository**:
```bash
git clone https://github.com/ohassanaly/rct_rag.git
cd rct_rag
```

- **Build and run the Docker container**:
```bash
docker build -t rct_search .
docker run -p 8080:8080 rct_search
```
- **Open your browser at http://localhost:8080 to access the application.**

---
## Demos

You have access to **three search engines**:

- **Sparse Engine** - [`demo`](demo/sparse_engine_demo.md)  
Retrieves the most relevant protocols for multi-word queries using TF-IDF.

- **Key-words Engine** - [`demo`](demo/exact_engine_demo.md)  
Finds protocols containing the exact keywords of your query, supporting wildcards (`*`) adn operators(AND/OR) for flexible matching.

- **Database** - [`demo`](demo/database_demo.md)  
Allows direct navigation and exploration of all protocols stored in the structured database.

---
## Project Structure

- [`builder`](rag/builder.md) – Handles data preparation and construction of each engines   
- [`search_engine`](rag/sparse_engine.md) – Contains the application logic and user interface  


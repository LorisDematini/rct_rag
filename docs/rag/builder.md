![Builder](assets/builder.png)

**Builder**: This module is responsible for data preparation and the construction of search engines. It contains:  

- `extract_pdf`: extraction of text from PDF files.  
- `acronyms`: management and extraction of acronyms found in the protocols. 
- `sections_regroup`: organization and regrouping of document sections.  
- `exact_engine` and `sparse_engine`: modules for building keyword-based and TF-IDF search engines.
- `top terms` : Top terms for each study use in display of results
- `config`: configuration files for data processing and building.  
- `data`: storage of source files and datasets.  
- `utils`: utility functions for preprocessing and data handling.

The script `main_builder.py` orchestrates the entire process of database and engines constructions.  

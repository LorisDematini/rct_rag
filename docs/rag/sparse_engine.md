**2. Search_engine**: This module manages the user interface and document search. It contains:  

- `app`: files related to invoking the selected search engine for consultation and querying.  
- `config`: configuration files for search engine parameters.  
- `core`: main search engine logic.  
- `display`: functions for formatting and displaying search results.  
- `utils`: utility functions for search operations and result handling.  

The script `main.py` runs the application and enables user interaction.  

![Sparse Search Engine](assets/sparse_search_engine.png)

Example: using the TF-IDF search engine  
- `display`: handles displaying the title and the query.  
- `load_sparse`: loads the different files built in the Builder module.  
- `query`: processes the user’s input query and sends it to the search engine.  
- `search_sparse`: the core search engine; performs the search and returns results.  
- `display`: another display function formats the results and uses `highlight` to emphasize query terms.  





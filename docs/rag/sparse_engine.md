## The TF-IDF search engine  

![Sparse Search Engine](assets/sparse_search_engine.png)

- `display`: handles displaying the title and the query.  
- `load_sparse`: loads the different files built in the Builder module.  
- `query`: processes the user’s input query and sends it to the search engine.  
- `search_sparse`: the core search engine; performs the search and returns results.  
- `display`: another display function formats the results and uses `highlight` to emphasize query terms.  
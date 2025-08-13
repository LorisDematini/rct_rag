#IMPORT
from acronyms import extract_acronyms_from_pdfs, extract_acronyms_from_json, merge_acronym_jsons, get_unique_acronyms
from extract_pdf import extract_study_tables_from_pdfs
from sections_regroup import categorize_study_sections
from config import PDF_FOLDER, SUMMARY_JSON_PATH, ACRONYMS_EXTRACT_PATH, ACRONYMS_STUDY_PATH, ACRONYMS_FILE, ACRONYMS_FILE_UNIQUE, SECTIONS_FULL_JSON_PATH, SECTIONS_JSON_PATH, SPARSE_JSON_PATH, SPARSE_PCKL_PATH, EXACT_JSON_PATH, EXACT_PCKL_PATH, AVAILABLE_SECTIONS_JSON_PATH
from config import categories_sparse, categories_exact
from sparse_engine import generator_save_documents, build_save_sparse_index
from exact_engine import generate_save_exact_documents, save_available_sections
from utils import top_terms_per_document


###EXTRACT
#Extract the tables of summary from the pdf
extract_study_tables_from_pdfs(PDF_FOLDER, SUMMARY_JSON_PATH)


###ACRONYMES
#Extract the tables of acronyms from the pdf 
extract_acronyms_from_pdfs(PDF_FOLDER, ACRONYMS_EXTRACT_PATH)

#Extract the acronyms from the json like (ex. Exemple Of Acronym (EOA))
extract_acronyms_from_json(SUMMARY_JSON_PATH, ACRONYMS_STUDY_PATH)

#Merge the 2 lists of acronyms by study gather before
merge_acronym_jsons(ACRONYMS_STUDY_PATH, ACRONYMS_EXTRACT_PATH, ACRONYMS_FILE)

#Find the uniques acronyms to do a list for every study
get_unique_acronyms(ACRONYMS_FILE, ACRONYMS_FILE_UNIQUE)


###SECTIONS
#Select sections wanted to full JSON (Key-Words)  
categorize_study_sections(SUMMARY_JSON_PATH, SECTIONS_FULL_JSON_PATH, categories_exact)

#Select sections wanted to sparse JSON (TFIDF)  
categorize_study_sections(SUMMARY_JSON_PATH, SECTIONS_JSON_PATH, categories_sparse)


###INDEX EXACT
#Generate the documents necessary to the exact search engine
documents_exact = generate_save_exact_documents(SECTIONS_FULL_JSON_PATH, EXACT_JSON_PATH, EXACT_PCKL_PATH)
#Save the list of available sections 
save_available_sections(documents_exact, AVAILABLE_SECTIONS_JSON_PATH)


###INDEX SPARSE
#Generate documents from Acronym and sparse JSON, with preprocessing
documents = generator_save_documents(SECTIONS_JSON_PATH, ACRONYMS_FILE, SPARSE_JSON_PATH, SPARSE_PCKL_PATH)

#Vectorize, create the sparse matrix and list of study ids from the documents
vectorizer, sparse_matrix, study_ids = build_save_sparse_index(documents)


#DISPLAY
#Find most important terms from the sparse matrix for each study
top_terms_per_document(vectorizer, sparse_matrix, study_ids)
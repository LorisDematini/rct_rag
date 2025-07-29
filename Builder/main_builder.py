#IMPORT
from Acronymes import extract_acronyms_from_pdfs, extract_acronyms_from_json, merge_acronym_jsons, get_consistent_unique_acronyms
from Extract import extract_study_tables_from_pdfs
from Sections import categorize_study_sections, categorize_study_sections_full
from Config import PDF_FOLDER, SUMMARY_JSON_PATH, ACRONYMS_EXTRACT_PATH, ACRONYMS_STUDY_PATH, ACRONYMS_FILE, ACRONYMS_FILE_UNIQUE, SECTIONS_FULL_JSON_PATH, SECTIONS_JSON_PATH

###EXTRACT
#ExtractPDF_JSON.py
extract_study_tables_from_pdfs(PDF_FOLDER, SUMMARY_JSON_PATH)


###ACRONYMES
#Abbreviation_extract.py : 
extract_acronyms_from_pdfs(PDF_FOLDER, ACRONYMS_EXTRACT_PATH)

#Acronyms_etudes.py :
extract_acronyms_from_json(SUMMARY_JSON_PATH, ACRONYMS_STUDY_PATH)

#fusion_json.py :
merge_acronym_jsons(ACRONYMS_STUDY_PATH, ACRONYMS_EXTRACT_PATH, ACRONYMS_FILE)

#Abbreviation_unique.py : 
get_consistent_unique_acronyms(ACRONYMS_FILE, ACRONYMS_FILE_UNIQUE)


###SECTIONS
#json_section_regroup_clean_complet.py
categorize_study_sections_full(SUMMARY_JSON_PATH, SECTIONS_FULL_JSON_PATH)


#json_section_regroup_clean.py
categorize_study_sections(SUMMARY_JSON_PATH, SECTIONS_JSON_PATH)

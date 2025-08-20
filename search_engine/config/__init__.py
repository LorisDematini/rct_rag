from typing import TYPE_CHECKING
from utils.lazy_import import make_lazy_import

if TYPE_CHECKING:
    from .paths import (
        PDF_FOLDER, SUMMARY_JSON_PATH, ACRONYMS_FILE, ACRONYMS_FILE_UNIQUE,
        SECTIONS_JSON_PATH, SPARSE_PCKL_PATH, VECTOR_PATH, MATRIX_PATH,
        STUDY_IDS_PATH, TOP_TERMS_PATH, EXACT_PCKL_PATH, AVAILABLE_SECTIONS_JSON_PATH,
        SECTIONS_FULL_JSON_PATH
    )
    from .display_strings import (
        title_main, title_data, download_label, title_exact, select_sec, type_query,
        show_section, title_sparse, validate, title_graph, x_label, y_label,
        no_protocol_query, no_pdf_avail, format_protocol, no_text_p, no_protocol_name,
        options_radio
    )

__getattr__ = make_lazy_import(__name__, {
    # paths
    "PDF_FOLDER": ".paths",
    "SUMMARY_JSON_PATH": ".paths",
    "ACRONYMS_FILE": ".paths",
    "ACRONYMS_FILE_UNIQUE": ".paths",
    "SECTIONS_JSON_PATH": ".paths",
    "SPARSE_PCKL_PATH": ".paths",
    "VECTOR_PATH": ".paths",
    "MATRIX_PATH": ".paths",
    "STUDY_IDS_PATH": ".paths",
    "TOP_TERMS_PATH": ".paths",
    "EXACT_PCKL_PATH": ".paths",
    "AVAILABLE_SECTIONS_JSON_PATH": ".paths",
    "SECTIONS_FULL_JSON_PATH": ".paths",
    # display_strings
    "title_main": ".display_strings",
    "title_data": ".display_strings",
    "download_label": ".display_strings",
    "title_exact": ".display_strings",
    "select_sec": ".display_strings",
    "type_query": ".display_strings",
    "show_section": ".display_strings",
    "title_sparse": ".display_strings",
    "validate": ".display_strings",
    "title_graph": ".display_strings",
    "x_label": ".display_strings",
    "y_label": ".display_strings",
    "no_protocol_query": ".display_strings",
    "no_pdf_avail": ".display_strings",
    "format_protocol": ".display_strings",
    "no_text_p": ".display_strings",
    "no_protocol_name": ".display_strings",
    "options_radio": ".display_strings",
})

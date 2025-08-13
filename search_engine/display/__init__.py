from typing import TYPE_CHECKING
from utils.lazy_import import make_lazy_import

if TYPE_CHECKING:
    from .display_sparse import display_sparse_results
    from .display_utils import (
        get_summary_data,
        extract_top_terms_by_study,
        clean_string,
        find_pdf_file,
        set_page,
        sidebar_radio,
        sidebar_title,
        text_input,
        title_print,
        radio_button_exact,
        get_summary_data_full,
    )
    from .highlight import highlight_text_sparse, highlight_text_exact
    from .display_db import display_list
    from .display_exact import display_exacte_results

__getattr__ = make_lazy_import(__name__, {
    # display_sparse
    "display_sparse_results": ".display_sparse",
    # display_utils
    "get_summary_data": ".display_utils",
    "extract_top_terms_by_study": ".display_utils",
    "clean_string": ".display_utils",
    "find_pdf_file": ".display_utils",
    "set_page": ".display_utils",
    "sidebar_radio": ".display_utils",
    "sidebar_title": ".display_utils",
    "text_input": ".display_utils",
    "title_print": ".display_utils",
    "radio_button_exact": ".display_utils",
    "get_summary_data_full": ".display_utils",
    # highlight
    "highlight_text_sparse": ".highlight",
    "highlight_text_exact": ".highlight",
    # display_db
    "display_list": ".display_db",
    # display_exact
    "display_exacte_results": ".display_exact",
})

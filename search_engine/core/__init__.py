from typing import TYPE_CHECKING
from utils.lazy_import import make_lazy_import

if TYPE_CHECKING:
    from .data_loader import load_sparse, load_exact, load_list
    from .sparse_search import search_sparse
    from .exact_search import search_ex, parse_query

__getattr__ = make_lazy_import(__name__, {
    "load_sparse": ".data_loader",
    "load_exact": ".data_loader",
    "load_list": ".data_loader",
    "search_sparse": ".sparse_search",
    "search_ex": ".exact_search",
    "parse_query": ".exact_search",
})
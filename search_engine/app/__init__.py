from typing import TYPE_CHECKING
from utils.lazy_import import make_lazy_import

if TYPE_CHECKING:
    from .sparse_app import run_sparse_app
    from .list_app import run_list_app
    from .exact_app import run_exact_app

__getattr__ = make_lazy_import(__name__, {
    "run_sparse_app": ".sparse_app",
    "run_list_app": ".list_app",
    "run_exact_app": ".exact_app",
})

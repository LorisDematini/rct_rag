import importlib

def make_lazy_import(module_name, mapping):
    """
    Create a __getattr__ function to lazily import attributes on first access.

    This is useful for delaying the import of heavy or rarely used modules 
    until their functions/classes are actually needed. It is typically used 
    inside a package's __init__.py to expose selected attributes without 
    importing the whole submodules at import time.

    Args:
        module_name (str):
            The fully-qualified name of the current module 
            (usually passed as __name__ in __init__.py).
        mapping (dict):
            A dictionary mapping attribute names (as exposed by the package) 
            to the relative or absolute module path where they are defined.
            Example:
                {
                    "func1": ".submodule1",
                    "ClassA": ".submodule2"
                }

    Returns:
        function:
            A __getattr__ function that can be assigned directly in the module 
            namespace (e.g., `__getattr__ = make_lazy_import(__name__, mapping)`).

    Raises:
        AttributeError:
            If the requested attribute name is not in the mapping.
    """
    def __getattr__(name):
        # Check if the requested attribute is in the lazy-load mapping
        if name in mapping:
            # Dynamically import the target module relative to the current one
            module = importlib.import_module(mapping[name], module_name)
            # Retrieve the requested attribute from the imported module
            return getattr(module, name)
        
        # If the attribute is not found in the mapping, raise an AttributeError
        raise AttributeError(f"module {module_name} has no attribute {name}")

    return __getattr__

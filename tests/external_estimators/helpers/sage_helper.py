import inspect
import os
import sys
import types
import importlib
from typing import List, Optional, Union, Dict, Any

import sage.all


def sage_import(
    module_path: str,
    import_list: Optional[List[str]] = None,
    add_to_namespace: bool = False,
) -> Union[None, types.ModuleType, Dict[str, Any]]:
    """
    Import specified functions or variables from a .sage module or return the full module.

    This function imports the specified functions or variables from a .sage module
    into the global namespace of the caller, or returns the full module or specified objects.

    Args:
        module_path: The path to the .sage module, using dot notation relative to the package
                     containing this function.
        import_list: An optional list of function or variable names to import from the module.
        add_to_namespace: If True, adds imported objects to the caller's namespace. If False,
                          returns the objects without modifying the namespace.

    Returns:
        - None if import_list is provided and add_to_namespace is True,
        - The full created module if import_list is None and add_to_namespace is True,
        - A dictionary of imported objects if import_list is provided and add_to_namespace is False,
        - The full created module if import_list is None and add_to_namespace is False.

    Raises:
        ImportError: If any name in import_list is not found in the module.

    Note:
        This function modifies the global namespace of the caller if add_to_namespace is True.
    """
    module_name, absolute_filepath = _get_module_info(module_path)
    module = _create_sage_module(module_name, absolute_filepath)

    if import_list:
        if add_to_namespace:
            _import_to_namespace(module, import_list)
            return None
        else:
            return {
                name: getattr(module, name)
                for name in import_list
                if hasattr(module, name)
            }
    else:
        if add_to_namespace:
            _import_module_to_namespace(module)
            return None
        else:
            return module


def _import_to_namespace(module: types.ModuleType, import_list: List[str]) -> None:
    """
    Import specified names from the module to the caller's global namespace.

    Args:
        module: The module from which to import.
        import_list: A list of names to import from the module.

    Raises:
        ImportError: If any name in import_list is not found in the module.
    """
    caller_globals = inspect.currentframe().f_back.f_back.f_globals

    for name in import_list:
        if not hasattr(module, name):
            raise ImportError(f"Cannot import {name} from {module.__name__}.")
        caller_globals[name] = getattr(module, name)


def _import_module_to_namespace(module: types.ModuleType) -> None:
    """
    Import all non-private attributes from the module to the caller's global namespace.

    Args:
        module: The module from which to import.
    """
    caller_globals = inspect.currentframe().f_back.f_back.f_globals

    for name, value in module.__dict__.items():
        if not name.startswith("_"):
            caller_globals[name] = value


def _get_module_info(module_path: str) -> tuple[str, str]:
    """
    Extract module name and absolute file path from the given module path.

    Args:
        module_path: The full path to the .sage module, using dot notation including the root package.

    Returns:
        A tuple containing the module name and its absolute file path.
    """
    path_parts = module_path.split(".")
    root_package_name = path_parts[0]

    try:
        root_package = importlib.import_module(root_package_name)
    except ImportError:
        raise ImportError(f"Could not import root package {root_package_name}")

    if hasattr(root_package, "__file__"):
        root_package_file = root_package.__file__
    elif root_package_name in sys.modules:
        root_package_file = sys.modules[root_package_name].__file__
    else:
        raise ValueError(
            f"Could not determine file location for package {root_package_name}"
        )

    root_package_dir = os.path.dirname(root_package_file)

    module_name = path_parts[-1]
    path_parts[-1] += ".sage"
    absolute_filepath = os.path.join(root_package_dir, *path_parts[1:])

    return module_name, absolute_filepath


def _create_sage_module(module_name: str, filepath: str) -> types.ModuleType:
    """
    Create a new module with Sage globals and execute the .sage file contents.

    Args:
        module_name: The name of the module to create.
        filepath: The absolute path to the .sage file.

    Returns:
        A new module containing the executed .sage file contents.
    """
    with open(filepath) as sage_file:
        code = sage.all.preparse(sage_file.read())

        module = types.ModuleType(module_name)
        module.__file__ = filepath

        for key, value in sage.all.__dict__.items():
            if not key.startswith("_"):
                setattr(module, key, value)

        exec(code, module.__dict__)
        return module

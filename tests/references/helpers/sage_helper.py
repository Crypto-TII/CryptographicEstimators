import inspect
import os
import types
from typing import List, Optional

import sage.all

from tests.references.helpers.constants import DOCKER_LIBRARY_PATH


def import_sage_module(
    module_path: str, import_list: Optional[List[str]] = None
) -> None:
    """
    Import specified functions or variables from a .sage module.

    This function imports the specified functions or variables from a .sage module
    into the global namespace of the caller.

    Args:
        module_path: The path to the .sage module, using dot notation.
        import_list: A list of function or variable names to import from the module.

    Raises:
        ValueError: If import_list is None or empty.
        ImportError: If any name in import_list is not found in the module.

    Note:
        This function modifies the global namespace of the caller.
    """
    if not import_list:
        raise ValueError(
            "You must specify functions/variables to import in the 'import_list' parameter."
        )

    module_name, absolute_filepath = _get_module_info(module_path)
    module = _create_sage_module(module_name, absolute_filepath)
    _import_to_namespace(module, import_list)


def _get_module_info(module_path: str) -> tuple[str, str]:
    """
    Extract module name and absolute file path from the given module path.

    Args:
        module_path: The path to the .sage module, using dot notation.

    Returns:
        A tuple containing the module name and its absolute file path.
    """
    path_parts = module_path.split(".")
    module_name = path_parts[-1]
    path_parts[-1] += ".sage"
    absolute_filepath = os.path.join(*DOCKER_LIBRARY_PATH, *path_parts)
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

    for name in import_list:
        caller_globals[name] = getattr(module, name)

import yaml
import os
import inspect
import itertools
from pathlib import Path
from importlib import import_module
from functools import reduce
from typing import List, Tuple, Dict, Any, Callable
from types import ModuleType
from tests.external_estimators.helpers.sage_helper import sage_import


def collect_ext_modules() -> List[ModuleType]:
    """
    Collects external modules from the current directory.

    Returns:
        List[ModuleType]: A list of imported modules.

    This function performs the following steps:
    1. Determines the root package and directory.
    2. Lists files in the current directory.
    3. Filters for files starting with "ext_".
    4. Attempts to import .py files and sage_import .sage files.
    5. Returns a list of successfully imported modules.
    """

    current_module = inspect.getmodule(collect_ext_modules)
    root_package_name = current_module.__name__.split(".")[0]
    root_package = import_module(root_package_name)
    root_package_dir = os.path.dirname(inspect.getfile(root_package))
    current_dir = os.path.dirname(os.path.abspath(__file__))
    files = os.listdir(current_dir)

    ext_files = [f for f in files if f.startswith("ext_")]

    modules = []

    for file in ext_files:
        _, ext = os.path.splitext(file)

        rel_path = os.path.relpath(os.path.join(current_dir, file), root_package_dir)
        module_path = ".".join(rel_path.split(os.sep)).rsplit(".", 1)[0]

        if ext == ".py":
            try:
                module = import_module(f"{module_path}")
                modules.append(module)
            except ImportError as e:
                print(f"Error importing {module_path}: {e}")

        elif ext == ".sage":
            try:
                module = sage_import(f"{root_package_name}.{module_path}")
                modules.append(module)
            except Exception as e:
                print(f"Error importing {module_path} with sage_import: {e}")

    return modules


def collect_ext_functions(module: ModuleType) -> List[Tuple[str, str, Callable]]:
    """
    Collects external functions from a given module.

    Args:
        module (ModuleType): The module to collect functions from.

    Returns:
        List[Tuple[str, str, Callable]]: A list of tuples containing
        (module_name, function_name, function_object) for each external function in the module.
    """
    module_name = module.__name__
    return [
        (module_name, name, obj)
        for name, obj in inspect.getmembers(module)
        if inspect.isfunction(obj) and name.startswith("ext_")
    ]


def dictionary_from_tuple(function_path: Tuple[str, str, Callable]) -> Dict[str, Any]:
    """
    Creates a dictionary representation of a function and its inputs/outputs.

    Args:
        function_path (Tuple[str, str, Callable]): A tuple containing
        (module_name, function_name, function_object).

    Returns:
        Dict[str, Any]: A nested dictionary representing the function's module, name, and inputs/outputs.
    """
    module_name, function_name, function = function_path
    unprefixed_module_name = module_name[4:]
    unprefixed_function_name = function_name[4:]
    inputs_with_expected_outputs = function()
    return {
        unprefixed_module_name: {
            unprefixed_function_name: {
                "inputs_with_expected_outputs": inputs_with_expected_outputs
            }
        }
    }


def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merges two dictionaries.

    Args:
        dict1 (Dict[str, Any]): The first dictionary.
        dict2 (Dict[str, Any]): The second dictionary.

    Returns:
        Dict[str, Any]: A new dictionary containing the merged contents of dict1 and dict2.
    """
    return {
        key: (
            deep_merge(dict1[key], dict2[key])
            if isinstance(dict1.get(key), dict) and isinstance(dict2.get(key), dict)
            else dict2[key] if key in dict2 else dict1[key]
        )
        for key in set(dict1) | set(dict2)
    }


def main():
    """
    Main function to process reference inputs, execute generators, and save results.

    This function performs the following steps:
    1. Collects external modules and their functions.
    2. Creates a dictionary of external functions and their inputs/outputs.
    3. Serializes the dictionary to YAML format.
    4. Validates the serialization by deserializing and comparing.
    5. Saves the serialized data to a YAML file.
    """

    external_kat_generators = list(
        itertools.chain.from_iterable(map(collect_ext_functions, collect_ext_modules()))
    )
    kat_dictionary = reduce(
        deep_merge, list(map(dictionary_from_tuple, external_kat_generators))
    )

    # We only save the serialized reference data if deserialization
    # perfectly reconstructs the original data.
    serialized_kat = yaml.dump(kat_dictionary, default_flow_style=None)
    loaded_data = yaml.unsafe_load(serialized_kat)
    assert kat_dictionary == loaded_data, "YAML dump and load did not preserve data"

    # We save the serialization in the parent directory
    output_file = Path(__file__).parent.parent / "kat.yaml"
    with output_file.open("w") as yaml_file:
        yaml.dump(kat_dictionary, yaml_file, default_flow_style=None)


if __name__ == "__main__":
    main()

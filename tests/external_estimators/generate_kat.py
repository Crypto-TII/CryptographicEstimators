import yaml
import operator
import os
import inspect
from importlib import import_module
from functools import reduce
from itertools import starmap
from typing import cast
from tests.external_estimators.helpers.sage_helper import sage_import
from tests.external_estimators.helpers.constants import (
    DOCKER_LIBRARY_PATH,
    LIBRARY_EXTERNAL_ESTIMATORS_PATH,
)
from tests.helper import DOCKER_YAML_REFERENCE_PATH


def collect_ext_modules():

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
                module = import_module(f"{root_package_name}.{module_path}")
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


def collect_ext_functions(module):
    module_name = module.__name__
    return [
        (module_name, name, obj)
        for name, obj in inspect.getmembers(module)
        if inspect.isfunction(obj) and name.startswith("ext_")
    ]


def dictionary_from_tuple(function_path):
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


def deep_merge(dict1, dict2):
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
    1. Extracts external estimators paths and inputs from EXT_INPUTS.
    2. Executes external functions with their respective inputs.
    3. Updates the reference data with the external functions outputs.
    4. Processes the reference data (renaming).
    5. Serializes and validates the processed data.
    6. Saves the processed data to a YAML file.
    """

    external_kat_generators = list(*map(collect_ext_functions, collect_ext_modules()))
    kat_dictionary = reduce(
        deep_merge, list(map(dictionary_from_tuple, external_kat_generators))
    )

    # We only save the serialized reference data if deserialization
    # perfectly reconstructs the original data.
    serialized_kat = yaml.dump(kat_dictionary, default_flow_style=None)
    loaded_data = yaml.unsafe_load(serialized_kat)
    assert kat_dictionary == loaded_data, "YAML dump and load did not preserve data"

    with open(DOCKER_YAML_REFERENCE_PATH, "w") as yaml_file:
        yaml.dump(kat_dictionary, yaml_file, default_flow_style=None)


if __name__ == "__main__":
    main()

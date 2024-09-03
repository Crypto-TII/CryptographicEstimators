import yaml
import operator
import os
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
from tests.external_estimators.ext_inputs import EXT_INPUTS


def extract_generator_paths_and_inputs(input_dict: dict, path: tuple = ()) -> iter:
    """
    Recursively extracts generator paths and their corresponding inputs from the input dictionary.

    This function traverses the input dictionary and yields tuples containing the generator path
    and its inputs for each leaf node containing an "inputs" key.

    Args:
        input_dict: The input dictionary to traverse.
        path: The current path in the dictionary (used for recursion).

    Yields:
        Tuples containing the generator path and its inputs.
    """
    for key, value in input_dict.items():
        current_path = path + (key,)

        if isinstance(value, dict):
            if "inputs" in value:
                yield current_path, value["inputs"]
            else:
                yield from extract_generator_paths_and_inputs(value, current_path)


def import_and_execute_generator(gen_path: tuple, inputs: list) -> tuple:
    """
    Imports a generator function and executes it with the given inputs.

    This function determines the file extension of the generator, imports it accordingly,
    and then executes the generator function with the provided inputs.

    Args:
        gen_path: A tuple representing the path to the generator function.
        inputs: A list of inputs to be passed to the generator function.

    Returns:
        A tuple containing the generator path and the output of the generator function.

    Raises:
        ValueError: If the file extension is not supported.
    """

    def find_generator_file_extension(gen_path: tuple) -> str:
        file_path = os.path.join(
            *DOCKER_LIBRARY_PATH, *LIBRARY_EXTERNAL_ESTIMATORS_PATH, *gen_path[:-1]
        )
        for ext in (".sage", ".py"):
            if os.path.isfile(file_path + ext):
                return ext
        raise ValueError(f"No supported file extension found for {file_path}")

    import_modpath = ".".join(LIBRARY_EXTERNAL_ESTIMATORS_PATH + gen_path[:-1])
    gen_function_name = gen_path[-1]
    gen_file_ext = find_generator_file_extension(gen_path)

    if gen_file_ext == ".py":
        estimator_module = import_module(import_modpath)
        gen_function = getattr(estimator_module, gen_function_name)
    else:
        sage_import(import_modpath, import_list=[gen_function_name])
        gen_function = globals()[gen_function_name]

    output = gen_function(inputs)
    return gen_path, output


def get_generator_info(dictionary: dict, gen_path: tuple) -> dict:
    """
    Retrieves the generator information from the dictionary using the given path.

    Args:
        dictionary: The dictionary containing generator information.
        gen_path: A tuple representing the path to the generator in the dictionary.

    Returns:
        A dictionary containing the generator information.
    """
    return reduce(operator.getitem, gen_path, dictionary)


def ext_prefix_to_int_prefix(data: dict) -> dict:
    """
    Recursively traverses a dictionary and replaces "ext_" with "int_" in string keys and values.

    Args:
        data: The dictionary to be traversed and modified.

    Returns:
        The modified dictionary with "ext_" replaced by "int_".
    """

    def replace_ext_with_int(element: str) -> str:
        return "int_" + element[4:] if element.startswith("ext_") else element

    if isinstance(data, dict):
        return {
            replace_ext_with_int(key): (
                ext_prefix_to_int_prefix(value)
                if isinstance(value, dict)
                else replace_ext_with_int(value) if isinstance(value, str) else value
            )
            for key, value in data.items()
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

    ext_kat_gen_modules = collect_ext_modules()

    ext_kat_gen_path_with_kat = map(collect_and_run_kat_generators, ext_kat_gen_modules)

    # Map to convert from kat_gen_path with kat, to nested dict.
    #
    # Reduce function using the | dict merge operator to create the new dictionary.
    for kat_gen_path, kat in kat_gen_path_with_kat:
        gen_info = cast(dict, get_generator_info(reference_data, gen_path))
        del gen_info["inputs"]
        gen_info["inputs_with_expected_outputs"] = outputs

    reference_data = ext_prefix_to_int_prefix(reference_data)

    # We only save the serialized reference data if deserialization
    # perfectly reconstructs the original data.
    serialized_data = yaml.dump(reference_data, default_flow_style=None)
    loaded_data = yaml.unsafe_load(serialized_data)
    assert reference_data == loaded_data, "YAML dump and load did not preserve data"

    with open(DOCKER_YAML_REFERENCE_PATH, "w") as yaml_file:
        yaml.dump(reference_data, yaml_file, default_flow_style=None)


if __name__ == "__main__":
    main()

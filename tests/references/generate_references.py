import yaml
import operator
import os
from importlib import import_module
from functools import reduce
from itertools import starmap, chain
from typing import cast
from tests.references.helpers.sage_helper import import_sage_module
from tests.references.helpers.constants import (
    DOCKER_LIBRARY_PATH,
    LIBRARY_REFERENCES_PATH,
)
from tests.helper import DOCKER_YAML_REFERENCE_PATH

REFERENCES_INPUTS = {
    "SDFqEstimator": {
        "gen_sdfq": {
            "gen_sdfq_lee_brickell": {
                "inputs": [(256, 128, 64, 251), (961, 771, 48, 31)]
            },
            "gen_sdfq_stern": {"inputs": [(256, 128, 64, 251), (961, 771, 48, 31)]},
            "gen_sdfq_stern_range": {
                "inputs": [
                    (
                        range(50, 70, 5),
                        range(20, 40, 2),
                        [7, 11, 17, 53, 103, 151, 199, 251],
                    ),
                ]
            },
        },
    },
}


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
            *DOCKER_LIBRARY_PATH, *LIBRARY_REFERENCES_PATH, *gen_path[:-1]
        )
        for ext in (".sage", ".py"):
            if os.path.isfile(file_path + ext):
                return ext
        raise ValueError(f"No supported file extension found for {file_path}")

    import_modpath = ".".join(LIBRARY_REFERENCES_PATH + gen_path[:-1])
    gen_function_name = gen_path[-1]
    gen_file_ext = find_generator_file_extension(gen_path)

    if gen_file_ext == ".py":
        estimator_module = import_module(import_modpath)
        gen_function = getattr(estimator_module, gen_function_name)
    else:
        import_sage_module(import_modpath, import_list=[gen_function_name])
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


def flatten_nested_dict(nested_dict: dict) -> dict:
    """
    Flattens a nested dictionary by removing the first level of nesting.

    Args:
        nested_dict: A dictionary where the values are also dictionaries.

    Returns:
        A flattened dictionary containing all key-value pairs from the input dictionary.
    """
    return dict(
        chain.from_iterable(outer_val.items() for outer_val in nested_dict.values())
    )


def rename_gen_to_test(data: dict) -> dict:
    """
    Recursively traverses a dictionary and replaces "gen_" with "test_" in string keys and values.

    Args:
        data: The dictionary to be traversed and modified.

    Returns:
        The modified dictionary with "gen_" replaced by "test_".
    """

    def replace_gen_with_test(element: str) -> str:
        return "test_" + element[4:] if element.startswith("gen_") else element

    if isinstance(data, dict):
        return {
            replace_gen_with_test(key): (
                rename_gen_to_test(value)
                if isinstance(value, dict)
                else replace_gen_with_test(value) if isinstance(value, str) else value
            )
            for key, value in data.items()
        }


def main():
    """
    Main function to process reference inputs, execute generators, and save results.

    This function performs the following steps:
    1. Extracts generator paths and inputs from REFERENCES_INPUTS.
    2. Executes generators with their respective inputs.
    3. Updates the reference data with the generator outputs.
    4. Processes the reference data (flattening and renaming).
    5. Serializes and validates the processed data.
    6. Saves the processed data to a YAML file.
    """
    reference_data = REFERENCES_INPUTS.copy()

    gen_paths_and_inputs = extract_generator_paths_and_inputs(REFERENCES_INPUTS)
    gen_paths_and_inputs_with_outputs = starmap(
        import_and_execute_generator, gen_paths_and_inputs
    )

    for gen_path, outputs in gen_paths_and_inputs_with_outputs:
        gen_info = cast(dict, get_generator_info(reference_data, gen_path))
        del gen_info["inputs"]
        gen_info["inputs_with_expected_outputs"] = outputs

    reference_data = flatten_nested_dict(reference_data)
    reference_data = rename_gen_to_test(reference_data)

    # We only save the serialized reference data if deserialization
    # perfectly reconstructs the original data.
    serialized_data = yaml.dump(reference_data, default_flow_style=None)
    loaded_data = yaml.unsafe_load(serialized_data)
    assert reference_data == loaded_data, "YAML dump and load did not preserve data"

    with open(DOCKER_YAML_REFERENCE_PATH, "w") as yaml_file:
        yaml.dump(reference_data, yaml_file, default_flow_style=None)


if __name__ == "__main__":
    main()

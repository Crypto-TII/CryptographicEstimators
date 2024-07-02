import yaml
import operator
import os
from importlib import import_module
from functools import reduce
from itertools import starmap, chain
from typing import cast
from tests.references.helpers.sage_helper import sage_import
from tests.references.helpers.constants import (
    DOCKER_LIBRARY_PATH,
    LIBRARY_REFERENCES_PATH,
)
from tests.helper import (
    DOCKER_YAML_REFERENCE_PATH,
)


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


## Glosary note:
## - gen -> generator
## - path -> tuples that contains the components of a path as strings. Ex.
##      gen_path = ("directory", "subdirectory", "filename/module", "gen_function_name")


def extract_gen_paths_with_inputs(dictionary, path=()):
    """
    Given the references inputs dictionary, this function yields a generator path with the generator inputs to be evaluated in, for each path in the dictionary
    """
    for key, value in dictionary.items():
        path_tuple = path + (key,)

        if isinstance(value, dict) and "inputs" in value:
            yield path_tuple, value["inputs"]
        elif isinstance(value, dict):
            yield from extract_gen_paths_with_inputs(value, path_tuple)


def import_and_exec_on_inputs(gen_path, inputs):
    """
    Imports a generator function given a path to that generator, and applies the given inputs on it.
    Raises ValueError if the file extension is not supported.
    """

    def find_gen_file_extension(gen_path):
        """
        Given a generator path, this function determines what extension the generator file have.
        """

        file_path = os.path.join(
            *DOCKER_LIBRARY_PATH, *LIBRARY_REFERENCES_PATH, *gen_path
        )
        supported_extensions = (".sage", ".py")
        for ext in supported_extensions:
            if os.path.isfile(file_path + ext):
                return ext
        else:
            return None

    import_modpath = ".".join(LIBRARY_REFERENCES_PATH + gen_path[:-1])
    gen_function_name = gen_path[-1]
    gen_file_ext = find_gen_file_extension(gen_path[:-1])

    if gen_file_ext == ".py":
        estimator_module = import_module(import_modpath)
        gen_function = getattr(estimator_module, gen_function_name)

    elif gen_file_ext == ".sage":
        sage_import(import_modpath, fromlist=[gen_function_name])
        gen_function = globals()[gen_function_name]

    else:
        raise ValueError(f"Unsupported file extension: {gen_file_ext}")

    output = gen_function(inputs)
    return gen_path, output


def extract_gen_info(dictionary, gen_path):
    """
    Given a generator path, this function traverses throught the dictionary to extract the dictionary with info about that generator (that is, the last dictionary, who contains the input/output description)
    """
    return reduce(operator.getitem, gen_path, dictionary)


def remove_first_nesting_level(dictionary):
    """
    Removes the first nesting level of a dictionary of dictionaries.

    Args:
        nested_dict (dict): A dictionary where the values are also dictionaries.

    Returns:
        dict: A single dictionary containing all the key-value pairs from the input dictionary,
        with the first nesting level removed.
    """
    return dict(
        chain.from_iterable(outer_val.items() for outer_val in dictionary.values())
    )


def rename_gen_to_test(data):
    """
    Recursively traverses a dictionary and modifies string keys and values starting with "gen_" to "test_".

    Args:
        data (dict): The dictionary to be traversed and modified.

    Returns:
        dict: The modified dictionary.
    """

    def check_gen_to_test(element):
        return (
            "test_" + element[4:]
            if isinstance(element, str) and element.startswith("gen_")
            else element
        )

    if isinstance(data, dict):
        return {
            check_gen_to_test(key): (
                rename_gen_to_test(value)
                if isinstance(value, dict)
                else check_gen_to_test(value)
            )
            for key, value in data.items()
        }
    else:
        return data


if __name__ == "__main__":

    reference_data = REFERENCES_INPUTS.copy()

    gens_path_with_inputs = extract_gen_paths_with_inputs(REFERENCES_INPUTS)
    gens_path_with_outputs = starmap(import_and_exec_on_inputs, gens_path_with_inputs)

    for gen_path, outputs in gens_path_with_outputs:
        gen_info = cast(dict, extract_gen_info(reference_data, gen_path))
        gen_info["expected_outputs"] = outputs

    # We remove the directory name of the dictionary, as we dont need them later to execute the tests
    reference_data = remove_first_nesting_level(reference_data)
    reference_data = rename_gen_to_test(reference_data)

    # We only write the reference data into a file if its serialization
    # is idempotent, i.e., f^-1(f(x))=x
    serialized_data = yaml.dump(reference_data, default_flow_style=None)
    loaded_data = yaml.unsafe_load(serialized_data)
    assert reference_data == loaded_data, "YAML dump and load did not preserve data"

    with open(DOCKER_YAML_REFERENCE_PATH, "w") as yaml_file:
        yaml.dump(reference_data, yaml_file, default_flow_style=None)

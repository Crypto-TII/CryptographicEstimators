# This file produces a YAML file containing precomputed reference values for the tests
# declared at `tests/validations/`, based on sage and non-sage based tests that can take
# a long time to execute.

from importlib import import_module
from tests.references.helpers.sage_helper import sage_import
from tests.references.helpers.constants import (
    ABSOLUTE_DOCKER_SYSTEM_PREFIX,
    ABSOLUTE_MODPATH_PREFIX,
    ABSOLUTE_YAML_PATH,
    ABSOLUTE_JSON_PATH,
)
from functools import reduce
from itertools import starmap
import yaml
import json
import operator
import os

REFERENCES_INPUTS = {
    "SDFqEstimator": {
        "gen_sdfq": {
            "gen_sdfq_lee_brickell": {
                "input": ([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01)
            },
            "gen_sdfq_stern": {
                "input": ([(256, 128, 64, 251), (961, 771, 48, 31)], 0.01)
            },
            "gen_sdfq_stern_range": {
                "input": (
                    range(50, 70, 5),
                    range(20, 40, 2),
                    [7, 11, 17, 53, 103, 151, 199, 251],
                    0.05,
                )
            },
        },
    },
}


def extract_gen_paths_with_attribute(dictionary, attribute, path=()):
    for key, value in dictionary.items():
        path_tuple = path + (key,)

        if isinstance(value, dict) and attribute in value:
            yield path_tuple, value[attribute]
        elif isinstance(value, dict):
            yield from extract_gen_paths_with_attribute(value, attribute, path_tuple)


def find_gen_file_extension(path_tuple):

    file_path = os.path.join(
        *ABSOLUTE_DOCKER_SYSTEM_PREFIX, *ABSOLUTE_MODPATH_PREFIX, *path_tuple
    )
    supported_extensions = (".sage", ".py")
    for ext in supported_extensions:
        if os.path.isfile(file_path + ext):
            return ext
    else:
        return None


def import_function_by_path(path_tuple):
    """
    Imports a function given a path tuple and its file extension.
    Raises ValueError if the file extension is not supported.
    """
    import_modpath = ".".join(ABSOLUTE_MODPATH_PREFIX + list(path_tuple[:-1]))
    gen_function_name = path_tuple[-1]
    gen_file_ext = find_gen_file_extension(path_tuple[:-1])

    if gen_file_ext == ".py":
        estimator_module = import_module(import_modpath)
        gen_function = getattr(estimator_module, gen_function_name)

    elif gen_file_ext == ".sage":
        sage_import(import_modpath, fromlist=[gen_function_name])
        gen_function = globals()[gen_function_name]

    else:
        raise ValueError(
            f"Unsupported file extension: {gen_file_ext}"
        )  # Raise ValueError

    return gen_function


def import_and_exec_on_inputs(path_tuple, inputs):
    gen_function = import_function_by_path(path_tuple)
    output = gen_function(*inputs)
    return path_tuple, output


def get_dict_from_path_tuple(dictionary, keys):
    """Gets a nested value using functools.reduce."""
    return reduce(operator.getitem, keys, dictionary)


if __name__ == "__main__":

    reference_dict = REFERENCES_INPUTS.copy()

    path_tuples_with_input = extract_gen_paths_with_attribute(
        REFERENCES_INPUTS, "input"
    )
    paths_tuples_with_output = starmap(
        import_and_exec_on_inputs, path_tuples_with_input
    )

    for path_tuple, output in paths_tuples_with_output:
        values = get_dict_from_path_tuple(reference_dict, path_tuple)
        values["output"] = (output,)

    # Mini test to ensure consistency
    yaml_string = yaml.dump(reference_dict, default_flow_style=False)
    loaded_dict = yaml.load(
        yaml_string, Loader=yaml.FullLoader
    )  # Use FullLoader for security
    assert reference_dict == loaded_dict, "YAML dump and load did not preserve data"

    with open(ABSOLUTE_YAML_PATH, "w") as yaml_file:
        yaml.dump(reference_dict, yaml_file, default_flow_style=False)

    with open(ABSOLUTE_JSON_PATH, "w") as file:
        json.dump(REFERENCES_INPUTS, file, indent=2, sort_keys=False)

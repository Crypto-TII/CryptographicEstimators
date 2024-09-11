import inspect
import importlib


def extract_sc_path_with_info(input_dict: dict, path: tuple = ()) -> iter:
    """
    Recursively extracts test paths and their corresponding inputs/outputs tuples from the input dictionary.

    This function traverses the input dictionary and yields tuples containing the test path
    and its inputs/outputs tuples for each leaf node containing an "inputs_with_expected_outputs" key.

    Args:
        input_dict: The input dictionary to traverse.
        path: The current path in the dictionary (used for recursion).

    Yields:
        Tuples containing the test path and its inputs/outputs tuples.
    """
    for key, value in input_dict.items():
        current_path = path + (key,)

        if isinstance(value, dict):
            if "inputs_with_expected_outputs" in value:
                yield current_path, value["inputs_with_expected_outputs"]
            else:
                yield from extract_sc_path_with_info(value, current_path)


def import_sc_from_path(single_case_path: tuple):
    """
    Imports a single case function from a specified path.

    Args:
        single_case_path (tuple): A tuple representing the path to the single case function, relative
            to the caller's location. The last element of the tuple is the function name, and
            the preceding elements (if any) represent the module path.

    Returns:
        function: The imported function.

    Example:
        function = import_single_case_from_path(('sdfq', 'lee-brickell'))
    """

    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)

    package_parts = caller_module.__name__.split(".")
    caller_path = ".".join(package_parts[:-1] + ["internal_estimators"])

    single_case_module_path = ".".join(single_case_path[:-1])
    function_name = single_case_path[-1]

    import_modpath = f"{caller_path}.{single_case_module_path}"
    module = importlib.import_module(import_modpath)
    function = getattr(module, function_name)

    return function


def kat_test(expected_output, actual_output, epsilon):
    assert abs(expected_output - actual_output) < epsilon


def test_all_estimators(yaml_references: dict):
    """ """

    # for filename in yaml_references:
    #     for internal_reference_name in yaml_references[filename]:
    #         inputs_with_expected_outputs = yaml_references[filename][
    #             internal_reference_name
    #         ]["inputs_with_expected_outputs"]
    #         for input, expected_output in inputs_with_expected_outputs:
    #             internal_reference_function = import_sc_from_path(
    #                 (filename, internal_reference_name)
    #             )
    #             actual_output, epsilon = internal_reference_function(input)
    #             kat_test(expected_output, actual_output, epsilon)

    sc_path_and_inputs_with_outputs = extract_sc_path_with_info(yaml_references)

    for sc_path, inputs_with_outputs in sc_path_and_inputs_with_outputs:
        inputs, expected_outputs = zip(*inputs_with_outputs)
        single_case_function = import_sc_from_path(sc_path)
        actual_outputs, epsilon = zip(*map(single_case_function, inputs))
        assert map(kat_test, list(zip(expected_outputs, actual_outputs, epsilon)))

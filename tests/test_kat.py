import inspect
import importlib
from itertools import starmap
from typing import Tuple, Callable, Dict, Iterable, Any, List


def extract_paths(
    nested_dict: Dict[str, Any], path: Tuple[str, ...] = ()
) -> Iterable[Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]]:
    """Recursively extracts internal estimators paths and their corresponding inputs/outputs tuples from the input dictionary.

    This function traverses the input dictionary and yields tuples containing the internal estimator path
    and its inputs/outputs tuples for each leaf node containing an "inputs_with_expected_outputs" key.

    Args:
        nested_dict (Dict[str, Any]): The input dictionary to traverse.
        path (Tuple[str, ...]): The current path in the dictionary (used for recursion).

    Yields:
        Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]: Tuples containing the internal estimators and its inputs/outputs tuples.
    """
    for key, value in nested_dict.items():
        current_path = path + (key,)

        if isinstance(value, dict):
            if "inputs_with_expected_outputs" in value:
                yield current_path, value["inputs_with_expected_outputs"]
            else:
                yield from extract_paths(value, current_path)


def import_internal_estimator(internal_estimator_path: Tuple[str, ...]) -> Callable:
    """Imports an internal estimator function from a specified path.

    Args:
        internal_estimator_path (Tuple[str, ...]): A tuple representing the path to the internal estimator function, relative
            to the caller's location. The last element of the tuple is the function name, and
            the preceding elements (if any) represent the module path.

    Returns:
        Callable: The imported function.

    Example:
        function = import_internal_estimator(('sdfq', 'lee-brickell'))
    """

    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)

    package_parts = caller_module.__name__.split(".")
    caller_path = ".".join(package_parts[:-1] + ["internal_estimators"])

    single_case_module_path = ".".join(internal_estimator_path[:-1])
    function_name = internal_estimator_path[-1]

    import_modpath = f"{caller_path}.{single_case_module_path}"
    module = importlib.import_module(import_modpath)
    function = getattr(module, function_name)

    return function


def kat_test(
    internal_estimator_name: str,
    input: Any,
    expected_output: Any,
    actual_output: Any,
    epsilon: float,
):
    """Asserts that the absolute difference between the expected and actual outputs is less than the specified epsilon.

    The expected output comes from the KAT values produced from external estimators, and the actual ones are produced by our internals estimators.

    Args:
        internal_estimator_name (str): The name of the internal estimator.
        input (Any): The input tuple used for the test.
        expected_output (Any): The expected output value.
        actual_output (Any): The actual output value.
        epsilon (float): The maximum allowable difference between the expected and actual outputs.
    """
    if not abs(expected_output - actual_output) <= epsilon:
        print("FAILED TEST!!!")
        print(f"Input: {input}, estimator: {internal_estimator_name}")
        print(
            f"Expected: {expected_output}, actual: {actual_output}, tolerance: {epsilon} "
        )
        return False
    else:
        return True


def test_all_estimators(kat: dict):
    """Runs a KAT test for all internal estimators specified in the YAML references.

    This function extracts the internal estimator paths and their corresponding inputs/outputs from the
    YAML references, imports the relevant internal estimator functions, and runs a standard KAT test
    to verify the outputs against the expected values produced by external estimators.

    Args:
        yaml_references (Dict[str, Any]): A dictionary containing the KAT references.
    """

    int_estimator_paths_with_values = extract_paths(kat)
    execution_list = []

    for internal_estimator_path, inputs_with_outputs in int_estimator_paths_with_values:
        inputs, expected_outputs = zip(*inputs_with_outputs)
        internal_estimator_function = import_internal_estimator(internal_estimator_path)
        actual_outputs, epsilon = zip(*map(internal_estimator_function, inputs))
        internal_estimator_name = f"{internal_estimator_path[-1]} from {internal_estimator_path[-2].upper()}Estimator"

        execution_list.extend(
            list(
                starmap(
                    kat_test,
                    list(
                        zip(
                            [internal_estimator_name] * len(inputs),
                            inputs,
                            expected_outputs,
                            actual_outputs,
                            epsilon,
                        )
                    ),
                )
            )
        )
    assert False not in execution_list

import pytest
import yaml
from pathlib import Path
import inspect
import importlib
from typing import Tuple, Callable, Dict, Iterable, Any, List


def load_kat_data() -> Dict[str, Any]:
    """Load Known Answer Test (KAT) values from YAML file.

    Returns:
        Dict[str, Any]: Dictionary containing test cases and expected results
        loaded from the YAML file.

    Note:
        The YAML file should be named 'kat.yaml' and located in the same
        directory as this test file.
    """
    test_dir = Path(__file__).parent
    kat_yaml_path = test_dir / "kat.yaml"
    with kat_yaml_path.open("r") as file:
        return yaml.unsafe_load(file)


def extract_paths(
    nested_dict: Dict[str, Any], path: Tuple[str, ...] = ()
) -> Iterable[Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]]:
    """Recursively extract internal estimator paths and their corresponding test cases.

    This function traverses the input dictionary and yields tuples containing the
    internal estimator path and its input/output test cases for each leaf node
    containing an "inputs_with_expected_outputs" key.

    Args:
        nested_dict (Dict[str, Any]): The nested dictionary to traverse.
        path (Tuple[str, ...]): The current path in the dictionary (used for recursion).

    Yields:
        Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]: A tuple containing:
            - The path to the internal estimator
            - List of (input, expected_output) pairs for testing

    Example:
        For a dictionary like:
        {
            "estimator1": {
                "kat_generator": {
                    "inputs_with_expected_outputs": [(1, 2), (3, 4)]
                }
            }
        }
        It yields: (('estimator1', 'kat_generator'), [(1, 2), (3, 4)])
    """
    for key, value in nested_dict.items():
        current_path = path + (key,)
        if isinstance(value, dict):
            if "inputs_with_expected_outputs" in value:
                yield current_path, value["inputs_with_expected_outputs"]
            else:
                yield from extract_paths(value, current_path)


def import_internal_estimator(internal_estimator_path: Tuple[str, ...]) -> Callable:
    """Import an internal estimator function from a specified path.

    This function dynamically imports an estimator function based on the provided path,
    relative to the caller's location in the package hierarchy.

    Args:
        internal_estimator_path (Tuple[str, ...]): Path to the internal estimator function.
            The last element is the function name, preceding elements form the module path.

    Returns:
        Callable: The imported estimator function.

    Example:
        estimator = import_internal_estimator(('sdfq', 'lee-brickell'))
        # Imports the lee-brickell function from the sdfq module
    """
    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)

    package_parts = caller_module.__name__.split(".")
    caller_path = ".".join(package_parts[:-1] + ["internal_estimators"])

    module_path = ".".join(internal_estimator_path[:-1])
    function_name = internal_estimator_path[-1]

    import_path = f"{caller_path}.{module_path}"
    module = importlib.import_module(import_path)
    return getattr(module, function_name)


def generate_test_cases() -> List[Tuple[str, Tuple[str, ...], Any, float]]:
    """Generate test cases from KAT data for parametrized testing.

    Returns:
        List[Tuple[str, Tuple[str, ...], Any, float]]: List of test cases, each containing:
            - Estimator name (human-readable)
            - Estimator path (for importing)
            - Input value
            - Expected output value
    """
    kat = load_kat_data()
    test_cases = []

    for estimator_path, test_pairs in extract_paths(kat):
        estimator_name = (
            f"{estimator_path[-1]} from {estimator_path[-2].upper()}Estimator"
        )
        for input_val, expected_output in test_pairs:
            test_cases.append(
                (estimator_name, estimator_path, input_val, expected_output)
            )

    return test_cases


@pytest.mark.parametrize(
    "estimator_name,estimator_path,input_val,expected_output", generate_test_cases()
)
def test_kat(
    estimator_name: str,
    estimator_path: Tuple[str, ...],
    input_val: Any,
    expected_output: float,
) -> None:
    """Execute Known Answer Tests for internal estimators.

    This test verifies that internal estimators produce results within
    acceptable tolerance of known correct values.

    Args:
        estimator_name (str): Human-readable name of the estimator
        estimator_path (Tuple[str, ...]): Import path for the estimator
        input_val (Any): Test input value
        expected_output (float): Expected output value

    Raises:
        AssertionError: If the actual output differs from expected output
            by more than the allowed tolerance (epsilon)
    """
    estimator_func = import_internal_estimator(estimator_path)
    actual_output, epsilon = estimator_func(input_val)

    assert (
        abs(expected_output - actual_output) <= epsilon
        or expected_output == actual_output
    ), (
        f"FAILED TEST!!!\n"
        f"Input: {input_val}, estimator: {estimator_name}\n"
        f"Expected: {expected_output}, actual: {actual_output}, tolerance: {epsilon}"
    )

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
    relative to the tests directory.

    Args:
        internal_estimator_path (Tuple[str, ...]): Path to the internal estimator function.
            The last element is the function name, preceding elements form the module path.

    Returns:
        Callable: The imported estimator function.

    Example:
        estimator = import_internal_estimator(('sdfq', 'lee-brickell'))
        # Imports the lee-brickell function from the sdfq module
    """
    module_path = internal_estimator_path[-2]  # e.g., 'sdfq' or 'le'
    function_name = internal_estimator_path[-1]  # e.g., 'lee_brickell' or 'bbps_1'

    module = importlib.import_module(
        f"tests.kat_tests.internal_estimators.{module_path}"
    )
    return getattr(module, function_name)


def get_available_estimators() -> Dict[str, List[str]]:
    """Get all available estimators and their functions from the KAT data.

    Returns:
        Dict[str, List[str]]: Dictionary mapping estimator types to their functions.
        Example: {'sdfq': ['lee_brickell', 'stern'], 'le': ['bbps_1', 'bbps_2']}
    """
    kat = load_kat_data()
    estimators = {}

    for path, _ in extract_paths(kat):
        estimator = path[-2]  # e.g., 'sdfq', 'le'
        function_name = path[-1]  # e.g., 'lee_brickell', 'bbps_1'

        if estimator not in estimators:
            estimators[estimator] = []
        estimators[estimator].append(function_name)

    return estimators


def get_available_estimators_message() -> str:
    """Get a formatted string showing available estimators and their functions.

    Returns:
        str: A tree-style formatted string of available estimators and functions.
    """
    estimators = get_available_estimators()

    lines = [
        "\nAvailable estimators and functions:",
        "===================================",
    ]

    for estimator, functions in sorted(estimators.items()):
        lines.append(f"└── {estimator.upper()}Estimator")
        for func in sorted(functions):
            lines.append(f"    └── {func}")

    lines.append("\nOr use 'all' to run all tests")
    return "\n".join(lines)


def generate_test_cases(
    target: str = None,
) -> List[Tuple[str, Tuple[str, ...], Any, float]]:
    """Generate test cases from KAT data for parametrized testing.

    Args:
        target (str, optional): Target estimator or function to filter for. Defaults to None.
            Use 'all' to run all tests.

    Returns:
        List[Tuple[str, Tuple[str, ...], Any, float]]: List of test cases, each containing:
            - Estimator name (human-readable)
            - Estimator path (for importing)
            - Input value
            - Expected output value
    """
    kat = load_kat_data()
    test_cases = []

    # Case 1: No filtering needed
    if not target or target.lower() == "all":
        for estimator_path, test_pairs in extract_paths(kat):
            estimator_name = (
                f"{estimator_path[-1]} from {estimator_path[-2].upper()}Estimator"
            )
            test_cases.extend(
                [
                    (estimator_name, estimator_path, input_val, expected_output)
                    for input_val, expected_output in test_pairs
                ]
            )
        return test_cases

    # Case 2: Filter by target
    target = target.lower()
    for estimator_path, test_pairs in extract_paths(kat):
        estimator = estimator_path[-2].lower()  # e.g., 'sdfq' or 'le'
        function_name = estimator_path[-1].lower()  # e.g., 'lee_brickell' or 'bbps_1'

        # Only process paths that match the target
        if target == estimator or target == function_name:
            estimator_name = (
                f"{estimator_path[-1]} from {estimator_path[-2].upper()}Estimator"
            )
            test_cases.extend(
                [
                    (estimator_name, estimator_path, input_val, expected_output)
                    for input_val, expected_output in test_pairs
                ]
            )

    return test_cases


def pytest_generate_tests(metafunc):
    """Pytest hook to generate test cases with the target filter applied."""
    if "estimator_name" in metafunc.fixturenames:
        target = metafunc.config.getoption("--target-kat")
        test_cases = generate_test_cases(target)

        # If we got an empty list of test cases, it means no valid target was found
        if not test_cases:
            skip_message = f"No test cases found for target '{target}'\n{get_available_estimators_message()}"
            pytest.skip(skip_message)

        metafunc.parametrize(
            "estimator_name,estimator_path,input_val,expected_output", test_cases
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

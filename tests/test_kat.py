import pytest
import yaml
from pathlib import Path
import inspect
import importlib
from typing import Tuple, Callable, Dict, Iterable, Any, List


def load_kat_data():
    """Load KAT values from YAML file"""
    test_dir = Path(__file__).parent
    kat_yaml_path = test_dir / "kat.yaml"
    with kat_yaml_path.open("r") as file:
        return yaml.unsafe_load(file)


def extract_paths(
    nested_dict: Dict[str, Any], path: Tuple[str, ...] = ()
) -> Iterable[Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]]:
    """Recursively extracts internal estimators paths and their corresponding inputs/outputs tuples."""
    for key, value in nested_dict.items():
        current_path = path + (key,)
        if isinstance(value, dict):
            if "inputs_with_expected_outputs" in value:
                yield current_path, value["inputs_with_expected_outputs"]
            else:
                yield from extract_paths(value, current_path)


def import_internal_estimator(internal_estimator_path: Tuple[str, ...]) -> Callable:
    """Imports an internal estimator function from a specified path."""
    caller_frame = inspect.currentframe().f_back
    caller_module = inspect.getmodule(caller_frame)

    package_parts = caller_module.__name__.split(".")
    caller_path = ".".join(package_parts[:-1] + ["internal_estimators"])

    single_case_module_path = ".".join(internal_estimator_path[:-1])
    function_name = internal_estimator_path[-1]

    import_modpath = f"{caller_path}.{single_case_module_path}"
    module = importlib.import_module(import_modpath)
    return getattr(module, function_name)


def generate_test_cases():
    """Generate test cases from KAT data."""
    kat = load_kat_data()
    test_cases = []

    for internal_estimator_path, inputs_with_outputs in extract_paths(kat):
        internal_estimator_name = f"{internal_estimator_path[-1]} from {internal_estimator_path[-2].upper()}Estimator"
        for input_val, expected_output in inputs_with_outputs:
            test_cases.append(
                (
                    internal_estimator_name,
                    internal_estimator_path,
                    input_val,
                    expected_output,
                )
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
):
    """Test each case, including the estimation computation."""
    # Import and run the estimator function here so it's part of the parallel execution
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

import pytest
import inspect
import importlib
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import Tuple, Callable, Dict, Iterable, Any, List
from pathlib import Path
import yaml


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


def compute_estimation(
    test_case: Tuple[Callable, Any, Any, str]
) -> Tuple[str, Any, Any, Any, float]:
    """Compute a single estimation and return complete test case data."""
    estimator_func, input_val, expected_output, estimator_name = test_case
    actual_output, epsilon = estimator_func(input_val)
    return estimator_name, input_val, expected_output, actual_output, epsilon


def compute_all_estimations():
    """Compute all estimations in parallel once and return results."""
    kat = load_kat_data()
    test_cases = []

    # Prepare test cases
    for internal_estimator_path, inputs_with_outputs in extract_paths(kat):
        internal_estimator_function = import_internal_estimator(internal_estimator_path)
        estimator_name = f"{internal_estimator_path[-1]} from {internal_estimator_path[-2].upper()}Estimator"

        test_cases.extend(
            (internal_estimator_function, input_val, expected, estimator_name)
            for input_val, expected in inputs_with_outputs
        )

    # Compute all results in parallel
    with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        return list(executor.map(compute_estimation, test_cases))


@pytest.mark.parametrize("test_case", compute_all_estimations())
def test_kat(test_case):
    """Test using pre-computed results."""
    estimator_name, input_val, expected_output, actual_output, epsilon = test_case

    assert (
        abs(expected_output - actual_output) <= epsilon
        or expected_output == actual_output
    ), (
        f"FAILED TEST!!!\n"
        f"Input: {input_val}, estimator: {estimator_name}\n"
        f"Expected: {expected_output}, actual: {actual_output}, tolerance: {epsilon}"
    )

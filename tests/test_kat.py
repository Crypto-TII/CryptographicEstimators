import inspect
import importlib
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from typing import Tuple, Callable, Dict, Iterable, Any, List


def extract_paths(
    nested_dict: Dict[str, Any], path: Tuple[str, ...] = ()
) -> Iterable[Tuple[Tuple[str, ...], List[Tuple[Any, Any]]]]:
    """Recursively extracts internal estimators paths and their corresponding inputs/outputs tuples from the input dictionary."""
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
    function = getattr(module, function_name)

    return function


def run_test(test_case: Tuple[Callable, Any, Any, str]) -> bool:
    """Runs a single test case."""
    estimator_func, input_val, expected_output, estimator_name = test_case
    actual_output, epsilon = estimator_func(input_val)

    if (
        not abs(expected_output - actual_output) <= epsilon
        and expected_output != actual_output
    ):
        print("FAILED TEST!!!")
        print(f"Input: {input_val}, estimator: {estimator_name}")
        print(
            f"Expected: {expected_output}, actual: {actual_output}, tolerance: {epsilon} "
        )
        return False
    return True


def test_all_estimators(kat: dict):
    """Runs KAT tests for all internal estimators in parallel."""
    test_cases = []

    for internal_estimator_path, inputs_with_outputs in extract_paths(kat):
        inputs, expected_outputs = zip(*inputs_with_outputs)
        internal_estimator_function = import_internal_estimator(internal_estimator_path)
        internal_estimator_name = f"{internal_estimator_path[-1]} from {internal_estimator_path[-2].upper()}Estimator"

        test_cases.extend(
            (internal_estimator_function, input_val, expected, internal_estimator_name)
            for input_val, expected in zip(inputs, expected_outputs)
        )

    # Run tests in parallel using ProcessPoolExecutor
    n_cores = cpu_count()
    with ProcessPoolExecutor(max_workers=n_cores) as executor:
        results = executor.map(run_test, test_cases)
        assert all(results), "Some tests failed"

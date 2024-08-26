import pytest
import yaml
import inspect
import os

from tests.helper import DOCKER_YAML_REFERENCE_PATH


@pytest.fixture(scope="session")
def yaml_references() -> dict:
    """
    Load YAML references from the specified file.
    """
    with open(DOCKER_YAML_REFERENCE_PATH, "r") as file:
        return yaml.unsafe_load(file)


@pytest.fixture(scope="session")
def test_data(yaml_references: dict):
    """
    Fixture to retrieve test data from YAML references.
    """

    def get_test_data(test_file: str = None, test_function: str = None):
        """
        Get inputs and expected outputs for a specific test function.
        If test_file or test_function is not provided, it will be inferred from the caller.
        """
        if test_file is None or test_function is None:
            caller_frame = inspect.currentframe().f_back
            if test_file is None:
                test_file = os.path.splitext(
                    os.path.basename(caller_frame.f_code.co_filename)
                )[0]
            if test_function is None:
                test_function = caller_frame.f_code.co_name

        data = yaml_references[test_file][test_function]
        return data["inputs_with_expected_outputs"]

    return get_test_data

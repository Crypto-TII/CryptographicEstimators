import pytest
import yaml

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

    def get_test_data(test_file: str, test_function: str):
        """
        Get inputs and expected outputs for a specific test function.
        """
        data = yaml_references[test_file][test_function]
        return data["inputs"], data["expected_outputs"]

    return get_test_data

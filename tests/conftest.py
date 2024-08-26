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

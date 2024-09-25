import pytest
import yaml
from pathlib import Path


@pytest.fixture(scope="session")
def kat() -> dict:
    """
    Load KAT values serialized in YAML from the kat.yaml file in the same directory as conftest.py.
    """
    conftest_dir = Path(__file__).parent
    kat_yaml_path = conftest_dir / "kat.yaml"

    with kat_yaml_path.open("r") as file:
        return yaml.unsafe_load(file)

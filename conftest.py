import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-long-doctests",
        action="store_true",
        default=False,
        help="Flag to skip long time execution doctests",
    )


@pytest.fixture(autouse=True)
def add_longtests(request, doctest_namespace):
    doctest_namespace["skip_long_doctests"] = request.config.getoption(
        "--skip-long-doctests"
    )

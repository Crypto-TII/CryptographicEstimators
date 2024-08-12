import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--long-doctests",
        action="store_true",
        default=False,
        help="run long doctests",
    )


@pytest.fixture(autouse=True)
def add_longtests(request, doctest_namespace):
    doctest_namespace["long_doctests"] = request.config.getoption("--long-doctests")

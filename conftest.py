import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--skip-long-doctests",
        action="store_true",
        default=False,
        help="Flag to skip long time execution doctests",
    )
    parser.addoption(
        "--target-kat",
        action="store",
        default=None,
        help="Target specific KAT test(s) to run. Can be an estimator name or a specific test function",
    )


@pytest.fixture(autouse=True)
def add_longtests(request, doctest_namespace):
    doctest_namespace["skip_long_doctests"] = request.config.getoption(
        "--skip-long-doctests"
    )


@pytest.fixture
def target_kat(request):
    return request.config.getoption("--target-kat")

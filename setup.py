from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import multiprocessing
import os
import sys


package_name = "cryptographic_estimators"

# Get information from separate files (README, VERSION)


def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()


def run_tests(include_long_tests):
    ncpus = multiprocessing.cpu_count()
    timeout_in_sec = 3600  # 1 hour

    SAGE_BIN = ""
    if os.path.exists("SAGE_BIN_PATH"):
        SAGE_BIN = readfile("SAGE_BIN_PATH").strip()

    if len(SAGE_BIN) == 0:
        SAGE_BIN = "sage"

    long_test_flag = ""
    if include_long_tests:
        long_test_flag = "--long"

    errno = os.system(
        f"{SAGE_BIN} -t {long_test_flag} -T {timeout_in_sec} --nthreads {ncpus} --force-lib " + package_name)
    if errno != 0:
        sys.exit(1)

# For the tests


class SageTestFast(TestCommand):
    def run_tests(self):
        run_tests(include_long_tests=False)


class SageTestAll(TestCommand):
    def run_tests(self):
        run_tests(include_long_tests=True)


package_name = "cryptographic_estimators"
packages = find_packages()
setup(
    name="cryptographic_estimators",
    version="1.0.1",
    author="TII",
    description="This library provides bit security estimators and asymptotic complexity estimators for cyrptographic problems. So far it covers the binary Syndrome Decoding Problem (SDEstimator) and the Multivaritate Quadratic Problem (MQEstimator).",
    packages=packages,
    package_dir={package_name: package_name},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # adding a special setup command for tests
    cmdclass={'testfast': SageTestFast, 'testall': SageTestAll},
)

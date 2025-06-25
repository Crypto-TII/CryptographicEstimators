from cryptographic_estimators.PKEstimator import PKProblem
from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP, SBC
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange, LeeBrickell


TEST_PARAMETERS = {
    "bit_complexities": False,
    "cost_for_list_operation": 1,
    "memory_for_list_element": 1,
    "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]},
}


def kmp(input: tuple, epsilon: float = 0.1):
    n, m, q, ell = input

    actual_complexity = KMP(
        PKProblem(n, m, q, ell), **TEST_PARAMETERS
    ).time_complexity()

    return actual_complexity, epsilon


def sbc(input: tuple, epsilon: float = 0.1):
    n, m, q, ell = input

    actual_complexity = SBC(
        PKProblem(n, m, q, ell), **TEST_PARAMETERS
    ).time_complexity()

    return actual_complexity, epsilon


def kmp_range(input: tuple, epsilon: float = 0.1):
    n, m, q, ell = input

    actual_complexity = KMP(
        PKProblem(n, m, q, ell), **TEST_PARAMETERS
    ).time_complexity()

    return actual_complexity, epsilon


def sbc_range(input: tuple, epsilon: float = 0.1):
    n, m, q, ell = input

    actual_complexity = SBC(
        PKProblem(n, m, q, ell), **TEST_PARAMETERS
    ).time_complexity()

    return actual_complexity, epsilon

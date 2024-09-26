from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange

BEULLENS_PARAMS = {"bit_complexities": 0}

BBPS_PARAMS = {
    "bit_complexities": 1,
    "sd_parameters": {"excluded_algorithms": ["Prange", "LeeBrickell"]},
}


def beullens(input: tuple, epsilon: float = 0.12):
    n, k, q = input

    actual_complexity = Beullens(
        LEProblem(n, k, q), **BEULLENS_PARAMS
    ).time_complexity()

    return actual_complexity, epsilon


def beullens_range(input: tuple, epsilon: float = 0.12):
    n, k, q = input

    candidate_1 = Beullens(LEProblem(n, k, q), **BEULLENS_PARAMS).time_complexity()
    candidate_2 = Beullens(LEProblem(n, k, q), **BEULLENS_PARAMS).time_complexity()
    actual_complexity = min(candidate_1, candidate_2)

    return actual_complexity, epsilon

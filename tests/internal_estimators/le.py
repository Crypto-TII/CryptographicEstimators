from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange

BEULLENS_PARAMS = {"bit_complexities": 0}

BBPS_PARAMS = {
    "bit_complexities": 1,
    "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]},
}


# Beullens
def beullens(input: tuple, epsilon: float = 0.12):
    n, k, q = input

    actual_complexity = Beullens(
        LEProblem(n, k, q), **BEULLENS_PARAMS
    ).time_complexity()

    return actual_complexity, epsilon


def beullens_range(input: tuple, epsilon: float = 1.2):
    """The higher tolerance is required to compensate the variance caused by the probabilistic nature of beullens runtime computation.

    For more info: https://github.com/Crypto-TII/CryptographicEstimators/issues/152#issuecomment-2395990074
    """
    n, k, q = input

    candidate_1 = Beullens(LEProblem(n, k, q), **BEULLENS_PARAMS).time_complexity()
    candidate_2 = Beullens(LEProblem(n, k, q), **BEULLENS_PARAMS).time_complexity()
    actual_complexity = min(candidate_1, candidate_2)

    return actual_complexity, epsilon


# BBPS
def bbps_1(input: tuple, epsilon: float = 0.1):
    n, k, q = input

    actual_complexity = BBPS(LEProblem(n, k, q), **BBPS_PARAMS).time_complexity()

    return actual_complexity, epsilon


def bbps_2(input: tuple, epsilon: float = 1):
    """For small q we need to allow for a slightly larger tolerance, because the coupon collector approximation is less accurate."""
    n, k, q = input

    actual_complexity = BBPS(LEProblem(n, k, q), **BBPS_PARAMS).time_complexity()

    return actual_complexity, epsilon


def bbps_range(input: tuple, epsilon: float = 1):
    n, k, q = input

    candidate_1 = BBPS(LEProblem(n, k, q), **BBPS_PARAMS).time_complexity()
    candidate_2 = BBPS(LEProblem(n, k, q), **BBPS_PARAMS).time_complexity()
    actual_complexity = min(candidate_1, candidate_2)

    return actual_complexity, epsilon

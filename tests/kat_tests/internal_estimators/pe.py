from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange, Stern
from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon, Beullens
from cryptographic_estimators.PEEstimator import PEProblem

leon_params = {
    "bit_complexities": 0,
    "sd_parameters": {"excluded_algorithms": [Prange, Stern]},
}


def leon1(input, epsilon=0.01):
    n, k, q = input

    actual_complexity = Leon(PEProblem(n, k, q), **leon_params).time_complexity()

    return actual_complexity, epsilon


def leon2(input, epsilon=0.01):
    actual_complexity, epsilon = leon1(input, epsilon)
    return actual_complexity, epsilon


def beullens(input, epsilon=0.01):
    n, k, q = input

    complexities = [
        Beullens(PEProblem(n, k, q), **leon_params).time_complexity() for _ in range(20)
    ]
    actual_complexity = min(complexities)

    return actual_complexity, epsilon

from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem

PARAMS = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
STERN_PARAMS = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}


def int_lee_brickell(input, epsilon=0.01):
    """
    Single case test for the LeeBrickell-SDFq problem with an error tolerance of epsilon.
    """
    n, k, w, q = input
    p = 2

    actual_complexity = LeeBrickell(
        SDFqProblem(n, k, w, q, **PARAMS), **PARAMS
    ).time_complexity(p=p)

    return actual_complexity, epsilon


def int_stern(input, epsilon=0.01):
    """
    Stern stimate produced by the CryptographicEstimators library
    Estimate for testing
    Single case test for the Stern-SDFq problem with an error tolerance of epsilon.
    """
    n, k, w, q = input

    actual_complexity = Stern(
        SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS
    ).time_complexity()

    return actual_complexity, epsilon


def int_stern_range(input, epsilon=0.05):
    """
    Single case test for the Stern-SDFq problem with an error tolerance of epsilon.

    Notes:
        This test sets the parameter range for 'l' from 1 to (n-k) for each problem instance,
        allowing the algorithm to optimize over this range when calculating the time complexity.
    """
    n, k, w, q = input
    algorithm = Stern(SDFqProblem(n, k, w, q, **STERN_PARAMS), **STERN_PARAMS)
    algorithm.set_parameter_ranges("l", 1, n - k)
    actual_complexity = algorithm.time_complexity()

    return actual_complexity, epsilon

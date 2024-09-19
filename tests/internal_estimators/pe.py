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


# For small values due to rounding issues we have to slightly increase the tolerance
def leon(input, epsilon=0.2):
    n, k, q = input

    # due to slightly different calculation of "number_of_weight_d_codewords" optimal w might differ by 1
    # for some edge cases
    actual_complexity_1 = Leon(PEProblem(n, k, q), **leon_params).time_complexity()
    actual_complexity_2 = Leon(PEProblem(n, k, q), **leon_params).time_complexity(
        w=A.optimal_parameters()["w"] - 1
    )

    # FIX: Now what?

    return actual_complexity, epsilon


def beullens(input, epsilon=0.01):
    n, k, q = input

    complexities = [
        Beullens(PEProblem(n, k, q), **leon_params).time_complexity() for _ in range(10)
    ]
    actual_complexity = min(complexities)

    return actual_complexity, epsilon

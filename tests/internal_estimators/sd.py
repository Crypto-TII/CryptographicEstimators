import sys
from cryptographic_estimators.SDEstimator import (
    SDProblem,
    SDEstimator,
    Prange,
    Dumer,
    BallCollision,
    BJMM,
    BJMMdw,
    BJMMpdw,
    BothMay,
    MayOzerov,
    Stern,
    BJMMplus,
)
from cryptographic_estimators.SDEstimator.SDAlgorithms import (
    Prange,
    Dumer,
    BallCollision,
    BJMMd2,
    BJMMd3,
    BJMM,
    BJMMdw,
    BJMMpdw,
    BothMay,
    MayOzerov,
    MayOzerovD2,
    MayOzerovD3,
    Stern,
    BJMMplus,
)


def estimates_with_prange(input: tuple, epsilon: int = 0):
    n, k, w, excluded_algorithms_names = input
    excluded_algorithms = list(
        map(lambda x: getattr(sys.modules[__name__], x), excluded_algorithms_names)
    )
    actual_complexity = SDEstimator(
        n, k, w, excluded_algorithms=excluded_algorithms
    ).estimate()["Prange"]["estimate"]["time"]

    return actual_complexity, epsilon


def bjmm_plus(input: tuple, epsilon: float = 0.01):
    n, k, w = input
    actual_complexity = BJMMplus(
        SDProblem(n, k, w), bit_complexities=0
    ).time_complexity()

    return actual_complexity, epsilon


def estimators_1(input: tuple, epsilon: float = 0.01):
    n, k, w, estimator_name = input
    internal_estimator = globals()[estimator_name]
    actual_complexity = internal_estimator(
        SDProblem(n, k, w), bit_complexities=0
    ).time_complexity()

    return actual_complexity, epsilon


def estimators_2(input: tuple, epsilon: float = 1.5):
    """
    The CryptographicEstimators finds (slightly) better parameters which lead to slightly better timings in case of Both-May and May-Ozerov. But given the same parameters the CryptographicEstimatos and SyndromeDecodingEstimators compute the same expected runtime. That's why we use a higher tolerance in this case.
    """
    return estimators_1(input, epsilon)

def estimators_3(input: tuple, epsilon: float = 0.5):
    """
    PENDING
    """
    return estimators_1(input, epsilon)


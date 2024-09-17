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
    ).estimate()

    return actual_complexity, epsilon

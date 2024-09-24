import sys
from cryptographic_estimators.MQEstimator import (
    MQProblem,
    MQEstimator,
    MQProblem,
    Bjorklund,
    BooleanSolveFXL,
    CGMTA,
    Crossbred,
    DinurFirst,
    DinurSecond,
    ExhaustiveSearch,
    F5,
    HybridF5,
    KPG,
    Lokshtanov,
    MHT,
)


def estimates_with_bjorklund_1(input: tuple, epsilon: int = 0):
    n, m, q, excluded_algorithms_names = input

    excluded_algorithms = [
        globals()[exc_algorithm_name]
        for exc_algorithm_name in excluded_algorithms_names
    ]
    internal_estimator = MQEstimator(n, m, q, excluded_algorithms=excluded_algorithms)
    actual_complexity = internal_estimator.estimate()["Bjorklund"]["estimate"]["time"]

    return actual_complexity, epsilon


def estimates_with_bjorklund_2(input: tuple, epsilon: int = 0):
    n, m, q, excluded_algorithms_names = input

    excluded_algorithms = [
        globals()[exc_algorithm_name]
        for exc_algorithm_name in excluded_algorithms_names
    ]
    internal_estimator = MQEstimator(n, m, q, excluded_algorithms=excluded_algorithms)
    actual_complexity = internal_estimator.estimate()["ExhaustiveSearch"]["estimate"][
        "time"
    ]

    return actual_complexity, epsilon

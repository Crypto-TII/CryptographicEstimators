from sage.all_cmdline import *
from math import log2

from tests.external_estimators.MQEstimator.legacy_implementations.mpkc.algorithms import (
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


def ext_estimates_with_bjorklund_1():

    # TODO: Add dictionary comparison support in a post-migration
    # step to unify ext_estimates_with_bjorklund_1 and _2
    # expected_dictionary = {
    #     "Bjorklund": {
    #         "estimate": {
    #             "time": 67.23834058346328,
    #             "memory": 47.4854636165402,
    #             "parameters": {"lambda_": 5 / 49},
    #         },
    #         "additional_information": {},
    #     },
    #     "ExhaustiveSearch": {
    #         "estimate": {
    #             "time": 52.48921146923813,
    #             "memory": 16.844129532345626,
    #             "parameters": {},
    #         },
    #         "additional_information": {},
    #     },
    # }

    excluded_algorithms = [
        "DinurFirst",
        "DinurSecond",
        "BooleanSolveFXL",
        "HybridF5",
        "Lokshtanov",
        "Crossbred",
        "F5",
        "KPG",
        "CGMTA",
        "MHT",
    ]

    inputs = [(100, 50, 2, excluded_algorithms)]

    expected_outputs = [67.23834058346328]
    inputs_with_expected_outputs = list(zip(inputs, expected_outputs))
    return inputs_with_expected_outputs


def ext_estimates_with_bjorklund_2():

    excluded_algorithms = [
        "DinurFirst",
        "DinurSecond",
        "BooleanSolveFXL",
        "HybridF5",
        "Lokshtanov",
        "Crossbred",
        "F5",
        "KPG",
        "CGMTA",
        "MHT",
    ]

    inputs = [(100, 50, 2, excluded_algorithms)]

    expected_outputs = [52.48921146923813]
    inputs_with_expected_outputs = list(zip(inputs, expected_outputs))
    return inputs_with_expected_outputs


def ext_estimators():
    """Generate expected complexities for MQ algorithms.

    Taken from https://github.com/Crypto-TII/multivariate_quadratic_estimatorup.
    """

    inputs = [
        [50, 50, 2],
        [70, 70, 4],
        [50, 70, 8],
        [120, 40, 8],
    ]

    external_algorithms = [
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
    ]

    def gen_single_kat(input, external_algorithm):
        n, m, q = input
        external_algorithm_name = external_algorithm.__name__
        try:
            if q == 2 and external_algorithm in [Bjorklund, DinurFirst, DinurSecond]:
                external_estimator = external_algorithm(n=n, m=m)
            else:
                external_estimator = external_algorithm(n=n, m=m, q=q, w=2.81)
        except:
            return None

        expected_complexity = log2(external_estimator.time_complexity())
        input = n, m, q, external_algorithm_name
        return input, expected_complexity

    inputs_with_expected_outputs = [
        gen_single_kat(input, estimator)
        for input in inputs
        for estimator in external_algorithms
    ]
    return [element for element in inputs_with_expected_outputs if element is not None]

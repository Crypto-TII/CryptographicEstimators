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

from sage.all_cmdline import *
import pytest
from math import log2
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
from tests.MQEstimator.legacy_implementations.mpkc.algorithms import (
    Bjorklund as TestBjorklund,
    BooleanSolveFXL as TestBooleanSolveFXL,
    CGMTA as TestCGMTA,
    Crossbred as TestCrossbred,
    DinurFirst as TestDinurFirst,
    DinurSecond as TestDinurSecond,
    ExhaustiveSearch as TestExhaustiveSearch,
    F5 as TestF5,
    HybridF5 as TestHybridF5,
    KPG as TestKPG,
    Lokshtanov as TestLokshtanov,
    MHT as TestMHT,
)


ranges = 0.01

test_sets = [
    # n   m   q
    [50, 50, 2],
    [70, 70, 4],
    [50, 70, 8],
    [120, 40, 8],
]

algos = [
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

test_algos = [
    TestBjorklund,
    TestBooleanSolveFXL,
    TestCGMTA,
    TestCrossbred,
    TestDinurFirst,
    TestDinurSecond,
    TestExhaustiveSearch,
    TestF5,
    TestHybridF5,
    TestKPG,
    TestLokshtanov,
    TestMHT,
]


def test_estimates_with_bjorklund():
    excluded_algorithms = [
        DinurFirst,
        DinurSecond,
        BooleanSolveFXL,
        HybridF5,
        Lokshtanov,
        Crossbred,
        F5,
        KPG,
        CGMTA,
        MHT,
    ]

    mq_estimator = MQEstimator(100, 50, 2, excluded_algorithms=excluded_algorithms)
    result = mq_estimator.estimate()
    expected_result = {
        "Bjorklund": {
            "estimate": {
                "time": 67.23834058346328,
                "memory": 47.4854636165402,
                "parameters": {"lambda_": 5 / 49},
            },
            "additional_information": {},
        },
        "ExhaustiveSearch": {
            "estimate": {
                "time": 52.48921146923813,
                "memory": 16.844129532345626,
                "parameters": {},
            },
            "additional_information": {},
        },
    }

    assert expected_result == result


def test_mq_raises_exception_with_bjorklund():
    e = [
        DinurFirst,
        DinurSecond,
        BooleanSolveFXL,
        HybridF5,
        Lokshtanov,
        Crossbred,
        F5,
        KPG,
        CGMTA,
        MHT,
    ]

    with pytest.raises(TypeError, match="q must be equal to 2"):
        Bjorklund(MQProblem(100, 50, 4))
        mq_estimator = MQEstimator(100, 50, 4, excluded_algorithms=e)
        mq_estimator.estimate()


def test_all():
    """
    tests that all estimations match those from https://github.com/Crypto-TII/multivariate_quadratic_estimatorup to
    a tolerance of 0.01 bit
    """
    assert len(algos) == len(test_algos)
    for i, _ in enumerate(test_algos):
        A1 = algos[i]
        A2 = test_algos[i]
        for set in test_sets:
            n, m, q = set[0], set[1], set[2]
            print(n, m, q)

            try:
                Alg1 = A1(MQProblem(n=n, m=m, q=q), bit_complexities=0)
                if q == 2 and A1 in [Bjorklund, DinurFirst, DinurSecond]:
                    Alg2 = A2(n=n, m=m)
                else:
                    Alg2 = A2(n=n, m=m, q=q, w=2.81)

            except:
                continue

            T1 = Alg1.time_complexity()
            T2 = log2(Alg2.time_complexity())
            print(Alg1._name, T1, T2)
            # print(Alg1.optimal_parameters())
            # print(Alg2._optimal_parameters)
            assert T2 - ranges <= T1 <= T2 + ranges


if __name__ == "__main__":
    test_all()

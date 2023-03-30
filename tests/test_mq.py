
from sage.all_cmdline import *

from math import log2
from .module.multivariate_quadratic_estimator.mpkc.algorithms.bjorklund import Bjorklund as TestBjorklund
from .module.multivariate_quadratic_estimator.mpkc.algorithms.boolean_solve_fxl import BooleanSolveFXL as TestBooleanSolveFXL
from .module.multivariate_quadratic_estimator.mpkc.algorithms.cgmta import CGMTA as TestCGMTA
from .module.multivariate_quadratic_estimator.mpkc.algorithms.crossbred import Crossbred as TestCrossbred
from .module.multivariate_quadratic_estimator.mpkc.algorithms.dinur1 import DinurFirst as TestDinurFirst
from .module.multivariate_quadratic_estimator.mpkc.algorithms.dinur2 import DinurSecond as TestDinurSecond
from .module.multivariate_quadratic_estimator.mpkc.algorithms.exhaustive_search import ExhaustiveSearch as TestExhaustiveSearch
from .module.multivariate_quadratic_estimator.mpkc.algorithms.f5 import F5 as TestF5
from .module.multivariate_quadratic_estimator.mpkc.algorithms.hybrid_f5 import HybridF5 as TestHybridF5
from .module.multivariate_quadratic_estimator.mpkc.algorithms.kpg import KPG as TestKPG
from .module.multivariate_quadratic_estimator.mpkc.algorithms.lokshtanov import Lokshtanov as TestLokshtanov
from .module.multivariate_quadratic_estimator.mpkc.algorithms.mht import MHT as TestMHT
from cryptographic_estimators.MQEstimator.MQAlgorithms import Bjorklund, BooleanSolveFXL, CGMTA, Crossbred, \
    DinurFirst, DinurSecond, ExhaustiveSearch, F5, HybridF5, KPG, Lokshtanov, MHT

from cryptographic_estimators.MQEstimator import MQProblem

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
    MHT
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
    TestMHT
]


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
                    Alg2 = A2(n=n, m=m, q=q)

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

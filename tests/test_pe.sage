from math import comb, ceil, log2, log
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
from cryptographic_estimators.PEEstimator import PEProblem
from cryptographic_estimators.PEEstimator.pe_helper import number_of_weight_d_codewords, gv_distance


load('tests/module/attack_cost.sage')
load('tests/module/cost.sage')

# global parameters
leon_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]}}


def test_leon1():
    """
    test some hardcoded values taken from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py 
    """
    ranges = 2.
    n, k, q = 250, 150, 53
    t1 = LEON(n, k, q) + log2(n)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges

    n, k, q = 106, 45, 7
    t1 = LEON(n, k, q) + log2(n)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges


def test_leon2():
    """
    test some hardcoded values from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """
    ranges = 2.
    n, k= 250, 150
    q_values = [11, 17, 53, 103, 151, 199, 251]
    for q in q_values:
        t1 = LEON(n, k, q) + log2(n)
        assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges


def test_leon():
    """
    tests leon on small instances
    """
    ranges = 4.5
    for n in range(30, 100, 5):
        for k in range(int(0.3*n), int(0.7*n), 5):
            for q in [3, 7, 17, 31]:
                t1 = Leon(PEProblem(n, k, q), **leon_params).time_complexity()
                t2 = LEON(n, k, q) + log2(n)
                assert t2 - ranges < t1 < t2 + ranges

if __name__ == "__main__":
    test_leon1()
    test_leon2()
    test_leon()

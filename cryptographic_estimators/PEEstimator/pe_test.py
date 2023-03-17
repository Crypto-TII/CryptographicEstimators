from math import comb, ceil, log2, log
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
from cryptographic_estimators.PEEstimator import PEProblem
from cryptographic_estimators.PEEstimator.pe_helper import number_of_weight_d_codewords, gv_distance


# global parameters
leon_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]}}


def minimal_w(n: int, k: int, q: int):
    w = 1;
    S = 0
    limit = min(100, int(number_of_weight_d_codewords(n, k, q, gv_distance(n, k, q) + 3)))
    while True:
        S += comb(n, w) * (q - 1) ** (w - 1)
        if S > limit * q ** (n - k):
            return w, ceil(S / q ** (n - k))
        w = w + 1


def ISD_COST(n,k,w,q):
    return (k*k + k*k*q)*comb(n,w)//comb(n-k,w-2)//comb(k,2)


def LEON(n, k, q):
    w, N = minimal_w(n, k, q)
    c_isd = ISD_COST(n, k, w, q) * n
    S = ceil(2 * (0.57 + log(N))) * c_isd
    return log2(S)


def test_leon1():
    """
    test some hardcoded values taken from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py 
    """
    ranges = 2.
    n, k, q = 250, 150, 53
    t1 = LEON(n, k, q)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges

    n, k, q = 106, 45, 7
    t1 = LEON(n, k, q)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges

    # TODO to big values
    n, k, q = 280, 117, 149
    t1 = LEON(n, k, q)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges

    n, k, q = 305, 127, 31
    t1 = LEON(n, k, q)
    assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges


def test_leon2():
    """
    test some hardcoded values from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """
    ranges = 2.
    n, k= 250, 150
    q_values = [11, 17, 53, 103, 151, 199, 251];
    for q in q_values:
        t1 = LEON(n, k, q)
        assert t1 - ranges <= Leon(PEProblem(n, k, q), **leon_params).time_complexity() <= t1 + ranges


#def test_leon():
#    """
#    tests leon on small instances
#    """
#    ranges = 2.
#    for n in range(10, 100, 5):
#        for k in range(int(0.3*n), int(0.7*n), 5):
#            for q in [3, 7, 17, 31]:
#                t1 = Leon(PEProblem(n, k, q), **leon_params).time_complexity()
#                t2 = LEON(n, k, q)
#                assert t2 - ranges < t1 < t2 + ranges


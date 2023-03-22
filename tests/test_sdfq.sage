from cryptographic_estimators.SDFqEstimator import SDFqEstimator
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem
from math import  floor, log2, ceil, comb, comb as binomial, log2 as log


load('tests/module/attack_cost.sage')
load('tests/module/cost.sage')


# global parameters
params = {"nsolutions": 0}


def test_sdfq_LeeBrickell():
    """
    special value test for Lee-Brickell
    """
    ranges = 2.0
    n, k, w, q = 256, 128, 64, 251
    t = ISD_COST(n, k, w, q)
    assert(t - ranges < LeeBrickell(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)

    n, k, w, q = 961, 771, 48, 31
    t = ISD_COST(n, k, w, q)
    assert(t - ranges < LeeBrickell(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)


def test_sdfq_stern():
    """
    special value test for Stern
    """
    ranges = 0.3
    n, k, w, q = 256, 128, 128, 251
    t = peters_isd(n, k, q, w)
    assert(t - ranges < Stern(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)

    n, k, w, q = 961,771, 48,31
    t = peters_isd(n, k, q, w)
    assert(t - ranges < Stern(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)


def test_sdfq_stern_range():
    """
    range test for Stern
    """
    ranges = 5.

    for n in range(30, 100):
        for k in range(int(0.2 * n), int(0.8 * n)):
            for w in range(1, min(n - k - 1, int(0.5 * n))):
                for q in [3, 7, 11, 17, 53, 103, 151, 199, 251]:
                    t1 = Stern(SDFqProblem(n, k, w, q, **params)).time_complexity()
                    t2 = peters_isd(n, k, q, w)
                    assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_sdfq_stern_range()
    test_sdfq_LeeBrickell()
    test_sdfq_stern()

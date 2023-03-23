import random
#from math import comb, comb as binomial, ceil, log2, log, factorial, sqrt, inf, floor
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern


load('tests/module/attack_cost.sage')
load('tests/module/cost.sage')

#from module.attack_cost import *
#from module.cost import *

bbps_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}
ranges = 3.


def test_bbps1():
    """
    special value test
    """
    n = 200
    k = 100
    for q in [11, 17, 31]:
        A = BBPS(LEProblem(n, k, q), **bbps_params)
        t1 = A.time_complexity()
        t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)
        if not (t2 - ranges< t1 < t2 + ranges):
            print(n, k, q, t1, t2)


def test_bbps2():
    """
    generic test
    """
    for n in range(100, 120):
        for k in range(max(int(0.2 * n), 20), int(0.7 * n)):
            for q in [7, 11, 17, 31]:
                A = BBPS(LEProblem(n, k, q), **bbps_params)
                t1 = A.time_complexity()
                t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

                if t1 == inf or t2 == inf:
                    continue

                assert t2 - ranges < t1 < t2 + ranges


beullens_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}
ranges = 3.


def test_beullens1():
    """
    special value test
    """
    n = 200
    k = 100
    for q in [11, 17, 31]:
        A = Beullens(LEProblem(n, k, q), **beullens_params)
        t1 = A.time_complexity()
        t2 = attack_cost(n, k, q) + log2(n)
        assert t2 - ranges < t1 < t2 + ranges


def test_beullens2():
    """
    small `n` test.
    """
    for n in range(50, 100, 3):
        for k in range(max(int(0.3 * n), 2), int(0.5 * n)):
            for q in [7, 11, 17, 31]:
                A = Beullens(LEProblem(n, k, q), **beullens_params)
                t1 = A.time_complexity()
                t2 = attack_cost(n, k, q) + log2(n)

                if t1 == inf or t2 == inf:
                    continue

                assert t2 - ranges < t1 < t2 + ranges

if __name__ == "__main__":
    test_beullens1()
    test_beullens2()
    test_bbps1()
    test_bbps2()
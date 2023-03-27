import random
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
from math import inf

load('tests/module/attack_cost.sage')
beullens_params = {"bit_complexities": 0}

ranges = 0.1


def test_beullens1():
    """
    special value test
    """
    n = 250
    k = 125
    for q in [11, 17, 31, 53]:
        A = Beullens(LEProblem(n, k, q), **beullens_params)
        t1=A.time_complexity()
        t2 = attack_cost(n, k, q) + log(n,2)
        assert t2 - ranges < t1 < t2 + ranges



def test_beullens2():
    """
    small `n` test.
    """
    for n in range(100, 103):
        for k in range(50, 53):
            for q in [7, 11]:
                A = Beullens(LEProblem(n, k, q), **beullens_params)
                B = Beullens(LEProblem(n, k, q), **beullens_params)
                t1 = min(A.time_complexity(),B.time_complexity())
                t21 = attack_cost(n, k, q)
                t22 = attack_cost(n, k, q)

                if t21 is None and t22 is None:
                    continue
                t2 = min(t21, t22)
                if t1 == inf or t2 == inf:
                    continue

                t2 += log(n,2)
                assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_beullens1()
    test_beullens2()
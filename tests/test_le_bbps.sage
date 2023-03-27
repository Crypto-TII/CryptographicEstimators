import random
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern


load('tests/module/cost.sage')
bbps_params = {"bit_complexities": 1, "sd_parameters": { "excluded_algorithms": [Prange, LeeBrickell]} }


def test_bbps1():
    """
    special value test
    """
    n = 200
    k = 100
    for q in [11, 17, 31]:
        ranges = 0.1
        if q == 11:
            # for such a small q we need to allow for a little more error range,
            # because the coupon collector is not exact enough
            ranges = 0.6

        A = BBPS(LEProblem(n, k, q), **bbps_params)
        t1 = A.time_complexity()
        t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

        if not (t2 - ranges< t1 < t2 + ranges):
            print(n, k, q, t1, t2)

        assert t2 - ranges < t1 < t2 + ranges


def test_bbps2():
    """
    generic test
    """
    ranges = 1.0
    #
    for n in range(100, 120):
        for k in range(max(int(0.2 * n), 20), int(0.7 * n)):
            for q in [7, 11, 17, 31]:
                A = BBPS(LEProblem(n, k, q), **bbps_params)
                t1 = A.time_complexity()
                t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

                if t1 == inf or t2 == inf:
                    continue

                assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_bbps1()
    test_bbps2()
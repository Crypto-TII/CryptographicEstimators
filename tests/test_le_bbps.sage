import random
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern

from math import inf
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
            # for small q we need to allow for a slightly larger tolerance,
            # because the coupon collector approximation is less accurate
            ranges = 0.6
        A = BBPS(LEProblem(n, k, q), **bbps_params)
        t1 = A.time_complexity()
        t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

        #if not (t2 - ranges< t1 < t2 + ranges):
        #    print(n, k, q, t1, t2)

        assert t2 - ranges < t1 < t2 + ranges


# We use an approximation of the coupon collector for efficiency reasons leading to small deviations for small instances
def correct_coupon_collector(L_prime,Nw_prime):
    if L_prime > Nw_prime - 1:
        L_prime= 2^L_prime
        Nw_prime=2^Nw_prime
        #      ____________________Approximation_________________   _________________Coupon Collector___________________________
        return (log2(L_prime)-log2(Nw_prime)+log2(log2(L_prime))) - log2(2*log(1.-L_prime/Nw_prime)/log(1.-1/Nw_prime)/Nw_prime)
    return 0


def test_bbps2():
    """
    generic test
    """
    ranges = 0.2


    for n in range(100, 120,5):
        for k in range(n//2,n//2+10,2):
            for q in [7, 11, 17, 31]:
                A = BBPS(LEProblem(n, k, q), **bbps_params)
                t1 = A.time_complexity()
                t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

                if t2 == 100000000000000:
                    continue

                verb = A._get_verbose_information()
                L,N= verb["L_prime"],verb["Nw_prime"]

                t2 += correct_coupon_collector(L,N)
                assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_bbps1()
    test_bbps2()

from cryptographic_estimators.SDFqEstimator import SDFqEstimator
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem
from math import  floor, log2, ceil, comb, comb as binomial, log2 as log


load('tests/module/attack_cost.sage')
load('tests/module/cost.sage')


# global parameters
params = {"bit_complexities": 0, "is_syndrome_zero": True, "nsolutions": 0}
stern_params = {"bit_complexities": 1, "is_syndrome_zero": True, "nsolutions": 0}

# correction term due to correction of the LeeBrickell procedure, see SDFqAlgorithms/leebrickell.py line 98/99
def lee_brickell_correction(k):
    return log(k, 2)*2 - log(binomial(k, 2), 2)


def test_sdfq_LeeBrickell():
    """
    special value test for Lee-Brickell
    """
    # we need to subtract the difference of lee brickell
    # and p = 1, because p = 2 is not always optimial
    ranges = 0.01
    n, k, w, q = 256, 128, 64, 251
    t1 = log(ISD_COST(n, k, w, q), 2) + log(n,2) - lee_brickell_correction(k)
    A = LeeBrickell(SDFqProblem(n, k, w, q, **params), **params)
    t2 = A.time_complexity(p=2)
    assert(t1 - ranges < t2 < t1 + ranges)

    n, k, w, q = 961, 771, 48, 31
    t1 = log(ISD_COST(n, k, w, q), 2) + log(n,2) - lee_brickell_correction(k)
    A = LeeBrickell(SDFqProblem(n, k, w, q, **params), **params)
    t2 = A.time_complexity(**{"p": 2})
    assert(t1 - ranges < t2 < t1 + ranges)


def test_sdfq_stern():
    """
    special value test for Stern
    """
    ranges = 0.01
    n, k, w, q = 256, 128, 64, 251
    t, p, l = peters_isd(n, k, q, w)
    t1 = Stern(SDFqProblem(n, k, w, q, **stern_params), **stern_params).time_complexity()
    assert(t - ranges < t1 < t + ranges)

    n, k, w, q = 961, 771, 48,31
    t, p, l = peters_isd(n, k, q, w)

    assert(t - ranges < Stern(SDFqProblem(n, k, w, q, **stern_params), **stern_params).time_complexity() < t + ranges)


def test_sdfq_stern_range():
    """
    range test for Stern
    """
    ranges = 0.05

    for n in range(50, 70, 5):
        for k in range(20, 40, 2):
            for w in range(4, min(n - k - 1, int(0.5 * n))):
                for q in [7, 11, 17, 53, 103, 151, 199, 251]:
                    A=Stern(SDFqProblem(n, k, w, q, **stern_params), **stern_params)
                    # peters_isd comparison code restricts l to this range
                    A.set_parameter_ranges("l", 1, n-k)
                    t1 = A.time_complexity()
                    print(A.optimal_parameters())
                    t2, p, l = peters_isd(n, k, q, w)

                    print(n,k,q,w,t1,t2)
                    assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_sdfq_LeeBrickell()
    test_sdfq_stern()
    test_sdfq_stern_range()
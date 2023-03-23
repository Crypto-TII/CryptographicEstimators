from cryptographic_estimators.PKEstimator import PKProblem
from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP, SBC

load('tests/module/cost.sage')
load('tests/module/kmp_cost.sage')
load('tests/module/our_cost.sage')


# global parameters
params = {"nsolutions": 0}


def test_kmp():
    """
    special value test
    """
    n = 94
    m = 55
    q = 509
    ell = 1

    ranges = 2.
    t1 = KMP(PKProblem(n, m, q, ell)).time_complexity()
    _, _, _, _, _, t2 = kmp_cost_numerical(n, m, ell, q)
    t2 += log2(n)
    assert t1 - ranges <= t2 <= t1 + ranges

def test_sbc():
    """
    special value test
    """
    n = 94
    m = 55
    q = 509
    ell = 1

    ranges = 2.
    A = SBC(PKProblem(n, m, q, ell))
    t1 = A.time_complexity()
    _, _, _, _, _, t2 = compute_new_cost(n, m, q, ell)
    t2 += log2(n)
    assert t1 - ranges <= t2 <= t1 + ranges


def test_kmp_range():
    """
    small value test
    """
    ranges = 3.

    for n in range(30, 100):
        for m in range(int(0.3 * n), int(0.7 * n)):
            for ell in range(1, 2):
                for q in [7, 11, 17, 53, 103, 151, 199, 251]:
                    if q^ell < n:
                        continue
                    t1 = KMP(PKProblem(n, m, q, ell)).time_complexity()
                    _, _, _, _, _, t2 = kmp_cost_numerical(n, m, ell, q)
                    t2 += log2(n)

                    print(n, m, q, ell, t1, t2)
                    assert t2 - ranges < t1 < t2 + ranges


def test_sbc_range():
    """
    small value test
    """
    ranges = 3.

    for n in range(30, 100):
        for m in range(int(0.3 * n), int(0.7 * n)):
            for ell in range(1, 2):
                for q in [7, 11, 17, 53, 103, 151, 199, 251]:
                    if q^ell < n:
                        continue
                    t1 = SBC(PKProblem(n, m, q, ell)).time_complexity()
                    _, _, _, _, _, t2 = compute_new_cost(n, m, q, ell)
                    t2 += log2(n)

                    print(n, m, q, ell, t1, t2)
                    assert t2 - ranges < t1 < t2 + ranges


if __name__ == "__main__":
    test_kmp_range()
    test_sbc_range()
    test_kmp()
    test_sbc()
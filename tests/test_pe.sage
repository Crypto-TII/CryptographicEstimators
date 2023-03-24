from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon, Beullens
from cryptographic_estimators.PEEstimator import PEProblem
from cryptographic_estimators.PEEstimator.pe_helper import number_of_weight_d_codewords, gv_distance


load('tests/module/attack_cost.sage')
load('tests/module/cost.sage')

# global parameters
leon_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]}}


def lee_brickell_correction(k):
    return log(k, 2)*2 - log(binomial(k, 2), 2)


def test_leon1():
    """
    test some hardcoded values taken from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py 
    """
    # we allow a difference of 1.02, because we account for 1 bit difference which comes from the different way
    # Lee
    n, k, q = 250, 125, 53
    ranges = 0.01
    t1 = LEON(n, k, q) + log(n, 2)

    A = Leon(PEProblem(n, k, q), **leon_params)
    t2 = A.time_complexity() + lee_brickell_correction(k)
    assert t1 - ranges <= t2 <= t1 + ranges

    n, k, q = 106, 45, 7
    t1 = LEON(n, k, q) + log(n, 2)
    t2 = Leon(PEProblem(n, k, q), **leon_params).time_complexity() + lee_brickell_correction(k)
    assert t1 - ranges <= t2 <= t1 + ranges


def test_leon2():
    """
    test some hardcoded values from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """
    ranges = 1.
    n, k= 250, 150
    q_values = [11, 17, 53, 103, 151, 199, 251]
    for q in q_values:
        t1 = LEON(n, k, q) + log2(n)
        t2 = Leon(PEProblem(n, k, q), **leon_params).time_complexity() + lee_brickell_correction(k)
        assert t1 - ranges <= t2 <= t1 + ranges


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


def test_beullens():
    """
    test some hardcoded values taken from:
       https://github.com/WardBeullens/LESS_Attack/blob/master/attack_cost.py
    """
    # we allow a difference of 1.02, because we account for 1 bit difference which comes from the different way
    # Lee
    n, k, q = 250, 125, 53
    ranges = 0.01
    ts = []
    ts2 = []
    for i in range(10):
        ts.append(attack_cost(n, k, q, False, False) + log(n, 2) - lee_brickell_correction(k))
        A = Beullens(PEProblem(n, k, q), **leon_params)
        ts2.append(A.time_complexity())
    t1 = min(ts)
    t2 = min(ts2)
    print(t2, t1, A.optimal_parameters())
    assert t1 - ranges <= t2 <= t1 + ranges

    # TODO
    n, k, q = 106, 45, 7
    ts = []
    ts2 = []
    for i in range(10):
        ts.append(attack_cost(n, k, q, False, False) + log(n, 2) - lee_brickell_correction(k))
        A = Beullens(PEProblem(n, k, q), **leon_params)
        ts2.append(A.time_complexity())
    t1 = min(ts)
    t2 = min(ts2)
    print(t2, t1, A.optimal_parameters())
    assert t1 - ranges <= t2 <= t1 + ranges



if __name__ == "__main__":
    test_beullens()
    test_leon1()
    test_leon2()
    test_leon()

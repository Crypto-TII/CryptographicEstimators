from math import comb, ceil, log2, log
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
from cryptographic_estimators.PEEstimator import PEProblem
from cryptographic_estimators.PEEstimator.pe_helper import number_of_weight_d_codewords, gv_distance

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
    # print(w, N, log2(c_isd), "LEON")
    return log2(S)

def test_leon():
    n, k, q = 100, 50, 3
    n, k, q = 250, 125, 53
    ranges = 2.
    params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]} }
    t1 = Leon(PEProblem(n, k, q), **params).time_complexity()
    t2 = LEON(n, k, q)
    #print(t1, t2)
    #exit(1)
    for n in range(10, 100, 5):
        for k in range(int(0.3*n), int(0.7*n), 5):
            for q in [3, 7, 17, 31]:
                t1 = Leon(PEProblem(n, k, q), **params).time_complexity()
                t2 = LEON(n, k, q)

                assert t2 - ranges < t1 < t2 + ranges
                #if not (t2 - 0.5 < t1 < t2 + 0.5):
                #    print(n, k, q, t1, t2)


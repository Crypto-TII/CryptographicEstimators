from math import comb as binomial, log2, factorial
from random import randint


def gv_distance(n: int, k: int, q: int):
    """
    Gilbert Varsharmov bound
    """
    d = 1
    right_term = q ** (n - k)
    left_term = 0
    while left_term <= right_term:
        left_term += binomial(n, d) * (q - 1) ** d
        d += 1
    d = d - 1
    return d


def number_of_weight_d_codewords(n: int, k: int, q: int, d: int):
    """
    Returns the number of weight d code words in a (n,k,q) code
    """
    return binomial(n, d) * (q - 1) ** (d - 2) * q ** (k - n + 1) * 1.


def random_sparse_vec_orbit(n: int, w: int, q: int):
    """

    """
    counts = [0] * (q - 1)
    s = 0
    while s < w:
        a = randint(0, q - 2)
        s += 1
        counts[a] += 1
    orbit_size = factorial(n) // factorial(n - w);
    for c in counts:
        orbit_size //= factorial(c)
    return log2(orbit_size)


def median_size_of_random_orbit(n: int, w: int, q: int):
    """

    """
    S = []
    for x in range(100):
        S.append(random_sparse_vec_orbit(n, w, q))
    S.sort()
    return S[49]


def hamming_ball(n: int, q: int, w: int):
    """

    """
    S = 0
    for i in range(0, w + 1):
        S += binomial(n, i) * (q - 1) ** i
    return log2(S)


def isd_cost(n, k, q, w):
    """

    """
    if n-k<w-2:
        return 100000
    return log2((k * k + k * k * q) * binomial(n, w) // binomial(n - k, w - 2) // binomial(k, 2))

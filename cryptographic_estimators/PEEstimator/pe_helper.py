from math import comb as binomial, log2


def gv_distance(n, k, q):
    d = 1
    right_term = q ** (n - k)
    left_term = 0
    while left_term <= right_term:
        left_term += binomial(n, d) * (q - 1) ** d
        d += 1
    d = d - 1
    return d


def number_of_weight_d_codewords(n, k, q, d):
    return binomial(n, d) * (q - 1) ** (d - 2) * q ** (k - n + 1) * 1.


def isd_cost(n, k, q,w):
    return log2(n*(k * k + k * k * q) * binomial(n, w) // binomial(n - k, w - 2) // binomial(k, 2))
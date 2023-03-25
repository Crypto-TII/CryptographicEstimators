from math import log2, inf, \
    comb as binomial


def cost_to_find_random_2dim_subcodes_with_support_w(n: int, k: int, w: int):
    """
    returns the cost of finding a 2 dimensional subcode in a code of length n and dimension k and support w
    """
    if n-k<w-2:
        return inf
    return log2((k * k + binomial(k, 2))) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2))
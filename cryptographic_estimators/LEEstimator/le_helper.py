from math import log2, comb as binomial


def cost_to_find_random_2dim_subcodes_with_support_w(n, k, w):
    return log2((k * k + binomial(k, 2))) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2))

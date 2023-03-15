from math import log2, comb as binomial, factorial


def gauss_binomial(m: int, r: int, q: int):
    """

    """
    return log2(q) * (r * (m - r))


def beullens_lee_brickell_adaptation(q: int, n: int, k: int, d: int, w: int, Nw: int):
    """

    """
    if w<d or n-w<k-d:
        return 1000
    iterations = log2(binomial(n, k)) - log2(binomial(w, d)) - log2(binomial(n - w, k - d))
    c_iter = k ** 3 + binomial(k, d)

    return log2(c_iter) + iterations - Nw


def lof(x: float):
    """

    """
    return log2(factorial(x))

def cost_for_finding_subcode(q: int, n: int, k: int, d: int, w: int, Nw: int):
    """

    """
    c_isd = beullens_lee_brickell_adaptation(q, n, k, d, w, Nw)
    return max(0, c_isd)

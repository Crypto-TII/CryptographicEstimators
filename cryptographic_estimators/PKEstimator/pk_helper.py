from math import log2, comb as binomial, factorial, inf


def gauss_binomial(m: int, r: int, q: int):
    return log2(q) * (r * (m - r))


def beullens_lee_brickell_adaptation(n: int, k: int, d: int, w: int, Nw: int):
    """
    Running time of Beullens LeeBrickel adaptation for finding d-dimensional subcode with support w
    """
    if w < d or n-w < k-d:
        return inf
    iterations = log2(binomial(n, k)) - log2(binomial(w, d)) - log2(binomial(n - w, k - d))
    c_iter = k ** 3 + binomial(k, d)

    return log2(c_iter) + iterations - Nw


def lof(x: int):
    return log2(factorial(x))

def cost_for_finding_subcode(n: int, k: int, d: int, w: int, Nw: int):
    """
    Compute cost for computation of d-dimensional subcode with support w where there exist Nw of them
    """
    c_isd = beullens_lee_brickell_adaptation(n, k, d, w, Nw)
    return max(0, c_isd)

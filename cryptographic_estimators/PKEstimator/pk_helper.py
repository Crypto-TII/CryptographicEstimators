from math import log2, comb as binomial


def gauss_binomial(m, r, q):
    return log2(q) * (r * (m - r))


def beullens_lee_brickell_adaptation(q, n, k, d, w, Nw):
    if w < d or n - w < k - d:
        return 1000
    iterations = log2(binomial(n, k)) - log2(binomial(w, d)) - log2(binomial(n - w, k - d))
    c_iter = k ** 3 + binomial(k, d)

    return log2(c_iter) + iterations - Nw


def cost_for_finding_subcode(q, n, k, d, w, Nw):
    c_isd = beullens_lee_brickell_adaptation(q, n, k, d, w, Nw)
    return max(0, c_isd)

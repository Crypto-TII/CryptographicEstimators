from math import log2, floor, comb as binomial, inf
from sage.rings.real_mpfr import RealField
from sage.rings.integer import Integer

RT = RealField(1000000)


def gauss_binomial(m, r, q):
    x = RT(1)
    for i in range(r):
        x = x * (1. - q ** (m - i * 1.)) / (1. - q ** (1. + i))

    return x


def peters_isd(q, n, k, w):
    x = floor(k / 2)

    log2q = log2(q)
    mincost = 10000000
    bestp = 0
    bestl = 0
    for p in range(1, 11):
        Anum = binomial(x, p)
        Bnum = binomial(k - x, p)
        # for(l=1,floor(log(Anum)/log(q)+p*log(q-1)/log(q))+10,\
        for l in range(1, floor(log2(Anum) / log2(q) + p * log2(q - 1) / log2(q)) + 10 + 1):
            # if(q==2):
            ops = 0.5 * (n - k) ** 2 * (n + k) + ((0.5 * k - p + 1) + (Anum + Bnum) * (q - 1) ** p) * l + q / (
                        q - 1.) * (
                          w - 2 * p + 1) * 2 * p * (1 + (q - 2) / (q - 1.)) * Anum * Bnum * (q - 1) ** (2 * p) / q ** l
            # ops=(n-k)**2*(n+k)\
            #     + ((0.5*k-p+1)+(Anum+Bnum)*(q-1)**p)*l\
            #     + q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*\
            #       Anum*Bnum*(q-1)**(2*p)/q**l

            prob = Anum * Bnum * binomial(n - k - l, w - 2 * p) / binomial(n, w)
            if prob == 0:
                return inf
            cost = log2(ops) + log2(log2q) - log2(prob)
            if cost < mincost:
                mincost = cost
                bestp = p
                bestl = l

    return mincost


def beullens_lee_brickell_adaptation(q, n, k, d, w, Nw):
    if w<d or n-w<k-d:
        return inf
    iterations = log2(binomial(n, k)) - log2(binomial(w, d)) - log2(binomial(n - w, k - d))
    c_iter = k ** 3 + binomial(k, d)

    return log2(c_iter) + iterations


def cost_for_finding_subcode(q, n, k, d, w, Nw):
    if d == 1:
        c_isd = peters_isd(q, n, k, w)  # TODO: exchange with call to our SDEstimator
    else:

        c_isd = beullens_lee_brickell_adaptation(q, n, k, d, w, Nw)

    return max(0, c_isd)

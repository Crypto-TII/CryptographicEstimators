import random
from math import comb, comb as binomial, ceil, log2, log, factorial, sqrt, inf, floor
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern


def peters_isd(n: int, k: int, q: int, w: int):
    x = k//2
    log2q = log2(q)
    mincost = 10000000
    bestp=0
    bestl=0
    max_p = max(w//2, 1)
    for p in range(0, max_p):
        Anum=max(binomial(x,p), 1)
        Bnum=max(binomial(k-x,p), 1)
        limit = min(floor(log(Anum)/log(q)+p*log(q-1)/log(q))+10 +1, n-k)
        for l in range(0, limit):
            if l > n-k-(w-2*p):
                continue
            ops=0.5*(n-k)**2*(n+k)+ ((0.5*k-p+1)+(Anum+Bnum)*(q-1)**p)*l+ q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*Anum*Bnum*(q-1)**(2*p)/q**l

            prob=log2(binomial(n,w)) - (log2(Anum)+log2(Bnum)+log2(binomial(n-k-l,w-2*p)))
            cost=log2(ops)+log2(log2q)+prob
            if cost<mincost:
                mincost=cost
                bestp=p
                bestl=l

    return mincost, bestp, bestl


def ISD_COST(n: int, k: int, w: int, q: int):
    return log2((k * k + k * k * q)) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(
        binomial(k, 2)) + log2(k) + log2(log(q))


def gv_distance(n, k, q):
    ##Gilbert - Varshamov distance of a code over Fq, with length n and dimension k
    ##Nw is the number of codewords with weight d (not considering scalar multiples)
    d = 1
    right_term = q**(n - k)
    left_term = 0
    while left_term <= right_term:
        left_term += binomial(n, d) * (q - 1)**d
        d += 1
    d = d - 1

    Nw = binomial(n, d) * (q - 1)**(d - 2) * q**(k - n + 1)

    return d, Nw


def improved_linear_beullens(n, k, q):
    w_in, Nw = gv_distance(n, k, q)

    max_w = n - k + 2

    best_cost = inf
    best_w = 0
    best_L_prime = 0
    best_w_prime = 0

    for w_prime in range(w_in, max_w):
        Nw_prime = binomial(n, w_prime) * (q - 1)**(w_prime - 1) * (q**k - 1) / (q**n - 1)

        for w in range(w_prime + 1, min(2 * w_prime, n)):
            pr_w_w_prime = binomial(w_prime, 2 * w_prime - w) * binomial(n - w_prime, w - w_prime) / binomial(n, w_prime)
            # zeta probability in the paper

            L_prime = (2 * Nw_prime**2 / (pr_w_w_prime) * (2 * log(n * 1.)))**0.25
            if L_prime < Nw_prime:
                x = 2 * w_prime - w
                pw = 0.5 * binomial(n, w - w_prime) * binomial(n - (w - w_prime), w - w_prime) * binomial(
                    n - 2 * (w - w_prime), 2 * w_prime - w) * factorial(2 * w_prime - w) * (q - 1)**(w - 2 * w_prime + 1) / (
                                 binomial(n, w_prime) * binomial(n - w_prime, w - w_prime) * binomial(w_prime,
                                                                                                      2 * w_prime - w))

                M_second = pr_w_w_prime * L_prime**4 / 4 * pw * (pr_w_w_prime - 2 / (Nw_prime**2))

                if M_second < 1:

                    C_isd, p, l = peters_isd(n, k, q, w_prime)
                    # cost = C_isd+log2(2*log(1.-L_prime/Nw_prime)/log(1.-1/Nw_prime)/Nw_prime);
                    # cost = C_isd+ log2(L_prime/Nw_prime);

                    if L_prime < Nw_prime / 2:
                        cost = C_isd + log2(L_prime / Nw_prime)
                    else:
                        Nw_prime = float(Nw_prime)
                        tmp = 1. - 1. / Nw_prime
                        if tmp == 1.0:
                            tmp = 0.9999
                        tmp = log(tmp)
                        cost = C_isd + log2(2 * log(1. - L_prime / Nw_prime) / tmp / Nw_prime)

                    if cost < best_cost:
                        best_cost = cost
                        best_w = w
                        best_w_prime = w_prime
                        best_L_prime = L_prime

    return best_cost, best_w, best_w_prime, best_L_prime


def random_sparse_vec_orbit(n,w,q):
    counts = [0]*(q-1)
    s = 0
    while s<w:
        a = random.randint(0,q-2)
        s += 1
        counts[a] += 1
    Orbit_size = factorial(n)//factorial(n-w);
    for c in counts:
        Orbit_size //= factorial(c)
    return Orbit_size


def median_size(n,w,q):
    S = []
    for x in range(100):
        S.append(random_sparse_vec_orbit(n,w,q))
    S.sort()
    return S[49]


def orbit_size(n,w,q,LEP=True):
    if LEP == False:
        return median_size(n,w,q)
    if LEP == True:
        return median_size(n, w, q) * ((q - 1) ** (w - 1))


def Hamming_Ball(n, q, w):
    S = 0
    for i in range(0, w + 1):
        S += binomial(n, i) * (q - 1) ** i
    return int(S)


def beullens_attack_cost_fixed_W(n, k, W, q, verbose=True, LEP=True):
    if LEP == False:  # number of vectors of weight W
        search_space_size = Hamming_Ball(n, q, W) // int(q ** (n - k)) // (q - 1)
    else:  # number of 2*spaces with support of size W
        search_space_size = (binomial(n, W) * int(q ** (2 * (W - 2)))) // int(q ** (2 * (n - k)))

    if search_space_size < 1:
        if verbose:
            print("no sparse vectors/spaces")
        return None

    size_of_orbit = orbit_size(n, W, q, LEP)

    if (LEP == False and size_of_orbit > q ** (n - k) // ceil(4 * log(n, 2))) or (
            LEP == True and size_of_orbit > q ** (2 * (n - k)) // ceil(4 * log(n, 2))):
        if verbose:
            print("Orbit too big")
        return None

    list_size = sqrt(search_space_size * 2 * log(n, 2))

    # number of gaussian eliminations
    GEs = 2 * (binomial(n, W) / binomial(n - k, W - 2) / binomial(k, 2) / search_space_size) * list_size

    # number of row operations
    if LEP == False:
        ISD_cost = (k ** 2 + k * k * q) * GEs
    else:
        ISD_cost = (k * k + binomial(k, 2)) * GEs

    if LEP == False:
        Normal_form_cost = 2 * list_size
    else:
        Normal_form_cost = 2 * q * list_size

    attack_cost = ISD_cost + Normal_form_cost

    if verbose:
        print("new attack cost (log_2 of #row ops): %f, list size: %d (2^%f), (w = %d)" % (
            log(attack_cost, 2), list_size, log(list_size, 2), W))

    return log(attack_cost, 2)


def beullens_attack_cost(n, k, q, verbose=False, LEP=True):
    best_cost = 10000000
    best_W = None

    for W in range(1, n - k + 1):
        c = beullens_attack_cost_fixed_W(n, k, W, q, False, LEP)
        if c is not None and c < best_cost:
            best_cost = c
            best_W = W

    if best_cost == 10000000:
        return None

    if verbose:
        beullens_attack_cost_fixed_W(n, k, best_W, q, True, LEP)
    return best_cost + log2(n)


bbps_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}
ranges = 3.


def test_bbps1():
    """
    special value test
    """
    n = 200
    k = 100
    for q in [11, 17, 31]:
        A = BBPS(LEProblem(n, k, q), **bbps_params)
        t1 = A.time_complexity()
        t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)
        if not (t2 - ranges< t1 < t2 + ranges):
            print(n, k, q, t1, t2)


def test_bbps2():
    """
    generic test
    """
    for n in range(100, 120):
        for k in range(max(int(0.2 * n), 20), int(0.7 * n)):
            for q in [7, 11, 17, 31]:
                A = BBPS(LEProblem(n, k, q), **bbps_params)
                t1 = A.time_complexity()
                t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)

                if t1 == inf or t2 == inf:
                    continue

                assert t2 - ranges < t1 < t2 + ranges


beullens_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}
ranges = 3.


def test_beullens1():
    """
    special value test
    """
    n = 200
    k = 100
    for q in [11, 17, 31]:
        A = Beullens(LEProblem(n, k, q), **beullens_params)
        t1 = A.time_complexity()
        t2 = beullens_attack_cost(n, k, q)
        assert t2 - ranges < t1 < t2 + ranges


def test_beullens2():
    """
    small `n` test.
    """
    for n in range(50, 100, 3):
        for k in range(max(int(0.3 * n), 2), int(0.5 * n)):
            for q in [7, 11, 17, 31]:
                A = Beullens(LEProblem(n, k, q), **beullens_params)
                t1 = A.time_complexity()
                t2 = beullens_attack_cost(n, k, q)

                if t1 == inf or t2 == inf:
                    continue

                assert t2 - ranges < t1 < t2 + ranges
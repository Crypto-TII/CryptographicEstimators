from cryptographic_estimators.PKEstimator import PKEstimator
A = PKEstimator(n=100,m=50,q=31,ell=2)
A.table()
exit(1)

#from cryptographic_estimators.SDEstimator import SDEstimator
#from cryptographic_estimators.SDEstimator.SDAlgorithms import *
#A = SDEstimator(16386, 16386 // 2, 128, doom=16386//2, excluded_algorithms=[BJMMdw, BJMMpdw, MayOzerov, BJMMd3, BallCollision, BothMay])
#A.table(precision=3, show_all_parameters=1)
#A = SDEstimator(16386, 16386 // 2, 128, excluded_algorithms=[BJMMdw, BJMMpdw, MayOzerov, BJMMd3, BallCollision, BothMay])
#A.table(precision=3, show_all_parameters=1)
#from cryptographic_estimators.SDEstimator import SDEstimator
#from cryptographic_estimators.SDEstimator.SDAlgorithms import *
#A = SDEstimator(16386, 16386 // 2, 128, qc=True, excluded_algorithms=[BJMMdw, BJMMpdw, MayOzerov, BothMay, BallCollision])
#A.table(precision=3, show_all_parameters=1)
#exit()


#from math import comb, ceil, log2, log
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern
#from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
#from cryptographic_estimators.PEEstimator import PEProblem
from cryptographic_estimators.PEEstimator.pe_helper import number_of_weight_d_codewords, gv_distance


leon_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]}}


def minimal_w(n: int, k: int, q: int):
    w = 1
    S = 0
    limit = min(100, int(number_of_weight_d_codewords(n, k, q, gv_distance(n, k, q) + 2)))
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
    print(w, N, log2(c_isd), "LEON")
    return log2(S)


#def test_leon():
#    n, k, q = 100, 50, 3
#    n, k, q = 250, 125, 53
#    ranges = 4.5
#    t1 = Leon(PEProblem(n, k, q), **leon_params).time_complexity()
#    t2 = LEON(n, k, q)
#    for n in range(10, 100, 1):
#        for k in range(int(0.3*n), int(0.7*n), 1):
#            for q in [3, 7, 17, 31]:
#                if q > n:
#                    continue
#                t1 = Leon(PEProblem(n, k, q), **leon_params).time_complexity()
#                t2 = LEON(n, k, q)
#
#                #assert t2 - ranges < t1 < t2 + ranges
#                if not (t2 - ranges < t1 < t2 + ranges):
#                    print(n, k, q, t1, t2)
#
#
#test_leon()
#exit(1)

#from cryptographic_estimators.SDFqEstimator import SDFqEstimator
#from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
#from cryptographic_estimators.SDFqEstimator import SDFqProblem
from math import  floor, log2, ceil, comb, comb as binomial, log2 as log, inf

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
        #print(n,k,q,w,p,Anum)
        limit = min(floor(log(Anum)/log(q)+p*log(q-1)/log(q))+10 +1, n-k)
        for l in range(0, limit):
            if l > n-k-(w-2*p):
                continue
            #if(q==2):
            ops=0.5*(n-k)**2*(n+k)+ ((0.5*k-p+1)+(Anum+Bnum)*(q-1)**p)*l+ q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*Anum*Bnum*(q-1)**(2*p)/q**l
            #else:
            #    ops=(n-k)**2*(n+k)\
            #         + ((0.5*k-p+1)+(Anum+Bnum)*(q-1)**p)*l\
            #         + q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*\
            #           Anum*Bnum*(q-1)**(2*p)/q**l

            #prob=Anum*Bnum*binomial(n-k-l,w-2*p)/binomial(n,w)
            prob=log2(binomial(n,w)) - (log2(Anum)+log2(Bnum)+log2(binomial(n-k-l,w-2*p)))
            cost=log2(ops)+log2(log2q)+prob
            #print(p,l,cost, prob, log2(ops))
            if cost<mincost:
                mincost=cost
                bestp=p
                bestl=l

    #print("Given q=",q,", n=",n,", k=",k,", w=",w);
    #print("parameters p=",bestp, " and l=",bestl," yield 2^",mincost," bit ops");
    return mincost, bestp, bestl


def ISD_COST(n: int, k: int, w: int, q: int):
    return log2((k * k + k * k * q)) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(
        binomial(k, 2)) + log2(k) + log2(log(q))

#ranges = 1.
#n,k,w,q=961, 771, 48, 31
##n,k,w,q=20,5,14,13
#params = {"nsolutions": 0}
#A = LeeBrickell(SDFqProblem(n,k,w,q, **params))
#print(A.p(), A._get_verbose_information())
#t1 = A.time_complexity()
#t2 = ISD_COST(n,k,w,q)
#print(t1,t2)
#exit(1)
#
#for n in range(50, 100, 3):
#    for k in range(max(int(0.2 * n), 2), int(0.7 * n)):
#        for w in range(2, min(n-k-1, int(0.5 * n))):
#            for q in [3, 7, 11, 17, 53, 103, 151, 199, 251]:
#                t1 = LeeBrickell(SDFqProblem(n,k,w,q, **params)).time_complexity()
#                t2 = ISD_COST(n,k,w,q)
#
#                ##assert t2 - ranges < t1 < t2 + ranges
#                if not (t2 - ranges< t1 < t2 + ranges):
#                   print(n, k, w, q, t1, t2)
#                   exit(1)
#
#










#BBPS
import random
from math import comb, comb as binomial, ceil, log2, log, factorial, sqrt
from cryptographic_estimators.LEEstimator.LEAlgorithms import *
from cryptographic_estimators.LEEstimator import LEProblem
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import LeeBrickell, Prange, Stern


##Gilbert - Varshamov distance of a code over Fq, with length n and dimension k
##Nw is the number of codewords with weight d (not considering scalar multiples)
def _gv_distance(n, k, q):
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
    w_in, Nw = _gv_distance(n, k, q)

    max_w = n - k + 2

    best_cost = inf
    best_w = 0
    best_L_prime = 0
    best_w_prime = 0

    for w_prime in range(w_in, max_w):
        # print(w_prime);
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
                    #                    cost = C_isd+ log2(L_prime/Nw_prime);

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
                        #print(cost);
                        best_cost = cost
                        best_w = w
                        best_w_prime = w_prime
                        best_L_prime = L_prime

    return best_cost, best_w, best_w_prime, best_L_prime


bbps_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}
ranges = 3.

#n = 59
#k = 12
#q = 11
#A = BBPS(LEProblem(n, k, q), **bbps_params)
#t1 = A.time_complexity()
#t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)
#if not (t2 - ranges< t1 < t2 + ranges):
#    print(n, k, q, t1, t2)
#exit()

#for n in range(100, 110, 3):
#    for k in range(max(int(0.2 * n), 20), int(0.7 * n)):
#        for q in [7, 11, 17, 31]:
#            A = BBPS(LEProblem(n, k, q), **bbps_params)
#            t1 = A.time_complexity()
#            t2, w, w_prime, L_prime = improved_linear_beullens(n, k, q)
#
#            if t1 == inf and t2 == inf:
#                continue
#
#            if not (t2 - ranges < t1 < t2 + ranges):
#                print(n, k, q, t1, t2)
#                #print(A.w(), A.w_prime())
#                #print(w, w_prime, L_prime)


def gauss_binomial(m: int, r: int, q: int):
    x = 1;
    for i in range(r):
        x = x * (1 - q ^ (m - i)) / (1 - q ^ (i + 1));

    return x;


# Complexity of original Beullen's algorithm to solve linear equivalence
def linear_beullens(n: int, k: int, q: int):
    max_w = n - k + 2

    best_cost = inf
    best_w = 0
    best_L = 0
    best_Nw2 = 0

    w_in, Nw = gv_distance(n, k, q)

    for w in range(w_in, max_w):
        # Nw2 = binomial(n, w) * (q**2 - 1)**w * gauss_binomial(k, 2, q) / ((q**2 - q) * (q**2 - 1)) / gauss_binomial(n, 2, q)
        Nw2 = log2(binomial(n, w)) + log2((q**2 - 1)**w) + log2(gauss_binomial(k, 2, q)) - log2((q**2 - q) * (q**2 - 1)) - log2(gauss_binomial(n, 2, q))

        if Nw2 > 1:
            L = (Nw2 * ceil(n * (n - 1) / (2 * w * (n - w))))**0.5
            if L < Nw2:
                C_isd, p, l = peters_isd(n, k, q, w)

                # uncomment to consider Prange's ISD
                #                    C_isd = log2((n^3+binomial(k,2))/(binomial(w,2)*binomial(n-w,k-2)/binomial(n,k)))
                #cost = C_isd + log2(2 * log(1. - L / Nw2) / log(1. - 1 / Nw2) / Nw2)
                cost = C_isd + log2(L) - Nw2

                if cost < best_cost:
                    best_cost = cost
                    best_w = w
                    best_L = L
                    best_Nw2 = Nw2

    return best_cost, best_w, best_L, best_Nw2





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

    if LEP == False:  # number of row operations
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
            best_W = W;

    if best_cost == 10000000:
        return None

    if verbose:
        beullens_attack_cost_fixed_W(n, k, best_W, q, True, LEP)
    return best_cost + log2(n)




beullens_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, LeeBrickell]}}

n = 200
k = 100
for q in [11, 17, 31]:
    A = Beullens(LEProblem(n, k, q), **beullens_params)
    t1 = A.time_complexity()
    t2 = beullens_attack_cost(n, k, q)
    if not (t2 - ranges< t1 < t2 + ranges):
        print(n, k, q, t1, t2)
        print(A.w())


#for n in range(50, 100, 3):
#    for k in range(max(int(0.3 * n), 2), int(0.5 * n)):
#        for q in [7, 11, 17, 31]:
#            A = Beullens(LEProblem(n, k, q), **beullens_params)
#            t1 = A.time_complexity()
#            t2 = beullens_attack_cost(n, k, q)
#
#            if t1 == inf and t2 == inf:
#                continue
#
#            if not (t2 - ranges < t1 < t2 + ranges):
#                print(n, k, q, t1, t2)
#                #print(A.w(), A.w_prime())
#                #print(w, w_prime, L_prime)



#leon_params = {"bit_complexities": 0, "sd_parameters": {"excluded_algorithms": [Prange, Stern]}}
#def test_leon():
#    """
#    tests leon on small instances
#    """
#    ranges = 4.5
#    for n in range(50, 100, 5):
#        for k in range(int(0.3*n), int(0.7*n), 5):
#            for q in [7, 17, 31]:
#                A = Leon(LEProblem(n, k, q), **leon_params)
#                t1 = A.time_complexity()
#                t2 = LEON(n, k, q) + log2(n)
#
#                print(A.w(),  number_of_weight_d_codewords(n, k, q, A.w()))
#                assert t2 - ranges < t1 < t2 + ranges

#test_leon()

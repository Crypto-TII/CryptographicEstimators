from cryptographic_estimators.SDFqEstimator import SDFqEstimator
from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import *
from cryptographic_estimators.SDFqEstimator import SDFqProblem
from math import  floor, log2, ceil, comb, comb as binomial, log2 as log

# global parameters
params = {"nsolutions": 0}


def ISD_COST(n: int, k: int, w: int, q: int):
    """

    """
    return log2((k * k + k * k * q)) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2)) + log2(k) + log2(log(q))


def peters_isd(n: int, k: int, q: int, w: int):
    """

    """
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
    return mincost#, bestp, bestl


def test_sdfq_LeeBrickell():
    """
    special value test for Lee-Brickell
    """
    ranges = 1.0
    n, k, w, q = 256, 128, 128, 251
    t = ISD_COST(n, k, q, w)
    assert(t - ranges < LeeBrickell(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)

    n, k, w, q = 961, 771, 48, 31
    t = ISD_COST(n, k, q, w)
    assert(t - ranges < LeeBrickell(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)


def test_sdfq_stern():
    """
    special value test for Stern
    """
    ranges = 0.3
    n, k, w, q = 256, 128, 128, 251
    t = peters_isd(n, k, q, w)
    assert(t - ranges < Stern(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)

    n, k, w, q = 961,771, 48,31
    t = peters_isd(n, k, q, w)
    assert(t - ranges < Stern(SDFqProblem(n, k, w, q, **params)).time_complexity() < t + ranges)


def test_sdfq_stern_range():
    """
    range test for Stern
    """
    ranges = 5.

    for n in range(20, 100, 3):
        for k in range(int(0.2 * n), int(0.8 * n)):
            for w in range(1, min(n - k - 1, int(0.5 * n))):
                for q in [3, 7, 11, 17, 53, 103, 151, 199, 251]:
                    t1 = Stern(SDFqProblem(n, k, w, q, **params)).time_complexity()
                    t2 = peters_isd(n, k, q, w)
                    assert t2 - ranges < t1 < t2 + ranges



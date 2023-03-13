from math import log2, comb as binomial, floor,log


def cost_to_find_random_2dim_subcodes_with_support_w(n, k, w):
    return log2((k * k + binomial(k, 2))) + log2(binomial(n, w)) - log2(binomial(n - k, w - 2)) - log2(binomial(k, 2))


#todo remove once Fq SD estimator implemented
def peters_isd(n,k,q,w):


    x = floor(k/2)

    log2q=log2(q)
    mincost=10000000
    max_p = min(11,floor(k/2))
    for p in range(1,max_p):
        Anum=binomial(x,p)
        Bnum=binomial(k-x,p)
        for l in range(1,floor( log(Anum)/log(q)+p*log(q-1)/log(q))+10 +1):
            if (n - k - l < w - 2 * p):
                return 100000000
            ops=0.5*(n-k)**2*(n+k)+ ((0.5*k-p+1)+(Anum+Bnum)*(q-1)**p)*l+ q/(q-1.)*(w-2*p+1)*2*p*(1+(q-2)/(q-1.))*Anum*Bnum*(q-1)**(2*p)/q**l

            prob=log2(Anum)+log2(Bnum)+log2(binomial(n-k-l,w-2*p))-log2(binomial(n,w))
            cost=log2(ops)+log2(log2q)-prob
            if cost<mincost:
                mincost=cost

    cost=mincost

    return cost
#!/usr/bin/python3

import random
from math import factorial, log, sqrt, ceil
import math

def binomial(n,k):
    return factorial(n)//factorial(k)//factorial(n-k)

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
        return median_size(n,w,q)*((q-1)**(w-1))
    
def Hamming_Ball(n,q,w):
    S = 0
    # count all vectors with weight < \omega
    for i in range(0,w+1):
        S += binomial(n,i) * (q-1)**i
    return int(S)

def attack_cost_fixed_W(n,k,W,q,verbose=True,LEP=True):
    if LEP == False: # number of vectors of weight W
        search_space_size = Hamming_Ball(n,q,W)//int(q**(n-k))//(q-1)
    else: # number of 2*spaces with support of size W 
        search_space_size = (binomial(n,W) * int(q**(2*(W-2)))) // int(q**(2*(n-k))) 

    if search_space_size < 1:
        if verbose:
            print("no sparse vectors/spaces")
        return None 

    size_of_orbit = orbit_size(n,W,q,LEP)

    if (LEP == False and size_of_orbit > q**(n-k)//ceil(4*log(n,2))) or (LEP == True and size_of_orbit > q**(2*(n-k))//ceil(4*log(n,2))) :
            if verbose:
                print("Orbit too big")
            return None
    
    list_size = sqrt(search_space_size*2*log(n,2))

    #number of gaussian eliminations
    GEs = 2*(binomial(n,W)/binomial(n-k,W-2)/binomial(k,2)/search_space_size)*list_size

    if LEP == False: #number of row operations
        ISD_cost = (k**2 + k*k*q)*GEs
    else:
        ISD_cost = (k*k + binomial(k,2))*GEs
        
    if LEP == False:
        Normal_form_cost = 2*list_size
    else:
        Normal_form_cost = 2*q*list_size

    attack_cost = ISD_cost + Normal_form_cost
    
    if verbose:
        print("new attack cost (log_2 of #row ops): %f, list size: %d (2^%f), (w = %d)" % (log(attack_cost,2), list_size ,log(list_size,2),W))
    
    return log(attack_cost,2)


def attack_cost(n,k,q,verbose=False, LEP = True):
    best_cost = 10000000
    best_W = None
    
    for W in range(1,n-k+1):
        c = attack_cost_fixed_W(n,k,W,q,False,LEP)
        if c is not None and c < best_cost:
            best_cost = c
            best_W = W;
    
    if best_cost == 10000000:
        return None

    if verbose:
        attack_cost_fixed_W(n,k,best_W,q,True,LEP)
    return best_cost
    

def minimal_w(n,k,q):
    w = 1;
    S = 0
    while True:
        S += binomial(n,w)*(q-1)**(w-1)
        if S > 100*q**(n-k):
            return w, ceil(S/q**(n-k))
        w = w+1
    

def ISD_COST(n,k,w,q):
    #return (k*k + binomial(k,2)*q)*binomial(n,w)//binomial(n-k,w-2)//binomial(k,2)
    return (k*k + k*k*q)*binomial(n,w)//binomial(n-k,w-2)//binomial(k,2)


def LEON(n,k,q):
    w , N = minimal_w(n,k,q)
    S = ceil(2*(0.57+log(N)))*ISD_COST(n,k,w,q)
    
    # print("Leon attack cost (log_2 of #row ops):%f, w: %d, N: %d " % (log(S,2),w,N), n, k, q)
    return log(S,2);


#print("proposed LESS-I parameters: ")
#print(attack_cost(250,125,53))
#LEON(250,125,53)
#
#print("\noriginal LESS-II parameters: ")
#print(attack_cost(106,45,7))
#LEON(106,45,7)
#
#print("\nproposed LESS-III parameters (larger field size): ")
#print(attack_cost(280,117,149,LEP=False))
#LEON(280,117,149)
#
#print("\nproposed LESS-III parameters (fixed field size): ")
#print(attack_cost(305,127,31,LEP=False))
#LEON(305,127,31)

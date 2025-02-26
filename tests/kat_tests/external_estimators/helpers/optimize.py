#!/usr/bin/env python3

import argparse
import collections
import random
import scipy.optimize as opt
import random as rng
from math import comb as binom
from math import log2, log, ceil, inf

# AES encryptions: kB/s
AES = {"128": {"128": 16892817.80, "192": 14375882.78, "256": 12473219.60},
       "256": {"128": 17863577.85, "192": 15071777.05, "256": 12982587.16}}
McEliece_level1 = {"name": "McEliece C1", "n": 3488, "k": 2720, "w": 64}
McEliece_level3 = {"name": "McEliece C3", "n": 4608, "k": 3360, "w": 96}
McEliece_level5a = {"name": "McEliece C5a", "n": 6688, "k": 5024, "w": 128}
McEliece_level5b = {"name": "McEliece C5b", "n": 6960, "k": 5413, "w": 119}
McEliece_level5c = {"name": "McEliece C5c", "n": 8192, "k": 6528, "w": 128}

BIKE_level1 = {"name": "BIKE C1", "n": 24646, "k": 12323, "w": 134, "w_k": 142}
BIKE_level3 = {"name": "BIKE C3", "n": 49318, "k": 24659, "w": 199, "w_k": 206}
BIKE_level5 = {"name": "BIKE C5", "n": 81946, "k": 40973, "w": 264, "w_k": 274}

HQC_level1 = {"name": "HQC C1", "n": 35338, "k": 17669, "w": 132, "w_e": 75}
HQC_level3 = {"name": "HQC C3", "n": 71702, "k": 35851, "w": 200, "w_e": 114}
HQC_level5 = {"name": "HQC C5", "n": 115274, "k": 57637, "w": 262, "w_e": 149}

levels_qc = {"BIKEmsg": [[], [], []], "BIKEkey": [[], [], []],
             "HQC": [[], [], []]}
AES_GATE_COUNT_LEVEL = {128: 143, 192: 207, 256: 272}

NOLOG = False


def HHH(c):
    """
    binary entropy
    :param c: float in [0,1]
    """
    if c == 0. or c == 1.:
        return 0.
    if c < 0. or c > 1.:
        return -1000

    return -(c * log2(c) + (1 - c) * log2(1 - c))


def H(c):
    """
    binary entropy
    :param c: float in [0,1]
    """
    if c == 0. or c == 1.:
        return 0.

    if c < 0. or c > 1.:
        return -1000

    return -(c * log2(c) + (1 - c) * log2(1 - c))


def binomH(n, k):
    """
    binary entropy
    :param n: int
    :param k: int
    """
    if k > n:
        return 0
    if k == n:
        return 0
    return n * HHH(k/n)


def binomHH(n, k):
    """
    same as `binomH` without checks
    """
    return n * HHH(k/n)


def time7diss(x):
    """
    magic function for the 7-dissection
    """
    return -2*x/3+2/3


def time11diss(x):
    """
    magic function for the 11-dissection
    """
    return -5/4*x+3/4


def float_range(start, stop, step):
    """
    helper function. Same as `range` only for floats
    """
    while start < stop:
        yield float(start)
        start += float(step)


def check_constraints(constraints, solution):
    """
    checks wether constrains are fullfilled or not
    """
    return [(constraint['type'], constraint['fun'](solution))
            for constraint in constraints]


def wrap(f, g):
    """
    helper function injecting variables names into the optimisation process.
    """
    def inner(x):
        return f(g(*x))
    return inner


def round_to_str(t):
    """
    Rounds the value 't' to a string with 4 digit precision
    (adding trailing zeroes to emphasize precision).
    """
    s = str(round(t, 4))
    # must be 6 digits
    return (s + "0" * (5 + s.find(".") - len(s)))


def round_upwards_to_str(t):
    """
    Rounds the value 't' *upwards* to a string with 4 digit precision
    (adding trailing zeroes to emphasize precision).
    """
    s = str(ceil(t*10000)/10000)
    # must be 6 digits
    return (s + "0" * (5 + s.find(".") - len(s)))


def xlx(x):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    if x <= 0:
        return 0
    return x*log2(x)


def p_good(a0, b0, a1, b1):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    return -2*xlx(a0/2) - 2*xlx(b0/2) - xlx(a1-a0/2) - xlx(b1-b0/2) \
           - xlx(1-a1-b1-a0/2-b0/2) - 2*g(a1, b1)


def g(a, b):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    return -xlx(a) - xlx(b) - xlx(1-a-b)


def f(a, b, c):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    if a <= 0:
        return g(b, c)
    if b <= 0:
        return g(a, c)
    if c <= 0:
        return g(a, b)
    if a+b+c >= 1:
        return min(g(b, c), g(a, c), g(a, b))
    try:
        return -a*log(a, 2) - b*log(b, 2) - c*log(c, 2)\
                - (1-a-b-c)*log(1-a-b-c, 2)
    except:
        return 0.


def p_good_2(b0, a0, c0, b1, a1, c1):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    def proba(x):
        return 2*xlx(a0/2) + 2*xlx(x+a1-a0/2-b0/2) + xlx(1-c0-2*a1-2*x)\
                + 2*xlx(b0/2-x) + 2*xlx(x) + 2*xlx(x+c0/2-b1/2+a1/2-a0/4-b0/4)\
                + xlx(b1-a1+a0/2+b0/2-2*x)

    bounds = [(max(a0/2+b0/2-a1, 0, b1/2-a1/2+a0/4+b0/4-c0/2),
               min(1/2.-c0/2-a1, b0/2, b1/2-a1/2+a0/4+b0/4))]
    if bounds[0][0] > bounds[0][1]:
        return p_good(b0, a0, b1, a1) - 1
    return - opt.fminbound(proba, bounds[0][0], bounds[0][1], xtol=1e-15,
                           full_output=1)[1] - 2*f(a1, b1, c1)


def p_good_2_aux(b0, a0, c0, b1, a1, c1):
    """
    SOURCE: https://github.com/xbonnetain/optimization-subset-sum
    """
    return -(2*xlx(a1-c1) + xlx(1-2*c1-2*b1) + 2*xlx(c1) + 2*xlx(b0/2-c1))\
            - 2*f(a1, b1, c1)


def H1(value):
    """
    inverse of the bin entropy function. Inverse only on [0,1] -> [0, 1/2]
    """
    if value == 1.0:
        return 0.5

    # approximate inverse binary entropy function
    steps = [0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001,
             0.00000001, 0.0000000001, 0.0000000000001, 0.000000000000001]
    r = 0.000000000000000000000000000000001

    for step in steps:
        i = r
        while (i + step < 1.0) and (H(i) < value):
            i += step

        r = i - step

    return r


def Hi(value):
    """
    puhhhh
    """
    return H1(value)


###############################################################################
#######################Adapted estimator functions#############################
###############################################################################
def _list_merge_async_complexity(L1, L2, l, hmap):
    """
    Complexity estimate of merging two lists exact

    INPUT:

    - ``L`` -- size of lists to be merged
    - ``l`` -- amount of bits used for matching
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)
    """

    if L1 == 1 and L2== 1:
        return 1
    if L1 == 1:
        return L2
    if L2 == 1:
        return L1
    if not hmap:
        return 0 #to be implemented
    else:
        return L1+L2 + L1*L2 // 2 ** l


def _list_merge_complexity(L, l, hmap):
    """
    Complexity estimate of merging two lists exact
    INPUT:
    - ``L`` -- size of lists to be merged
    - ``l`` -- amount of bits used for matching
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)
    """

    if L == 1:
        return 1
    if not hmap:
        return max(1, 2 * int(log2(L)) * L + L ** 2 // 2 ** l)
    else:
        return 2 * L + L ** 2 // 2 ** l


def _gaussian_elimination_complexity(n, k, r):
    """
    Complexity estimate of Gaussian elimination routine
    INPUT:
    - ``n`` -- Row additons are perfomed on ``n`` coordinates
    - ``k`` -- Matrix consists of ``n-k`` rows
    - ``r`` -- Blocksize of method of the four russian for inversion, default
                is zero
    [Bar07]_ Bard, G.V.: Algorithms for solving linear and polynomial systems
    of equations over finite fields
    with applications to cryptanalysis. Ph.D. thesis (2007)
    [BLP08] Bernstein, D.J., Lange, T., Peters, C.: Attacking and defending the
    mceliece cryptosystem.
    In: International Workshop on Post-Quantum Cryptography. pp. 31–46.
    Springer (2008)
    """

    if r != 0:
        return (r ** 2 + 2 ** r + (n - k - r)) * int(((n + r - 1) / r))

    return (n - k) ** 2


def _optimize_m4ri(n, k, mem=inf):
    """
    Find optimal blocksize for Gaussian elimination via M4RI
    INPUT:
    - ``n`` -- Row additons are perfomed on ``n`` coordinates
    - ``k`` -- Matrix consists of ``n-k`` rows
    """

    (r, v) = (0, inf)
    for i in range(n - k):
        tmp = log2(_gaussian_elimination_complexity(n, k, i))
        if v > tmp and r < mem:
            r = i
            v = tmp
    return r


def _mem_matrix(n, k, r):
    """
    Memory usage of parity check matrix in vector space elements
    INPUT:
    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``r`` -- block size of M4RI procedure
    """
    return n - k + 2 ** r


###############################################################################
##################################BCJ##########################################
###############################################################################

def optimize_bcj(new=True, only_diss=False, verb=True, membound=1.,
                 iters=10000):
    """
    Optimization target: original BCJ algorithm for subset-sum, using {0,-1,1}
    representations
    with a 4-level merging tree.

    :param new: if set to true the new version of `BCJ` will be optimizes
                if false, the original version.
    :param only_diss: if set to `true` the optimization will take the 7/11
                    dissection into account but not the tree repetitions.
    :param verb: verbose output
    :param membound: set the maximal memory the optimisation should use
                    value between [0,1]
    """
    set_bcj = collections.namedtuple('bcj', 'l1 l2 l3 L1 L2 L3 L4 '
                                     'alpha1 alpha2 alpha3 r1 r2 r3')

    if new and only_diss:
        print("BCJ specify only the new algorithm or only dissection")
        return

    def bcj(f):
        return wrap(f, set_bcj)

    def g(a, b):
        return -xlx(a) - xlx(b) - xlx(1-a-b)

    p3 = lambda x: 1/4 + x.alpha3
    p2 = lambda x: 1/8 + x.alpha3/2 + x.alpha2
    p1 = lambda x: 1/16 + x.alpha3/4 + x.alpha2/2+x.alpha1
    p0 = lambda x: p1(x)/2

    m3 = lambda x: x.alpha3
    m2 = lambda x: x.alpha3/2 + x.alpha2
    m1 = lambda x: x.alpha3/4 + x.alpha2/2 + x.alpha1
    m0 = lambda x: m1(x)/2

    D1 = lambda x: g(p1(x), m1(x))
    D2 = lambda x: g(p2(x), m2(x))
    D3 = lambda x: g(p3(x), m3(x))
    q2 = lambda x: D2(x) + x.r1 - 2*D1(x)
    q3 = lambda x: D3(x) + x.r2 - 2*D2(x)
    q4 = lambda x: 1 + x.r3 - 2*D3(x)

    t1= lambda x: max(7*x.l1 - r(x),0)
    t2= lambda x: max(7*x.l1 + 3*x.l2 - r(x),0) - t1(x)
    t3= lambda x: max(7*x.l1 + 3*x.l2 + x.l3 - r(x), 0) - t1(x) - t2(x)

    l = lambda x: x.l1+x.l2+x.l3
    r = lambda x: x.r3 + 2*x.r2 + 4*x.r1

    def bcj_reps(p, d, m):
        return p+d+binomH(1-p-d, m) + binomH(1-p-d-m, m)

    bjc_constraints = [
        # representations
        {'type': 'eq', 'fun':
         bcj(lambda x: x.r1 - bcj_reps(p2(x), m2(x), x.alpha1))},
        {'type': 'eq', 'fun':
         bcj(lambda x: x.r2 - bcj_reps(p3(x), m3(x), x.alpha2))},
        {'type': 'eq', 'fun':
         bcj(lambda x: x.r3 - bcj_reps(1/2, 0, x.alpha3))},

        # list sizes
        # { 'type' : 'eq'  , 'fun' : bcj(lambda x : x.L4 - (2*x.L3- (1-l(x)) +q4(x)))},
        {'type': 'ineq', 'fun': bcj(lambda x: x.L3 - (2*x.L2 - x.l3 + q3(x)))},
        {'type': 'ineq', 'fun': bcj(lambda x: x.L2 - (2*x.L1 - x.l2 + q2(x)))},
        {'type': 'ineq', 'fun': bcj(lambda x: x.L1 - (D1(x) - x.l1))},

        # correctness constraints
        {'type': 'ineq', 'fun': bcj(lambda x: 1-l(x))},
        # { 'type' : 'ineq', 'fun' : bcj(lambda x : x.r3-x.r2)},
        # { 'type' : 'ineq', 'fun' : bcj(lambda x : x.r2-x.r1)},

        # memory
        {'type': 'ineq', 'fun':
         bcj(lambda x: membound - bcj_memory(x))},

        # saturation constraints
        {'type': 'ineq', 'fun': bcj(lambda x: x.l1 - x.r1)},
        {'type': 'ineq', 'fun':
         bcj(lambda x: x.l2 - (2*x.r1 + x.r2 - 3*x.l1))},
        {'type': 'ineq', 'fun': bcj(lambda x: x.l3 - (r(x)-7*x.l1-3*x.l2))},
    ]

    def bcj_classical_time_new(x):
        """
        Time with 7-Diss and repition of subtrees
        """
        x = set_bcj(*x)
        m = max(x.L3, x.L2, x.L1)
        space = D1(x)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        timefac = time7diss(memfac)
        return max(max(space*timefac, x.L1) + t1(x)
                   , max(x.L1, x.L2 - q2(x)) + t2(x) + t1(x)
                   , max(x.L2, x.L3 - q3(x), 2*x.L3-(1-l(x)))
                   + t3(x) + t2(x) + t1(x))

    def bcj_classical_time_dissection(x):
        """
        Time with 7-Diss but without repition of subtrees
        """
        x = set_bcj(*x)
        m = max(x.l3, x.l2, x.l1)
        space = D1(x)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        timefac = time7diss(memfac)
        return max(max(space*timefac, x.L1)
                   , max(x.L1, x.L2 - x.l1)
                   , max(x.L2, x.L3 - x.l2)
                   , max(x.L3, x.L4 - x.l3))

    def bcj_classical_time_org(x):
        """
        Time and Memory without 7-Diss and without repition of subtrees
        """
        x = set_bcj(*x)
        return max(max(x.L1*2, x.L2 - x.l1)
                   , max(x.L2, x.L3 - x.l2)
                   , max(x.L3, x.L4 - x.l3))

    def bcj_memory_new(x):
        """
        Memory with 7-Diss
        """
        x = set_bcj(*x)
        space = D1(x)
        m = max(x.L1, x.L2, x.L3)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        return max(space*memfac, m)

    def bcj_memory_org(x):
        """
        Memory MITM
        """
        x = set_bcj(*x)
        return max(x.L4, x.L3, x.L2, x.L1)

    time = bcj_classical_time_org
    if new:
        time = bcj_classical_time_new
    if only_diss:
        time = bcj_classical_time_dissection

    bcj_memory = bcj_memory_org
    if new:
        bcj_memory = bcj_memory_new

    # objective = time
    mycons = bjc_constraints

    start = [random.uniform(0, 0.15) for _ in range(7)] +\
            [random.uniform(0, 0.05) for _ in range(3)] +\
            [random.uniform(0, 1) for _ in range(3)]

    bounds = [(0, 0.8)]*7 + [(0, 0.05)] * 3 + [(0, 1)]*3

    result = opt.minimize(time, start, bounds=bounds, tol=1e-10,
                          constraints=mycons, options={'maxiter': iters})

    astuple = set_bcj(*result.x)

    if verb:
        print(t1(astuple), t2(astuple), t3(astuple))
        print("memory ", bcj_memory(result.x))
        print("Validity: ", result.success)
        print("Time: ", round_upwards_to_str(time(astuple)))
        for t in astuple._asdict():
            print(t, round_upwards_to_str(astuple._asdict()[t]))

        print("Checking that the constraints are satisfied:")
        print(check_constraints(mycons, result.x))
    else:
        if not NOLOG:
            t = check_constraints(mycons, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(time(astuple)))

    t = check_constraints(mycons, result.x)

    if all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq") \
       and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq"):
        return time(astuple)
    else:
        return -1


###############################################################################
#################################BBSS##########################################
###############################################################################

def optimize_bbss(new=True, only_diss=False, membound=1, active_two=True,
                  verb=True, iters=10000):
    """
    Optimization target: new algorithm for subset-sum, using {0,-1,1,2}
    representations
    with a 4-level merging tree.

    :param new: if set to true the new version of `BCJ` will be optimizes
                if false, the original version.
    :param only_diss: if set to `true` the optimization will take the 7/11
                    dissection into account but not the tree repetitions.
    :param active_two: if set to `true` will add two into the optimization.
    :param verb: verbose output
    :param membound: set the maximal memory the optimisation should use
                    value between [0,1]
    """
    set_bbss = collections.namedtuple('classical', 'p0 p1 p2 l1 l2 l3 l4 c1 c2 c3 alpha1 alpha2 alpha3 gamma1 gamma2 gamma3')

    def bbss(f):
        return wrap(f, set_bbss)

    if new and only_diss:
        print("please specify either the ne algorithm or only dissection")
        return

    # =================================
    # Among these variables:
    # - pi is the filtering probability at level i
    # - li is the list size at level i (classically, all lists at a given level
    # have same size)
    # (l0 = 0, since we want to find the solution)
    # - ci is the total number of bits of the modular constraint at level i
    # - alphai is the total number of "-1" at level i
    # - gammai is the total number of "2" at level i

    constraints_bbss = [
        # filtering terms
        {'type': 'eq', 'fun': bbss(lambda x: p_good_2_aux(1/2., 0, 0., 1/4.+x.alpha1-2*x.gamma1, x.alpha1, x.gamma1) - x.p0)},
        {'type': 'eq', 'fun': bbss(lambda x: p_good_2(1/4.+x.alpha1-2*x.gamma1, x.alpha1, x.gamma1, 1/8.+x.alpha2-2*x.gamma2, x.alpha2, x.gamma2) - x.p1)},
        {'type': 'eq', 'fun': bbss(lambda x: p_good_2(1/8.+x.alpha2-2*x.gamma2, x.alpha2, x.gamma2, 1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3) - x.p2)},

        # sizes of the lists
        # { 'type' : 'eq', 'fun' : bbss(lambda x : 2*x.l1 - (1-x.c1) + x.p0 )},
        {'type': 'eq', 'fun': bbss(lambda x: 2*x.l2 - (x.c1 - x.c2) + x.p1 - x.l1)},
        {'type': 'eq', 'fun': bbss(lambda x: 2*x.l3 - (x.c2 - x.c3) + x.p2 - x.l2)},
        {'type': 'eq', 'fun': bbss(lambda x: 2*x.l4 - x.c3 - x.l3)},
        {'type': 'ineq', 'fun': bbss(lambda x: f(1/4.+x.alpha1-2*x.gamma1, x.alpha1, x.gamma1) - x.c1 - x.l1)},
        {'type': 'ineq', 'fun': bbss(lambda x: f(1/8.+x.alpha2-2*x.gamma2, x.alpha2, x.gamma2) - x.c2 - x.l2)},
        {'type': 'ineq', 'fun': bbss(lambda x: f(1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3) - x.c3 - x.l3)},
        {'type': 'ineq', 'fun': bbss(lambda x: x.l4-f(1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3)*0.5 )},

        # coherence of the -1
        {'type': 'ineq', 'fun': bbss(lambda x: x.alpha2 - x.alpha1/2)},
        {'type': 'ineq', 'fun': bbss(lambda x: x.alpha3 - x.alpha2/2)},
        {'type': 'ineq', 'fun': bbss(lambda x: x.alpha1 - 2*x.gamma1)},
        {'type': 'ineq', 'fun': bbss(lambda x: x.alpha2 - 2*x.gamma2)},
        {'type': 'ineq', 'fun': bbss(lambda x: x.alpha3 - 2*x.gamma3)},

        # memory
        {'type': 'ineq', 'fun': bbss(lambda x: membound-bbss_memory(x))},
    ]

    if active_two:
        constraints_bbss.append({'type': 'ineq', 'fun': bbss(lambda x: - x.gamma1)})
        constraints_bbss.append({'type': 'ineq', 'fun': bbss(lambda x: - x.gamma2)})
        constraints_bbss.append({'type': 'ineq', 'fun': bbss(lambda x: - x.gamma3)})

    def bbss_time_new(x):
        """
        Time with 7-Diss and repition of subtrees
        """
        x = set_bbss(*x)
        m = max(x.l3, x.l2, x.l1)
        space = f(1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        timefac = time7diss(memfac)
        it3 = x.c1-x.c2  # l3
        it2 = x.c2-x.c3  # l2
        return max(max(space*timefac, x.l3) - min(2*x.l1 - (1-x.c1) + x.p0 + it3 + 3*it2, 0)
                   , max(x.l3, x.l2 - x.p2) - min(2*x.l1 - (1-x.c1) + x.p0 + it3, 0)
                   , max(x.l2, x.l1 - x.p1, 2*x.l1 - (1-x.c1))
                   - min(2*x.l1 - (1-x.c1) + x.p0, 0))

    def bbss_time_dissection(x):
        """
        Time with 7-Diss but without repition of subtrees
        """
        x = set_bbss(*x)
        m = max(x.l3, x.l2, x.l1)
        space = f(1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        timefac = time7diss(memfac)
        # return max(x.l4, x.l3, x.l2 - x.p2, x.l1 - x.p1, -x.p0)
        # it3=x.c1-x.c2 # l3
        # it2=x.c2-x.c3 # l2
        return max(max(space*timefac, x.l3) - min(2*x.l1 - (1-x.c1) + x.p0, 0)
                   , max(x.l3, x.l2 - x.p2) - min(2*x.l1 - (1-x.c1) + x.p0, 0)
                   , max(x.l2, x.l1 - x.p1, 2*x.l1 - (1-x.c1))
                   - min(2*x.l1 - (1-x.c1) + x.p0, 0))

    def bbss_time_org(x):
        """
        Time and Memory without 7-Diss and without repition of subtrees
        """
        x = set_bbss(*x)
        # it3=x.c1-x.c2 # l3
        # it2=x.c2-x.c3 # l2
        return max(max(x.l4, x.l3) - min(2*x.l1 - (1-x.c1) + x.p0, 0)
                   , max(x.l3, x.l2 - x.p2) - min(2*x.l1 - (1-x.c1) + x.p0, 0)
                   , max(x.l2, x.l1 - x.p1, 2*x.l1 - (1-x.c1))
                   - min(2*x.l1 - (1-x.c1) + x.p0, 0))

    def bbss_memory_new(x):
        """
        Memory with 7-Diss
        """
        x = set_bbss(*x)
        space = f(1/16.+x.alpha3-2*x.gamma3, x.alpha3, x.gamma3)
        m = max(x.l3, x.l2, x.l1)
        memfac = m/space
        memfac = max(1/7, min(memfac, 1/4))
        return max(space * memfac, x.l3, x.l2, x.l1)

    def bbss_memory_org(x):
        """
        MITM Memory
        """
        x = set_bbss(*x)
        return max(x.l4, x.l3, x.l2, x.l1)

    time = bbss_time_org
    if new:
        time = bbss_time_new
    if only_diss:
        time = bbss_time_dissection

    bbss_memory = bbss_memory_org
    if new:
        bbss_memory = bbss_memory_new
    mycons = constraints_bbss

    start = [(-0.2)]*3 +\
            [random.uniform(0.18, 0.22) for _ in range(7)] +\
            [0.03]*3 +\
            [(0.000)]*3

    bounds = [(-0.6, 0)]*3 +\
             [(0, 1)]*7 +\
             [(0, 0.05)]*3 +\
             [(0, 0.00)]*3

    result = opt.minimize(time, start, bounds=bounds, tol=1e-10,
                          constraints=mycons, options={'maxiter': iters})

    astuple = set_bbss(*result.x)
    if verb:
        print("memory ", bbss_memory(result.x))
        print("Validity: ", result.success)
        print("Time: ", round_upwards_to_str(time(astuple)))
        for t in astuple._asdict():
            print(t, round_upwards_to_str(astuple._asdict()[t]))
        print("Checking that the constraints are satisfied:")
        print(check_constraints(mycons, result.x))
    else:
        if not NOLOG:
            t = check_constraints(mycons, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(time(astuple)))
    t = check_constraints(mycons, result.x)

    if all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq") and \
       all(-10**(-7) <= i[1] for i in t if i[0] == "ineq"):
        return time(astuple)
    else:
        return -1


def BCJ_BBSS_memlimit(bbss=False, new=False):
    """
    calc runtime for every memory limitation
    :param bbss: if set to `true` bbss will get optimized, else bcj
    :param new: if set to `true` the new versions get optimized, else the
                original.
    """
    L = []
    algo = optimize_bcj
    if bbss:
        algo = optimize_bbss
    membound = 0.29
    while membound > 0.05:
        mini = 2
        c = 0
        while c < 5:
            try:
                t = float(algo(new=new, verb=False))
                print(t)
            except ValueError:
                print("error")
                continue

            if t != -1:
                if mini > t:
                    mini = t
                c += 1

        L.append([membound, mini])
        membound -= 0.02

    return L


###############################################################################
#################################BJMM##########################################
###############################################################################

def optimize_bjmm(k=0.488, w=Hi(1-0.488)/2, verb=False, membound=1.,
                  iters=10000):
    """
    optimize the original version of Becker Joux May Meurers algorithm:
        https://eprint.iacr.org/2012/026
    :param k: code rate
    :param w: error weight
    :param verb: verbose output
    :param membound: optimize under memory constraint: in [0, 1]
    :param iters: number of iterations scipy is using.
    """
    set_bjmm = collections.namedtuple('BJMM', 'l p p1 p2 L0 L1 L2 r1 r2')

    def bjmm(f):
        return wrap(f, set_bjmm)

    def bjmm_reps(p, p2, l):
        if p == 0. or p2 == 0. or l == 0.:
            return 0
        if l < p2 or p < p2/2. or l - p2 < p - p2/2.:
            return 0.

        return binomH(p2, p2/2.) + binomH(l-p2, p-p2/2.)

    def classical_time_bjmm(x):
        x = set_bjmm(*x)
        perms = binomHH(1., w) - binomHH(k + x.l, x.p) - \
            binomHH(1. - k - x.l, w - x.p)
        T1 = max(2.*x.L0 - x.r1, x.L0)
        T2 = max(2.*x.L1 - (x.r2 - x.r1), x.L1)
        T3 = max(2.*x.L2 - (x.l - x.r2), x.L2)
        return perms + max(T1, T2, T3)

    def classical_mem_bjmm(x):
        x = set_bjmm(*x)
        return max(x.L0, x.L1, x.L2)

    constraints_bjmm = [
        # weights
        {'type': 'ineq',   'fun': bjmm(lambda x: (2. * x.p1) - x.p2)},
        {'type': 'ineq',   'fun': bjmm(lambda x: (2. * x.p2) - x.p)},

        # representations and constrains
        {'type': 'ineq',   'fun': bjmm(lambda x: x.r2 - x.r1)},
        {'type': 'ineq',   'fun': bjmm(lambda x: x.l - x.r2)},

        # reps
        {'type': 'eq',   'fun': bjmm(
            lambda x: x.r1 - bjmm_reps(x.p1, x.p2, k + x.l))},
        {'type': 'eq',   'fun': bjmm(
            lambda x: x.r2 - bjmm_reps(x.p2, x.p,  k + x.l))},

        # list
        {'type': 'eq',   'fun': bjmm(
            lambda x: x.L0 - binomHH((k+x.l)/2, x.p1/2.))},
        {'type': 'eq',   'fun': bjmm(
            lambda x: x.L1 - (binomHH((k+x.l), x.p1) - x.r1))},
        {'type': 'eq',   'fun': bjmm(
            lambda x: x.L2 - (binomHH((k+x.l), x.p2) - x.r2))},

        # memory
        {'type': 'ineq', 'fun': bjmm(
            lambda x: membound-classical_mem_bjmm(x))},
    ]

    time = classical_time_bjmm
    objective = time
    mycons = constraints_bjmm

    start = [(rng.uniform(0.05, 0.09))]+[(rng.uniform(0.01, 0.02))] + \
        [(rng.uniform(0.001, 0.015))]*2 + \
        [(0.031)]*3 + [(rng.uniform(0.001, 0.2))]*2
    bounds = [(0.05, 0.08)]*1 + [(0.001, 0.03)]*1 + \
        [(0.0002, 0.02)]*2 + [(0.001, 0.04)]*3 + [(0.002, 0.05)]*2

    result = opt.minimize(time, start,
                          bounds=bounds, tol=1e-7,
                          constraints=mycons, options={'maxiter': iters})

    astuple = set_bjmm(*result.x)

    if verb:
        print("Validity: ", result.success)
        print("Time: ", time(astuple))

        for t in astuple._asdict():
            print(t, round_to_str(astuple._asdict()[t]))
        print("Checking that the constraints are satisfied:")
        print(check_constraints(mycons, result.x))
    else:
        if not NOLOG:
            t = check_constraints(mycons, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(time(astuple)))

    return result.success, objective(astuple), result


def optimize_mem_bjmm(retries=1000):
    """
    finds the optimal runtime under a certain memory restriction
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    bjmm_data = []
    for mem in float_range(0., 0.2, 0.1):
        global bjmm_membound
        bjmm_membound = mem
        time = min([optimize_bjmm(verb=False, membound=bjmm_membound) for _ in range(retries)])
        bjmm_data.append([mem, time])
    print(bjmm_data)
    return bjmm_data


def optimize_k_bjmm(retries=1000, half_distance=True):
    """
    optimize under restrictions on the code rate
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    bjmm_data = []
    for k_ in float_range(0., 0.5, 0.1):
        k = k_
        w = Hi(1 - k_)
        if half_distance:
            w = w/2

        time = min([optimize_bjmm(k=k, w=w, verb=False) for _ in range(retries)])
        bjmm_data.append([k, w, time])
    print(bjmm_data)
    return bjmm_data


###############################################################################
#################################NEW BJMM######################################
###############################################################################


def optimize_new_bjmm(k=0.488, w=Hi(1-0.488)/2, verb=False,
                      membound=1., iters=10000):
    """
    optimize the new version of Becker Joux May Meurers algorithm:
        https://eprint.iacr.org/2012/026
    :param k: code rate
    :param w: error weight
    :param verb: verbose output
    :param membound: optimize under memory constraint: in [0, 1]
    :param iters: number of iterations scipy is using.
    """

    set_new_bjmm = collections.namedtuple(
        'NEWBJMM', 'l p p1 p2 L1 L2 L3 r1 r2 l1 l2')

    def new_bjmm(f):
        return wrap(f, set_new_bjmm)

    def new_bjmm_reps(p, p2, l):
        if p == 0. or p2 == 0. or l == 0.:
            return 0
        if l < p2 or p < p2/2. or l - p2 < p - p2/2.:
            return 0.

        return binomHH(p2, p2/2.) + binomHH(l-p2, p-p2/2.)

    def classical_time_new_bjmm(x):
        x = set_new_bjmm(*x)
        perms = binomHH(1., w) - binomHH(k + x.l, x.p) - \
            binomHH(1. - k - x.l, w - x.p)
        T1 = max(2*x.L1 - x.l1, x.L1)
        T2 = max(2*x.L2 - x.r2, x.L2)
        T3 = max(2*x.L3 - (x.l - x.l2 - x.l1), x.L3)

        return max(
            max(3*x.l1 - 2*x.r1 - x.r2, 0) + T1,
            max(3*x.l1 + x.l2 - 2*x.r1 - x.r2, 0) + max(T2, T3)
        ) + perms
        # return perms + max(x.L1,
        #                   2*x.L1-x.r1, x.L2,
        #                   2*x.L2-(x.r2-x.r1),
        #                   x.L3,
        #                   2*x.L3 - (x.l - x.r2))
        #                   #x.L4)

    def classical_mem_new_bjmm(x):
        x = set_new_bjmm(*x)
        return max(x.L1/2, x.L2, x.L3)  # , x.L4)

    constraints_new_bjmm = [
        # weights
        {'type': 'ineq',   'fun': new_bjmm(lambda x: 2. * x.p1 - x.p2)},
        {'type': 'ineq',   'fun': new_bjmm(lambda x: 2. * x.p2 - x.p)},

        # reps
        {'type': 'eq',   'fun': new_bjmm(
            lambda x: x.r1 - new_bjmm_reps(x.p1, x.p2, k + x.l))},
        {'type': 'eq',   'fun': new_bjmm(
            lambda x: x.r2 - new_bjmm_reps(x.p2, x.p, k + x.l))},

        # binomial coeeficient correctness
        {'type': 'ineq',   'fun': new_bjmm(lambda x: x.l - (x.l1 + x.l2))},
        {'type': 'ineq',   'fun': new_bjmm(lambda x: x.l1 - x.r1)},
        {'type': 'ineq',   'fun': new_bjmm(lambda x: x.l2 - x.r2)},
        # { 'type' : 'ineq',   'fun' : new_bjmm(lambda x : 2*x.r1 + x.r2 - x.l2 - 3*x.l1) },

        # list
        {'type': 'eq',   'fun': new_bjmm(
            lambda x: x.L1 - binomHH((k+x.l)/2, x.p1/2.))},
        {'type': 'eq',   'fun': new_bjmm(
            lambda x: x.L2 - (binomHH((k+x.l), x.p1) - x.l1))},
        {'type': 'eq',   'fun': new_bjmm(
            lambda x: x.L3 - (binomHH((k+x.l), x.p2) + x.r1 - 3*x.l1 - x.l2))},
        # { 'type' : 'eq',   'fun' : new_bjmm(lambda x : x.L4 - (binomHH((k+x.l), x.p) - x.l)  ) },

        # correctness
        # { 'type' : 'ineq',   'fun' : new_bjmm(lambda x : 1. - k - x.l) },
        # { 'type' : 'ineq',   'fun' : new_bjmm(lambda x : (1. - k - x.l) - (w - x.p)) },
        # { 'type' : 'ineq',   'fun' : new_bjmm(lambda x : w - x.p) },

        # memory
        {'type': 'ineq', 'fun': new_bjmm(
            lambda x: membound-classical_mem_new_bjmm(x))},
    ]

    time = classical_time_new_bjmm
    objective = time
    mycons = constraints_new_bjmm

    start = [(rng.uniform(0.06, 0.08))] + \
            [(rng.uniform(0.01, 0.02))] + \
            [(rng.uniform(0.005, 0.2))]*9
    bounds = [(0.06, 0.08)]*1 + \
             [(0.01, 0.02)]*1 + \
             [(0.0002, 0.02)]*2 + \
             [(0.001, 0.04)]*7

    result = opt.minimize(time, start,
                          bounds=bounds, tol=1e-7,
                          constraints=mycons, options={'maxiter': iters})

    astuple = set_new_bjmm(*result.x)
    if verb:
        print("Validity: ", result.success)
        print("Time: ", time(astuple))

        for t in astuple._asdict():
            print(t, round_to_str(astuple._asdict()[t]))

        print("Checking that the constraints are satisfied:")
        print(check_constraints(mycons, result.x))
    else:
        if not NOLOG:
            t = check_constraints(mycons, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(time(astuple)))

    return result.success, objective(astuple), result


def optimize_mem_new_bjmm(retries=1000):
    """
    finds the optimal runtime under a certain memory restriction
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    bjmm_data = []
    for mem in float_range(0., 0.2,  0.02):
        global new_bjmm_membound
        new_bjmm_membound = mem
        time = min([optimize_new_bjmm(membound=new_bjmm_membound, verb=False) for _ in range(retries)])
        bjmm_data.append([mem, time])
    print(bjmm_data)
    return bjmm_data


def optimize_k_new_bjmm(retries=1000, half_distance=True):
    """
    optimize under restrictions on the code rate
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    bjmm_data = []
    for k_ in float_range(0., 0.5, 0.1):
        k = k_
        w = Hi(1 - k_)
        if half_distance:
            w = w/2

        time = min([optimize_new_bjmm(k=k, w=w, verb=False) for _ in range(retries)])
        bjmm_data.append([k, w, time])
    print(bjmm_data)
    return bjmm_data


###############################################################################
#################################MMT###########################################
###############################################################################


def optimize_mmt(k=0.488, w=Hi(1-0.488)/2, verb=False, membound=1.,
                 iters=10000):
    """
    optimize the original version of May Meurers Thomae algorithm:
        https://www.iacr.org/archive/asiacrypt2011/70730106/70730106.pdf
    :param k: code rate
    :param w: error weight
    :param verb: verbose output
    :param membound: optimize under memory constraint: in [0, 1]
    :param iters: number of iterations scipy is using.
    """
    set_mmt = collections.namedtuple('MMT', 'l p L1 L2 L3 r1')

    def mmt(f):
        return wrap(f, set_mmt)

    def dissection_mmt_memory(x):
        """Memory with 7-Diss
        """
        x = set_mmt(*x)
        space = binomHH((k+x.l)/2, x.p/4)
        m = max(x.L1, x.L2, x.L3)
        memfac = m / space
        memfac = max(1/7, min(memfac, 1/4))
        return max(space * memfac, m)

    def classical_time_mmt(x):
        """
        """
        x = set_mmt(*x)
        perms = binomHH(1., w) - binomHH(k + x.l, x.p) - \
            binomHH(1. - k - x.l, w - x.p)
        return perms + max(x.L1, x.L2, x.L3)

    def classical_memory_mmt(x):
        """
        """
        return max(x.L1, x.L2, x.L3)
        # return max(x.L1/2, x.L2, x.L3)
        # return dissection_mmt_memory(x)

    # classical mmt
    constraints_mmt = [
        # list
        {'type': 'eq',   'fun': mmt(lambda x: x.L1 - binomHH((k+x.l)/2, x.p/4))},
        {'type': 'eq',   'fun': mmt(lambda x: x.L2 - (2*x.L1 - x.r1))},
        {'type': 'eq',   'fun': mmt(lambda x: x.L3 - (2*x.L2 - (x.l - x.r1)))},
        # reps
        {'type': 'eq',   'fun': mmt(lambda x: x.r1 - binomHH(x.p, x.p/2.))},
        # memory
        {'type': 'ineq', 'fun': mmt(
            lambda x: membound-classical_memory_mmt(x))},
    ]

    start = [(rng.uniform(0.001, 0.2))]*2 +\
            [(0.1)] * 3 + \
            [(rng.uniform(0.001, 0.22))]*1
    bounds = [(0., 0.3)]*6

    result = opt.minimize(classical_time_mmt, start,
                          bounds=bounds, tol=1e-7,
                          constraints=constraints_mmt, options={'maxiter': iters})

    astuple = set_mmt(*result.x)

    if verb:
        print("Validity: ", result.success)
        print("Time: ", classical_time_mmt(astuple))

        for t in astuple._asdict():
            print(t, round_to_str(astuple._asdict()[t]))
        print("Checking that the constraints are satisfied:")
        print(check_constraints(constraints_mmt, result.x))

        return result.success, classical_time_mmt(astuple), result
    else:
        if not NOLOG:
            t = check_constraints(constraints_mmt, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(classical_time_mmt(astuple)))

    return classical_time_mmt(astuple)


def optimize_mem_mmt(retries=1000):
    """
    finds the optimal runtime under a certain memory restriction
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    mmt_data = []
    for mem in float_range(0., 0.2, 0.02):
        time = min([optimize_mmt(membound=mem, verb=False) for _ in range(retries)])
        mmt_data.append([mem, time])
    print(mmt_data)
    return mmt_data


def optimize_k_mmt(retries=1000, half_distance=True):
    """
    optimize under restrictions on the code rate
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    mmt_data = []
    for k_ in float_range(0., 0.5, 0.1):
        k = k_
        w = Hi(1 - k_)
        if half_distance:
            w = w/2

        time = min([optimize_mmt(k=k, w=w, verb=False) for _ in range(retries)])
        mmt_data.append([k, w, time])
    print(mmt_data)
    return mmt_data


def optimize_new_mmt(k=0.488, w=Hi(1-0.488)/2, verb=False,
                     membound=1.0, iters=10000):
    """
    optimize the new version of May Meurers Thomae algorithm:
        https://www.iacr.org/archive/asiacrypt2011/70730106/70730106.pdf
    :param k: code rate
    :param w: error weight
    :param verb: verbose output
    :param membound: optimize under memory constraint: in [0, 1]
    :param iters: number of iterations scipy is using.
    """
    set_new_mmt = collections.namedtuple('NEWMMT', 'l p L1 L2 L3 r1 l1')

    def new_mmt(f):
        return wrap(f, set_new_mmt)

    def dissection_new_mmt_memory(x):
        """
        Memory with 7-Diss
        """
        x = set_new_mmt(*x)
        space = binomHH((k+x.l)/2, x.p/4)
        m = max(x.L1, x.L2, x.L3)
        memfac = m / space
        memfac = max(1/7, min(memfac, 1/4))
        return max(space * memfac, m)

    def classical_time_new_mmt(x):
        """
        """
        x = set_new_mmt(*x)
        perms = binomHH(1., w) - binomHH(k + x.l, x.p) - \
            binomHH(1. - k - x.l, w - x.p)
        tree = max(x.L1, x.L2, x.L3) + max(0, x.l1-x.r1)
        return perms + tree

    def classical_memory_new_mmt(x):
        """
        """
        x = set_new_mmt(*x)
        return max(x.L1, x.L2, x.L3)
        # return max(x.L1/2, x.L2, x.L3)
        # return dissection_genius_mmt_memory(x)

    constraints_new_mmt = [
        # list
        {'type': 'eq',   'fun': new_mmt(
            lambda x: x.L1 - binomHH((k+x.l)/2, x.p/4))},
        {'type': 'eq',   'fun': new_mmt(lambda x: x.L2 - (2*x.L1 - x.l1))},
        {'type': 'eq',   'fun': new_mmt(lambda x: x.L3 - (2*x.L2 - (x.l - x.l1)))},
        # reps
        {'type': 'eq',   'fun': new_mmt(lambda x: x.r1 - binomHH(x.p, x.p/2.))},
        # memory
        {'type': 'ineq', 'fun': new_mmt(
            lambda x: membound-classical_memory_new_mmt(x))},
        # correctness
        {'type': 'ineq', 'fun': new_mmt(lambda x: x.l - x.l1)},
        {'type': 'ineq', 'fun': new_mmt(lambda x: x.l1 - x.r1)},
    ]

    start = [(rng.uniform(0.0, 0.03))]*1 + [(rng.uniform(0.0, 0.03))] * \
        1 + [(0.01)]*3 + [(rng.uniform(0.001, 0.01))]*2
    # start = [(0.022)]*1 + [(0.007)]*1 + [(0.015)]*3 + [(0.007)]*2
    bounds = [(0., 0.05)] + [(0., 0.05)] + [(0., 0.02)]*3 + [(0., 0.02)]*2

    result = opt.minimize(classical_time_new_mmt, start,
                          bounds=bounds, tol=1e-7,
                          constraints=constraints_new_mmt, options={'maxiter': iters})

    astuple = set_new_mmt(*result.x)

    if verb:
        print("Validity: ", result.success)
        print("Time: ", classical_time_new_mmt(astuple))

        for t in astuple._asdict():
            print(t, round_to_str(astuple._asdict()[t]))
        print("Checking that the constraints are satisfied:")
        print(check_constraints(constraints_new_mmt, result.x))

        return result.success, classical_time_new_mmt(astuple), result
    else:
        if not NOLOG:
            t = check_constraints(constraints_new_mmt, result.x)
            valid = all(-10**(-7) <= i[1] <= 10**(-7) for i in t if i[0] == "eq")\
                and all(-10**(-7) <= i[1] for i in t if i[0] == "ineq")

            print("Validity: ", result.success & valid)
            print("Time: ", round_upwards_to_str(classical_time_new_mmt(astuple)))
    return classical_time_new_mmt(astuple)


def optimize_mem_new_mmt(retries=100):
    """
    finds the optimal runtime under a certain memory restriction
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    mmt_data = []
    retries = 3
    for mem in float_range(0., 0.2, 0.02):
        time = min([optimize_new_mmt(membound=mem, verb=False) for _ in range(retries)])
        mmt_data.append([mem, time])
    print(mmt_data)
    return mmt_data


def optimize_k_new_mmt(retries=1000, half_distance=True):
    """
    optimize under restrictions on the code rate
    :param retries: number of repetitions to find the minimum. Note that this
                    values does NOT effect the number of repetitions of scipy.
    """
    mmt_data = []
    retries = 3
    for k_ in float_range(0., 0.5, 0.1):
        k = k_
        w = Hi(1 - k_)
        if half_distance:
            w = w/2

        time = min([optimize_new_mmt(k=k, w=w, verb=False) for _ in range(retries)])
        mmt_data.append([k, w, time])
    print(mmt_data)
    return mmt_data


def bjmm_depth_2_qc_complexity(n: int, k: int, w: int, mem=inf, hmap=1, mmt=0, qc=0, base_p=-1, l_val=0, l1_val=0, memory_access=0, enable_tmto=1):
    """
        Complexity estimate of BJMM algorithm in depth 2
        [MMT11] May, A., Meurer, A., Thomae, E.: Decoding random linear codes in  2^(0.054n). In: International Conference
        on the Theory and Application of Cryptology and Information Security. pp. 107–124. Springer (2011)
        [BJMM12] Becker, A., Joux, A., May, A., Meurer, A.: Decoding random binary linear codes in 2^(n/20): How 1+ 1= 0
        improves information set decoding. In: Annual international conference on the theory and applications of
        cryptographic techniques. pp. 520–536. Springer (2012)
        expected weight distribution::
            +--------------------------+-------------------+-------------------+
            | <-----+ n - k - l +----->|<--+ (k + l)/2 +-->|<--+ (k + l)/2 +-->|
            |           w - 2p         |        p          |        p          |
            +--------------------------+-------------------+-------------------+

        INPUT:
        - ``n`` -- length of the code
        - ``k`` -- dimension of the code
        - ``w`` -- Hamming weight of error vector
        - ``mem`` -- upper bound on the available memory (as log2), default unlimited
        - ``hmap`` -- indicates if hashmap is being used (default: true)
        - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
        - ``mmt`` -- restrict optimization to use of MMT algorithm (precisely enforce p1=p/2)
        - ``qc`` -- optimize in the quasi cyclic setting
        - ``base_p`` -- hard code the base p enumerated in the baselists.
                        if this value is set to -1 the code will optimize over
                        different values
        - ``l_val`` -- hardcode `l`. If set to 0 the code will optimize over
                        different values.
        - ``l1_val`` -- same as `l` only for `l1`
        - ``memory_access`` -- specifies the memory access cost model
                                (default: 0, choices:
                                 0 - constant,
                                 1 - logarithmic,
                                 2 - square-root,
                                 3 - cube-root
                                 or deploy custom function which takes as input
                                 the logarithm of the total memory usage)
        - ``enable_tmto`` -- enable the new time memory tradeoff proposed in
                            this work
    """
    n = int(n)
    k = int(k)
    w = int(w)

    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [25, 450, 25]
    i_val_inc = [10, 10, 10]
    params = [-1 for _ in range(7)]
    lists = []

    while True:
        stop = True
        mod2 = (params[0] - i_val_inc[0]//2) % 2
        for p in range(max(params[0] - i_val_inc[0]//2 - mod2, 2*qc), min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), min(i_val[1], n - k))):
                for p1 in range(max(params[2] - i_val_inc[2] // 2, (p + 1) // 2, qc), min(w, i_val[2])):
                    if mmt and p1 != p // 2:
                        continue

                    if base_p != -1 and p1 != base_p:
                        continue

                    if l_val != 0 and l != l_val:
                        continue

                    k1 = (k + l) // 2
                    L1 = binom(k1, p1)
                    if qc:
                        L1b = binom(k1, p1-1)*k

                    if log2(L1) > time:
                        continue

                    if k1 - p < p1 - p / 2:
                        continue

                    if not (qc):
                        reps = (binom(p, p//2) * binom(k1 - p, p1 - p//2)) ** 2
                    else:
                        reps = binom(p, p//2) * binom(k1 - p, p1 -
                                                      p//2)*binom(k1 - p+1, p1 - p // 2)
                        if p-1 > p//2:
                            reps *= (binom(p-1, p // 2))

                    if enable_tmto == 1:
                        start = int(log2(L1))-5
                        end = start + 10
                    else:
                        start = int(ceil(log2(reps)))
                        end = start + 1

                    for l1 in range(start, end):
                        if l1 > l:
                            continue

                        L12 = max(1, L1 ** 2 // 2 ** l1)

                        qc_advantage = 0
                        if qc:
                            L12b = max(1, L1*L1b//2**l1)
                            qc_advantage = log2(k)

                        tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r)) if not (
                            qc) else log2(L1+L1b + min(L12, L12b) + _mem_matrix(n, k, r))
                        if tmp_mem > mem:
                            continue

                        Tp = max(log2(binom(n, w))
                                 - log2(binom(n - k - l, w - 2 * p + qc))
                                 - log2(binom(k1, p))
                                 - log2(binom(k1, p - qc))
                                 - qc_advantage - solutions, 0)

                        Tg = _gaussian_elimination_complexity(n, k, r)
                        if not (qc):
                            T_tree = 2 * _list_merge_complexity(L1, l1, hmap) + _list_merge_complexity(L12,
                                                                                                       l - l1,
                                                                                                       hmap)
                        else:
                            T_tree = _list_merge_async_complexity(L1, L1b, l1, hmap) + _list_merge_complexity(L1, l1, hmap) + _list_merge_async_complexity(L12, L12b,
                                                                                                                                                           l-l1, hmap)

                        T_rep = int(ceil(2 ** (l1 - log2(reps))))

                        tmp = Tp + log2(Tg + T_rep * T_tree)
                        # print(tmp, Tp, T_rep, T_tree)

                        if memory_access == 1:
                            tmp += log2(tmp_mem)
                        elif memory_access == 2:
                            tmp += tmp_mem/3
                        elif callable(memory_access):
                            tmp += memory_access(tmp_mem)

                        if tmp < time or (tmp == time and tmp_mem < memory):
                            time = tmp
                            memory = tmp_mem
                            params = [p, l, p1, T_tree, Tp, l1, log2(reps)]
                            tree_detail = [log2(Tg), log2(
                                2 * _list_merge_complexity(L1, l1, hmap)), log2(_list_merge_complexity(L12, l - l1, hmap))]
                            lists = [log2(L1), log2(L12), 2*log2(L12)-(l-l1)]

        for i in range(len(i_val)):
            if params[i] == i_val[i] - 1:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop == True:
            break
    par = {"l": params[1], "p": params[0], "p1": params[2],
           "l1": params[5], "reps": params[6], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par,
           "perms": params[4], "lists": lists}
    return res


def compute_mceliece_table():
    """
    """
    verbose = 1
    levels_mceliece = [[], [], []]
    for access_cost in range(3):
        for mem_indicator in range(3):
            levels_mceliece[access_cost].append([])
            for sec_level in [128, 192, 256, 257, 258]:
                switch = sec_level
                if sec_level > 256:
                    sec_level = 256

                AES_blockwidth = 128 if sec_level == 128 else 256
                AES_kilobytes = AES[str(AES_blockwidth)][str(sec_level)]
                if switch == 128:
                    c = McEliece_level1
                elif switch == 192:
                    c = McEliece_level3
                elif switch == 256:
                    c = McEliece_level5a
                elif switch == 257:
                    c = McEliece_level5b
                else:
                    c = McEliece_level5c
                n = c["n"]
                k = c["k"]-1
                w = c["w"]

                AES_kilobytes *= 2

                AES_encryptions_sec = AES_kilobytes*1024*8/AES_blockwidth

                AES_encryptions_year = AES_encryptions_sec*60*60*24*365
                AES_years = sec_level-log2(AES_encryptions_year)

                McEliece_1284_years = 16.01/365
                if mem_indicator == 0:
                    max_mem = inf
                elif mem_indicator == 1:
                    max_mem = 80-log2(n)
                else:
                    max_mem = 60-log2(n)

                McEliece_1284_complexity = bjmm_depth_2_qc_complexity(
                    1284, 1027, 24, memory_access=access_cost, enable_tmto=1)["time"]+log2(1284)
                McEliece_big_complexity = bjmm_depth_2_qc_complexity(
                    n, k, w, memory_access=access_cost, mem=max_mem, enable_tmto=1)["time"]+log2(n)

                McEliece_big_years = log2(
                    McEliece_1284_years)+McEliece_big_complexity-McEliece_1284_complexity

                if verbose:
                    if AES_years-McEliece_big_years < 0:
                        print("McEliece is", abs(
                            AES_years-McEliece_big_years), "bits harder")
                    else:
                        print("AES is", abs(
                            AES_years-McEliece_big_years), "bits harder")
                levels_mceliece[access_cost][mem_indicator].append(
                    McEliece_big_years-AES_years)


def compute_qc_table():
    """
    """
    verbose = 1
    levels_qc = {"BIKEmsg": [[], [], []],
                 "BIKEkey": [[], [], []], "HQC": [[], [], []]}
    for bike_o_hqc in ["HQC", "BIKEmsg", "BIKEkey",]:
        for access_cost in range(3):
            for mem_indicator in range(1):
                levels_qc[bike_o_hqc][access_cost].append([])
                for sec_level in [128, 192, 256]:
                    AES_blockwidth = 128 if sec_level == 128 else 256
                    AES_kilobytes = AES[str(AES_blockwidth)][str(sec_level)]
                    if sec_level == 128:
                        c = params_qc[bike_o_hqc][0]
                    elif sec_level == 192:
                        c = params_qc[bike_o_hqc][1]
                    else:
                        c = params_qc[bike_o_hqc][2]

                    n = c["n"]
                    k = c["k"]
                    if bike_o_hqc == "BIKEkey":
                        w = c["w_k"]
                    else:
                        w = c["w"]

                    AES_kilobytes *= 2

                    AES_encryptions_sec = AES_kilobytes*1024*8/AES_blockwidth
                    AES_encryptions_year = AES_encryptions_sec*60*60*24*365
                    AES_years = sec_level-log2(AES_encryptions_year)

                    max_mem = inf
                    if mem_indicator == 0:
                        max_mem = inf
                    elif mem_indicator == 1:
                        max_mem = 60 - log2(n)
                    else:
                        max_mem = 80 - log2(n)

                    Experiment_years = 38.16/24/365
                    Experiment_complexity = bjmm_depth_2_qc_complexity(
                        3138, 3138//2, 56, qc=1, memory_access=access_cost, enable_tmto=1)["time"]+log2(3138)
                    big_complexity = bjmm_depth_2_qc_complexity(
                        n, k, w, mem=max_mem, qc=0 if bike_o_hqc == "BIKEkey" else 1, memory_access=access_cost, enable_tmto=1)["time"]+log2(n)
                    if bike_o_hqc == "BIKEkey":
                        big_complexity -= log2(k)
                    big_years = log2(Experiment_years) + \
                        big_complexity-Experiment_complexity
                    if verbose:
                        if AES_years-big_years < 0:
                            # print(abs(AES_years-big_years))
                            name = bike_o_hqc
                            print(name, "is", abs(AES_years-big_years), "bits harder")
                        else:
                            print("AES is", abs(AES_years-big_years), "bits harder")
                    levels_qc[bike_o_hqc][access_cost][mem_indicator].append(
                        big_years-AES_years)


def compute_mceliece_table_vs_aes(verbose=True):
    """
    """
    tm = 0
    levels_mceliece = [[], [], []]
    for access_cost in range(3):
        for mem_indicator in range(3):
            levels_mceliece[access_cost].append([])
            for sec_level in [128, 192, 256, 257, 258]:
                switch = sec_level
                if sec_level > 256:
                    sec_level = 256

                # AES_blockwidth=128 if sec_level==128 else 256
                # AES_kilobytes=AES[str(AES_blockwidth)][str(sec_level)]
                if switch == 128:
                    c = McEliece_level1
                elif switch == 192:
                    c = McEliece_level3
                elif switch == 256:
                    c = McEliece_level5a
                elif switch == 257:
                    c = McEliece_level5b
                else:
                    c = McEliece_level5c

                n = c["n"]
                k = c["k"]-1
                w = c["w"]

                # AES_kilobytes*=2
                # AES_encryptions_sec=AES_kilobytes*1024*8/AES_blockwidth
                # AES_encryptions_year=AES_encryptions_sec*60*60*24*365
                # AES_years=sec_level-log2(AES_encryptions_year)
                AES_years = AES_GATE_COUNT_LEVEL[sec_level]
                # McEliece_1284_years=16.01/365

                if mem_indicator == 0:
                    max_mem = inf
                elif mem_indicator == 1:
                    max_mem = 80-log2(n)
                else:
                    max_mem = 60-log2(n)

                # McEliece_1284_complexity=bjmm_depth_2_qc_complexity(1284,1027,24,memory_access=access_cost,enable_tmto=1)["time"]+log2(1284)
                McEliece_big_complexity = bjmm_depth_2_qc_complexity(
                    n, k, w, memory_access=access_cost, mem=max_mem, enable_tmto=tm)["time"]+log2(n)
                # McEliece_big_years=log2(McEliece_1284_years)+McEliece_big_complexity-McEliece_1284_complexity

                McEliece_big_years = McEliece_big_complexity

                if verbose:
                    if AES_years-McEliece_big_years < 0:
                        print("McEliece is", abs(
                            AES_years-McEliece_big_years), "bits harder")
                    else:
                        print("AES is", abs(
                            AES_years-McEliece_big_years), "bits harder")
                levels_mceliece[access_cost][mem_indicator].append(
                    McEliece_big_years-AES_years)


def compute_qc_table_vs_aes(verbose=True):
    verbose = 1
    levels_qc = {"BIKEmsg": [[], [], []],
                 "BIKEkey": [[], [], []], "HQC": [[], [], []]}
    for bike_o_hqc in ["HQC", "BIKEmsg", "BIKEkey",]:
        for access_cost in range(3):
            for mem_indicator in range(1):
                levels_qc[bike_o_hqc][access_cost].append([])
                for sec_level in [128, 192, 256]:
                    if sec_level == 128:
                        c = params_qc[bike_o_hqc][0]
                    elif sec_level == 192:
                        c = params_qc[bike_o_hqc][1]
                    else:
                        c = params_qc[bike_o_hqc][2]

                    n = c["n"]
                    k = c["k"]

                    if bike_o_hqc == "BIKEkey":
                        w = c["w_k"]
                    else:
                        w = c["w"]

                    print(n, k, w)
                    # AES_kilobytes*=2
                    # AES_blockwidth=128 if sec_level==128 else 256
                    # AES_kilobytes=AES[str(AES_blockwidth)][str(sec_level)]
                    # AES_encryptions_sec=AES_kilobytes*1024*8/AES_blockwidth
                    # AES_encryptions_year=AES_encryptions_sec*60*60*24*365
                    # AES_years=sec_level-log2(AES_encryptions_year)
                    AES_years = AES_GATE_COUNT_LEVEL[sec_level]

                    if mem_indicator == 0:
                        max_mem = inf
                    elif mem_indicator == 1:
                        max_mem = 60-log2(n)
                    else:
                        max_mem == 80-log2(n)

                    # Experiment_years=38.16/24/365
                    # Experiment_complexity=bjmm_depth_2_qc_complexity(3138,3138//2,56,qc=1,memory_access=access_cost,enable_tmto=1)["time"]+log2(3138)
                    qc = 0 if bike_o_hqc == "BIKEkey" else 1

                    big_complexity = bjmm_depth_2_qc_complexity(
                        n, k, w, memory_access=access_cost, mem=max_mem, qc=qc, enable_tmto=1)["time"]+log2(n)
                    # McEliece_big_complexity=bjmm_depth_2_qc_complexity(n,k,w,memory_access=access_cost,mem=max_mem,enable_tmto=1)["time"]+log2(n)

                    if bike_o_hqc == "BIKEkey":
                        big_complexity -= log2(k)

                    # big_years = log2(Experiment_years)+big_complexity-Experiment_complexity
                    big_years = big_complexity
                    #print(big_complexity, AES_years)
                    if verbose:
                        if AES_years-big_years < 0:
                            name = bike_o_hqc
                            print(name, "is", abs(
                                AES_years-big_years), "bits harder")
                        else:
                            print("AES is", abs(AES_years-big_years), "bits harder")

                    levels_qc[bike_o_hqc][access_cost][mem_indicator].append(
                        big_years-AES_years)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SSS and decoding optimizer')
    parser.add_argument('--bcj', action='store_true',
                        help='optimize the BCJ algorithm')
    parser.add_argument('--new_bcj', action='store_true',
                        help='optimize the BCJ algorithm')
    parser.add_argument('--bbss', action='store_true',
                        help='optimize the BBSS algorithm')
    parser.add_argument('--new_bbss', action='store_true',
                        help='optimize the BBSS algorithm')

    parser.add_argument('--bjmm', action='store_true',
                        help='optimize the BJMM algorithm')
    parser.add_argument('--new_bjmm', action='store_true',
                        help='optimize the new BJMM algorithm')
    parser.add_argument('--mmt', action='store_true',
                        help='optimize the MMT algorithm')
    parser.add_argument('--new_mmt', action='store_true',
                        help='optimize the new MMT algorithm')

    parser.add_argument('-k', type=float, default=0.488,
                        help='code dimension, only for bjmm/mmt')
    parser.add_argument('-w', type=float, default=Hi(1-0.488)/2,
                        help='optimize the new MMT algorithm')

    parser.add_argument('--verbose', action='store_true',
                        help='verbose output')
    parser.add_argument('--retries', type=int, default=10000,
                        help='number of retries per optimisation step')
    parser.add_argument('--memlimit', action='store_true',
                        help='optimize under memory limitation')
    parser.add_argument('--rate', action='store_true',
                        help='optimize under memory limitation')

    args = parser.parse_args()

    if args.rate:
        if args.mmt:
            optimize_k_mmt()
        if args.new_mmt:
            optimize_k_new_mmt()
        if args.bjmm:
            optimize_k_bjmm()
        if args.new_bjmm:
            optimize_k_new_bjmm()

    if args.memlimit:
        # global NOLOG
        NOLOG = True

        if args.mmt:
            optimize_mem_mmt()
        if args.new_mmt:
            optimize_mem_new_mmt()
        if args.bjmm:
            optimize_mem_bjmm()
        if args.new_bjmm:
            optimize_mem_new_bjmm()

        bbss = False
        if args.bbss or args.new_bbss:
            bbss = True

        new = False
        if args.new_bbss or args.new_bcj:
            new = True

        BCJ_BBSS_memlimit(bbss, new)
        exit(0)

    memlimit = 1.
    if args.bcj:
        optimize_bcj(False, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.new_bcj:
        optimize_bcj(True, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.bbss:
        optimize_bbss(False, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.new_bbss:
        optimize_bbss(True, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.bjmm:
        optimize_bjmm(k=args.k, w=args.w, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.new_bjmm:
        optimize_new_bjmm(k=args.k, w=args.w, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.mmt:
        optimize_mmt(k=args.k, w=args.w, verb=args.verbose, iters=args.retries, membound=memlimit)
    if args.new_mmt:
        optimize_new_mmt(k=args.k, w=args.w, verb=args.verbose, iters=args.retries, membound=memlimit)

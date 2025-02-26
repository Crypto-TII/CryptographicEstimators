#from .theoretical_estimates import *
from math import inf, ceil, log2, comb
from prettytable import PrettyTable
#from progress.bar import Bar
from scipy.special import binom as binom_sp
from scipy.optimize import fsolve
from warnings import filterwarnings

filterwarnings("ignore", category=RuntimeWarning)


def binom(n, k):
    return comb(int(n), int(k))


def __truncate(x, precision):
    """
    Truncates a float

    INPUT:

    - ``x`` -- value to be truncated
    - ``precision`` -- number of decimal places to after which the ``x`` is truncated

    """

    return float(int(x * 10 ** precision) / 10 ** precision)


def __concat_pretty_tables(t1, t2):
    v = t1.split("\n")
    v2 = t2.split("\n")
    vnew = ""
    for i in range(len(v)):
        vnew += v[i] + v2[i][1:] + "\n"
    return vnew[:-1]


def __round_or_truncate_to_given_precision(T, M, truncate, precision):
    if truncate:
        T, M = __truncate(T, precision), __truncate(M, precision)
    else:
        T, M = round(T, precision), round(M, precision)
    return '{:.{p}f}'.format(T, p=precision), '{:.{p}f}'.format(M, p=precision)


def __memory_access_cost(mem, memory_access):
    if memory_access == 0:
        return 0
    elif memory_access == 1:
        return log2(mem)
    elif memory_access == 2:
        return mem / 2
    elif memory_access == 3:
        return mem / 3
    elif callable(memory_access):
        return memory_access(mem)
    return 0


def _gaussian_elimination_complexity(n, k, r):
    """
    Complexity estimate of Gaussian elimination routine

    INPUT:

    - ``n`` -- Row additons are perfomed on ``n`` coordinates
    - ``k`` -- Matrix consists of ``n-k`` rows
    - ``r`` -- Blocksize of method of the four russian for inversion, default is zero

    [Bar07]_ Bard, G.V.: Algorithms for solving linear and polynomial systems of equations over finite fields
    with applications to cryptanalysis. Ph.D. thesis (2007)

    [BLP08] Bernstein, D.J., Lange, T., Peters, C.: Attacking and defending the mceliece cryptosystem.
    In: International Workshop on Post-Quantum Cryptography. pp. 31–46. Springer (2008)

    EXAMPLES::

        >>> from .estimator import _gaussian_elimination_complexity
        >>> _gaussian_elimination_complexity(n=100,k=20,r=1) # doctest: +SKIP

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

    EXAMPLES::

        >>> from .estimator import _mem_matrix
        >>> _mem_matrix(n=100,k=20,r=0) # doctest: +SKIP

    """
    return n - k + 2 ** r


def _list_merge_complexity(L, l, hmap):
    """
    Complexity estimate of merging two lists exact

    INPUT:

    - ``L`` -- size of lists to be merged
    - ``l`` -- amount of bits used for matching
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        >>> from .estimator import _list_merge_complexity
        >>> _list_merge_complexity(L=2**16,l=16,hmap=1) # doctest: +SKIP

    """

    if L == 1:
        return 1
    if not hmap:
        return max(1, 2 * int(log2(L)) * L + L ** 2 // 2 ** l)
    else:
        return 2 * L + L ** 2 // 2 ** l


def _indyk_motwani_complexity(L, l, w, hmap):
    """
    Complexity of Indyk-Motwani nearest neighbor search

    INPUT:

    - ``L`` -- size of lists to be matched
    - ``l`` -- amount of bits used for matching
    - ``w`` -- target weight
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        >>> from .estimator import _indyk_motwani_complexity
        >>> _indyk_motwani_complexity(L=2**16,l=16,w=2,hmap=1) # doctest: +SKIP

    """

    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    lam = max(0, int(min(ceil(log2(L)), l - 2 * w)))
    return binom(l, lam) // binom(l - w, lam) * _list_merge_complexity(L, lam, hmap)


def _mitm_nn_complexity(L, l, w, hmap):
    """
    Complexity of Indyk-Motwani nearest neighbor search

    INPUT:

    - ``L`` -- size of lists to be matched
    - ``l`` -- amount of bits used for matching
    - ``w`` -- target weight
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        >>> from .estimator import _indyk_motwani_complexity
        >>> _indyk_motwani_complexity(L=2**16,l=16,w=2,hmap=1) # doctest: +SKIP

    """
    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    L1 = L * binom(l / 2, w / 2)
    return _list_merge_complexity(L1, l, hmap)


def prange_complexity(n, k, w, mem=inf, memory_access=0):
    """
    Complexity estimate of Prange's ISD algorithm

    [Pra62] Prange, E.: The use of information sets in decoding cyclic codes. IRE Transactions
                        on Information Theory 8(5), 5–9 (1962)

    expected weight distribution::

        +--------------------------------+-------------------------------+
        | <----------+ n - k +---------> | <----------+ k +------------> |
        |                w               |              0                |
        +--------------------------------+-------------------------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2(bits)), default unlimited
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import prange_complexity
        >>> prange_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """

    solutions = max(0, log2(binom(n, w)) - (n - k))

    r = _optimize_m4ri(n, k, mem)
    Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
    Tg = log2(_gaussian_elimination_complexity(n, k, r))
    time = Tp + Tg
    memory = log2(_mem_matrix(n, k, r))

    time += __memory_access_cost(memory, memory_access)

    params = [r]

    par = {"r": params[0]}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def stern_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of Stern's ISD algorithm

    [Ste88] Stern, J.:  A method for finding codewords of small weight. In: International
    Colloquium on Coding Theory and Applications. pp. 106–113. Springer (1988)

    [BLP08] Bernstein, D.J., Lange, T., Peters, C.: Attacking and defending the mceliece cryptosystem.
    In: International Workshop on Post-Quantum Cryptography. pp. 31–46. Springer (2008)

    expected weight distribution::

        +-------------------------+---------+-------------+-------------+
        | <----+ n - k - l +----> |<-- l -->|<--+ k/2 +-->|<--+ k/2 +-->|
        |          w - 2p         |    0    |      p      |      p      |
        +-------------------------+---------+-------------+-------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import stern_complexity
        >>> stern_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """

    solutions = max(0, log2(binom(n, w)) - (n - k))

    r = _optimize_m4ri(n, k, mem)
    time = inf
    memory = 0
    params = [-1 for i in range(2)]
    i_val = [20]
    i_val_inc = [10]
    k1 = k // 2
    while True:
        stop = True
        for p in range(min(k1, w // 2, i_val[0])):
            L1 = binom(k1, p)
            l_val = int(log2(L1))
            if log2(L1) > time:
                continue
            for l in range(max(l_val - i_val_inc[0], 0), l_val + i_val_inc[0]):

                tmp_mem = log2(2 * L1 + _mem_matrix(n, k, r))
                if tmp_mem > mem:
                    continue

                Tp = max(0,
                         log2(binom(n, w)) - log2(binom(n - k, w - 2 * p)) - log2(binom(k1, p) ** 2) - solutions)

                # We use Indyk-Motwani (IM) taking into account the possibility of multiple existing solutions
                # with correct weight distribution, decreasing the amount of necessary projections
                # remaining_sol denotes the number of expected solutions per permutation
                # l_part_iterations is the expected number of projections need by IM to find one of those solutions

                remaining_sol = (binom(n - k, w - 2 * p) * binom(k1, p) ** 2 * binom(n, w) // 2 ** (n - k)) // binom(n,
                                                                                                                     w)
                l_part_iterations = binom(n - k, w - 2 * p) // binom(n - k - l, w - 2 * p)

                if remaining_sol > 0:
                    l_part_iterations //= max(1, remaining_sol)
                    l_part_iterations = max(1, l_part_iterations)

                Tg = _gaussian_elimination_complexity(n, k, r)
                tmp = Tp + log2(Tg + _list_merge_complexity(L1, l, hmap) * l_part_iterations)

                tmp += __memory_access_cost(tmp_mem, memory_access)

                time = min(time, tmp)

                if tmp == time:
                    memory = tmp_mem
                    params = [p, l]

        for i in range(len(i_val)):
            if params[i] == i_val[i] - 1:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop:
            break

    par = {"l": params[1], "p": params[0]}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def dumer_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of Dumer's ISD algorithm

    [Dum91] Dumer, I.:  On minimum distance decoding of linear codes. In: Proc. 5th Joint
                        Soviet-Swedish Int. Workshop Inform. Theory. pp. 50–52 (1991)

    expected weight distribution::

        +--------------------------+------------------+-------------------+
        | <-----+ n - k - l +----->|<-- (k + l)/2 +-->|<--+ (k + l)/2 +-->|
        |           w - 2p         |       p          |        p          |
        +--------------------------+------------------+-------------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import dumer_complexity
        >>> dumer_complexity(n=100,k=50,w=10) # doctest: +SKIP


    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [10, 40]
    i_val_inc = [10, 10]
    params = [-1 for _ in range(2)]
    while True:
        stop = True
        for p in range(min(w // 2, i_val[0])):
            for l in range(min(n - k - (w - p), i_val[1])):
                k1 = (k + l) // 2
                L1 = binom(k1, p)
                if log2(L1) > time:
                    continue

                tmp_mem = log2(2 * L1 + _mem_matrix(n, k, r))
                if tmp_mem > mem:
                    continue

                Tp = max(log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p)) - log2(binom(k1, p) ** 2) - solutions, 0)
                Tg = _gaussian_elimination_complexity(n, k, r)
                tmp = Tp + log2(Tg + _list_merge_complexity(L1, l, hmap))

                tmp += __memory_access_cost(tmp_mem, memory_access)

                time = min(time, tmp)
                if tmp == time:
                    memory = tmp_mem
                    params = [p, l]

        for i in range(len(i_val)):
            if params[i] == i_val[i] - 1:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop:
            break

    par = {"l": params[1], "p": params[0]}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def ball_collision_decoding_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of the ball collision decodding algorithm

    [BLP11] Bernstein, D.J., Lange, T., Peters, C.:  Smaller decoding exponents: ball-collision decoding.
    In: Annual Cryptology Conference. pp. 743–760. Springer (2011)

    expected weight distribution::

        +------------------+---------+---------+-------------+-------------+
        | <-+ n - k - l +->|<- l/2 ->|<- l/2 ->|<--+ k/2 +-->|<--+ k/2 +-->|
        |    w - 2p - 2pl  |   pl    |   pl    |      p      |      p      |
        +------------------+---------+---------+-------------+-------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import ball_collision_decoding_complexity
        >>> ball_collision_decoding_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [10, 80, 4]
    i_val_inc = [10, 10, 10]
    params = [-1 for _ in range(3)]
    k1 = k // 2
    while True:
        stop = True
        for p in range(min(w // 2, i_val[0])):
            for l in range(min(n - k - (w - 2 * p), i_val[1])):
                for pl in range(min(i_val[2], (w - 2 * p) // 2, l // 2 + 1)):
                    L1 = binom(k1, p)
                    L1 *= max(1, binom(l // 2, pl))
                    if log2(L1) > time:
                        continue

                    tmp_mem = log2(2 * L1 + _mem_matrix(n, k, r))
                    if tmp_mem > mem:
                        continue

                    Tp = max(
                        log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p - 2 * pl)) - 2 * log2(
                            binom(k1, p)) - 2 * log2(
                            binom(l // 2, pl)) - solutions, 0)
                    Tg = _gaussian_elimination_complexity(n, k, r)
                    tmp = Tp + log2(Tg + _list_merge_complexity(L1, l, hmap))

                    tmp += __memory_access_cost(tmp_mem, memory_access)

                    time = min(time, tmp)
                    if tmp == time:
                        memory = tmp_mem
                        params = [p, pl, l]

        for i in range(len(i_val)):
            if params[i] == i_val[i] - 1:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop:
            break

    par = {"l": params[2], "p": params[0], "pl": params[1]}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def bjmm_complexity(n, k, w, mem=inf, hmap=1, only_depth_two=0, memory_access=0):
    """
    Complexity estimate of BJMM algorithm

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

    EXAMPLES::

        >>> from .estimator import bjmm_complexity
        >>> bjmm_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    d2 = bjmm_depth_2_complexity(n, k, w, mem, hmap, memory_access)
    d3 = bjmm_depth_3_complexity(n, k, w, mem, hmap, memory_access)
    return d2 if d2["time"] < d3["time"] or only_depth_two else d3


def bjmm_depth_2_complexity(n, k, w, mem=inf, hmap=1, memory_access=0, mmt=0):
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

    EXAMPLES::

        >>> from .estimator import bjmm_depth_2_complexity
        >>> bjmm_depth_2_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [35, 500, 35]
    i_val_inc = [10, 10, 10]
    params = [-1 for _ in range(3)]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), min(i_val[1], n - k))):
                for p1 in range(max(params[2] - i_val_inc[2] // 2, (p + 1) // 2), min(w, i_val[2])):
                    if mmt and p1 != p // 2:
                        continue
                    k1 = (k + l) // 2
                    L1 = binom(k1, p1)
                    if log2(L1) > time:
                        continue

                    if k1 - p < p1 - p / 2:
                        continue
                    reps = (binom(p, p / 2) * binom(k1 - p, p1 - p / 2)) ** 2

                    l1 = int(ceil(log2(reps)))

                    if l1 > l:
                        continue

                    L12 = max(1, L1 ** 2 // 2 ** l1)

                    tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r))
                    if tmp_mem > mem:
                        continue

                    Tp = max(log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p)) - 2 * log2(
                        binom((k + l) // 2, p)) - solutions, 0)
                    Tg = _gaussian_elimination_complexity(n, k, r)
                    T_tree = 2 * _list_merge_complexity(L1, l1, hmap) + _list_merge_complexity(L12,
                                                                                               l - l1,
                                                                                               hmap)
                    T_rep = int(ceil(2 ** (l1 - log2(reps))))

                    tmp = Tp + log2(Tg + T_rep * T_tree)
                    tmp += __memory_access_cost(tmp_mem, memory_access)

                    time = min(tmp, time)
                    if tmp == time:
                        memory = tmp_mem
                        params = [p, l, p1]

        for i in range(len(i_val)):
            if params[i] == i_val[i] - 1:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop:
            break

    par = {"l": params[1], "p": params[0], "p1": params[2], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def bjmm_depth_3_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of BJMM algorithm in depth 3

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

    EXAMPLES::

        >>> from .estimator import bjmm_depth_3_complexity
        >>> bjmm_depth_3_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    params = [-1 for _ in range(4)]
    i_val = [25, 400, 20, 10]
    i_val_inc = [10, 10, 10, 10]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2 + (params[0] - i_val_inc[0] // 2) % 2, 0),
                       min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), min(n - k, i_val[1]))):
                k1 = (k + l) // 2
                for p2 in range(max(params[2] - i_val_inc[2] // 2, p // 2 + ((p // 2) % 2)), i_val[2], 2):
                    for p1 in range(max(params[3] - i_val_inc[3] // 2, (p2 + 1) // 2), i_val[3]):
                        L1 = binom(k1, p1)

                        if log2(L1) > time:
                            continue

                        reps1 = (binom(p2, p2 / 2) * binom(k1 - p2, p1 - p2 / 2)) ** 2
                        l1 = int((log2(reps1))) if reps1 != 1 else 0

                        L12 = max(1, L1 ** 2 // 2 ** l1)
                        reps2 = (binom(p, p / 2) * binom(k1 - p, p2 - p / 2)) ** 2
                        l2 = int(ceil(log2(reps2))) if reps2 != 1 else 0

                        L1234 = max(1, L12 ** 2 // 2 ** (l2 - l1))
                        tmp_mem = log2((2 * L1 + L12 + L1234) + _mem_matrix(n, k, r))
                        if tmp_mem > mem:
                            continue

                        Tp = max(log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p)) - 2 * log2(
                            binom((k + l) // 2, p)) - solutions, 0)
                        Tg = _gaussian_elimination_complexity(n, k, r)
                        T_tree = 4 * _list_merge_complexity(L1, l1, hmap) + 2 * _list_merge_complexity(L12,
                                                                                                       l2 - l1,
                                                                                                       hmap) + _list_merge_complexity(
                            L1234,
                            l - l2,
                            hmap)
                        T_rep = int(ceil(2 ** (3 * max(0, l1 - log2(reps1)) + max(0, l2 - log2(reps2)))))

                        tmp = Tp + log2(Tg + T_rep * T_tree)
                        tmp += __memory_access_cost(tmp_mem, memory_access)

                        if tmp < time:
                            time = tmp
                            memory = tmp_mem
                            params = [p, l, p2, p1]

        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                stop = False
                i_val[i] += i_val_inc[i]

        if stop:
            break

    par = {"l": params[1], "p": params[0], "p1": params[3], "p2": params[2], "depth": 3}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def bjmm_depth_2_partially_disjoint_weight_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of BJMM algorithm in depth 2 using partially disjoint weight, applying explicit MitM-NN search on second level

    [MMT11] May, A., Meurer, A., Thomae, E.: Decoding random linear codes in  2^(0.054n). In: International Conference
    on the Theory and Application of Cryptology and Information Security. pp. 107–124. Springer (2011)

    [BJMM12] Becker, A., Joux, A., May, A., Meurer, A.: Decoding random binary linear codes in 2^(n/20): How 1+ 1= 0
    improves information set decoding. In: Annual international conference on the theory and applications of
    cryptographic techniques. pp. 520–536. Springer (2012)

    [EssBel21] Esser, A. and Bellini, E.: Syndrome Decoding Estimator. In: IACR Cryptol. ePrint Arch. 2021 (2021), 1243

    expected weight distribution::

        +--------------------------+--------------------+--------------------+--------+--------+
        | <-+ n - k - l1 - 2 l2 +->|<-+ (k + l1) / 2 +->|<-+ (k + l1) / 2 +->|   l2   |   l2   |
        |       w - 2 p - 2 w2     |         p          |         p          |   w2   |   w2   |
        +--------------------------+--------------------+--------------------+--------+--------+


    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import bjmm_depth_2_partially_disjoint_weight_complexity
        >>> bjmm_depth_2_partially_disjoint_weight_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [30, 25, 5]
    i_val_inc = [10, 10, 10, 10, 10]
    params = [-1 for _ in range(5)]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for p1 in range(max(params[1] - i_val_inc[1] // 2, (p + 1) // 2), min(w, i_val[1])):
                for w2 in range(max(params[2] - i_val_inc[2] // 2, 0), min(w - p1, i_val[2])):

                    #############################################################################################
                    ######choose start value for l1 close to the logarithm of the number of representations######
                    #############################################################################################
                    try:
                        f = lambda x: log2((binom(p, p // 2) * binom_sp((k + x) / 2 - p, p1 - p // 2))) * 2 - x
                        l1_val = int(fsolve(f, 0)[0])
                    except:
                        continue
                    if f(l1_val) < 0 or f(l1_val) > 1:
                        continue
                        #############################################################################################

                    for l1 in range(max(0, l1_val - i_val_inc[3] // 2), l1_val + i_val_inc[3] // 2):
                        k1 = (k + l1) // 2
                        reps = (binom(p, p // 2) * binom(k1 - p, p1 - p // 2)) ** 2

                        L1 = binom(k1, p1)
                        if log2(L1) > time:
                            continue

                        L12 = L1 ** 2 // 2 ** l1
                        L12 = max(L12, 1)
                        tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r))
                        if tmp_mem > mem:
                            continue

                        #################################################################################
                        #######choose start value for l2 such that resultlist size is close to L12#######
                        #################################################################################
                        try:
                            f = lambda x: log2(int(L12)) + int(2) * log2(binom_sp(x, int(w2))) - int(2) * x
                            l2_val = int(fsolve(f, 0)[0])
                        except:
                            continue
                        if f(l2_val) < 0 or f(l2_val) > 1:
                            continue
                        ################################################################################
                        l2_min = w2
                        l2_max = (n - k - l1 - (w - 2 * p - 2 * w2)) // 2
                        l2_range = [l2_val - i_val_inc[4] // 2, l2_val + i_val_inc[4] // 2]
                        for l2 in range(max(l2_min, l2_range[0]), min(l2_max, l2_range[1])):
                            Tp = max(
                                log2(binom(n, w)) - log2(binom(n - k - l1 - 2 * l2, w - 2 * p - 2 * w2)) - 2 * log2(
                                    binom(k1, p)) - 2 * log2(binom(l2, w2)) - solutions, 0)
                            Tg = _gaussian_elimination_complexity(n, k, r)

                            T_tree = 2 * _list_merge_complexity(L1, l1, hmap) + _mitm_nn_complexity(L12, 2 * l2, 2 * w2,
                                                                                                    hmap)
                            T_rep = int(ceil(2 ** max(l1 - log2(reps), 0)))

                            tmp = Tp + log2(Tg + T_rep * T_tree)
                            tmp += __memory_access_cost(tmp_mem, memory_access)

                            time = min(tmp, time)

                            if tmp == time:
                                memory = tmp_mem
                                params = [p, p1, w2, l2, l1]

        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                i_val[i] += i_val_inc[i]
                stop = False
        if stop:
            break
        break

    par = {"l1": params[4], "p": params[0], "p1": params[1], "depth": 2, "l2": params[3], "w2": params[2]}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def bjmm_depth_2_disjoint_weight_complexity(n, k, w, mem=inf, hmap=1, p_range=[0, 25], memory_access=0):
    """
    Complexity estimate of May-Ozerov algorithm in depth 2 using Indyk-Motwani for NN search


    [MMT11] May, A., Meurer, A., Thomae, E.: Decoding random linear codes in  2^(0.054n). In: International Conference
    on the Theory and Application of Cryptology and Information Security. pp. 107–124. Springer (2011)

    [BJMM12] Becker, A., Joux, A., May, A., Meurer, A.: Decoding random binary linear codes in 2^(n/20): How 1+ 1= 0
    improves information set decoding. In: Annual international conference on the theory and applications of
    cryptographic techniques. pp. 520–536. Springer (2012)

    [EssBel21] Esser, A. and Bellini, E.: Syndrome Decoding Estimator. In: IACR Cryptol. ePrint Arch. 2021 (2021), 1243
    
    expected weight distribution::

        +---------------------------+-------------+------------+----------+----------+----------+----------+
        |<-+ n - k - 2 l1 - 2 l2 +->|<-+ k / 2 +->|<-+ k / 2 ->|<-+ l1 +->|<-+ l1 +->|<-+ l2 +->|<-+ l2 +->|
        |   w - 2 p - 2 w1 - 2 w2   |      p      |      p     |    w1    |    w1    |    w2    |    w2    |
        +---------------------------+-------------+------------+----------+----------+----------+----------+


    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``p_range`` -- interval in which the parameter p is searched (default: [0, 25], helps speeding up computation)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import bjmm_depth_2_disjoint_weight_complexity
        >>> bjmm_depth_2_disjoint_weight_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """

    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k)
    i_val = [p_range[1], 20, 10, 10, 5]
    i_val_inc = [10, 10, 10, 10, 10, 10, 10]
    params = [-1 for _ in range(7)]
    while True:
        stop = True
        for p in range(max(p_range[0], params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for p1 in range(max(params[1] - i_val_inc[1] // 2, (p + 1) // 2), min(w, i_val[1])):
                s = max(params[2] - i_val_inc[2] // 2, 0)
                for w1 in range(s - (s % 2), min(w // 2 - p, i_val[2]), 2):
                    for w11 in range(max(params[3] - i_val_inc[3] // 2, (w1 + 1) // 2), min(w, i_val[3])):
                        for w2 in range(max(params[4] - i_val_inc[4] // 2, 0), min(w // 2 - p - w1, i_val[4])):
                            ##################################################################################
                            ######choose start value for l1 such that representations cancel out exactly######
                            ##################################################################################
                            try:
                                f = lambda x: 2 * log2((binom(p, p // 2) * binom(k // 2 - p, p1 - p // 2)) * (
                                        binom_sp(x, w1 // 2) * binom_sp(x - w1, w11 - w1 // 2)) + 1) - 2 * x
                                l1_val = int(
                                    fsolve(f, 2 * log2((binom(p, p // 2) * binom(k // 2 - p, p1 - p // 2))))[0])
                            except:
                                continue
                            if f(l1_val) < 0 or f(l1_val) > 10:
                                continue
                            #################################################################################

                            for l1 in range(max(l1_val - i_val_inc[5], w1, w11), l1_val + i_val_inc[5]):
                                k1 = k // 2
                                reps = (binom(p, p // 2) * binom(k1 - p, p1 - p // 2)) ** 2 * (
                                        binom(w1, w1 // 2) * binom(l1 - w1, w11 - w1 // 2)) ** 2
                                reps = max(reps, 1)
                                L1 = binom(k1, p1)
                                if log2(L1) > time:
                                    continue

                                L12 = L1 ** 2 * binom(l1, w11) ** 2 // 2 ** (2 * l1)
                                L12 = max(L12, 1)
                                tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r))
                                if tmp_mem > mem:
                                    continue

                                #################################################################################
                                #######choose start value for l2 such that resultlist size is equal to L12#######
                                #################################################################################
                                try:
                                    f = lambda x: log2(L12) + 2 * log2(binom_sp(x, w2) + 1) - 2 * x
                                    l2_val = int(fsolve(f, 50)[0])
                                except:
                                    continue
                                if f(l2_val) < 0 or f(l2_val) > 10:
                                    continue
                                ################################################################################
                                l2_max = (n - k - 2 * l1 - (w - 2 * p - 2 * w1 - 2 * w2)) // 2
                                l2_min = w2
                                l2_range = [l2_val - i_val_inc[6] // 2, l2_val + i_val_inc[6] // 2]
                                for l2 in range(max(l2_min, l2_range[0]), min(l2_max, l2_range[1])):
                                    Tp = max(
                                        log2(binom(n, w)) - log2(
                                            binom(n - k - 2 * l1 - 2 * l2, w - 2 * p - 2 * w1 - 2 * w2)) - 2 * log2(
                                            binom(k1, p)) - 2 * log2(binom(l1, w1)) - 2 * log2(
                                            binom(l2, w2)) - solutions, 0)
                                    Tg = _gaussian_elimination_complexity(n, k, r)

                                    T_tree = 2 * _mitm_nn_complexity(L1, 2 * l1, 2 * w11, hmap) + _mitm_nn_complexity(
                                        L12, 2 * l2, 2 * w2, hmap)
                                    T_rep = int(ceil(2 ** max(2 * l1 - log2(reps), 0)))

                                    tmp = Tp + log2(Tg + T_rep * T_tree)
                                    tmp += __memory_access_cost(tmp_mem, memory_access)

                                    time = min(tmp, time)

                                    if tmp == time:
                                        memory = tmp_mem
                                        params = [p, p1, w1, w11, w2, l2, l1 + l2]

        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                i_val[i] += i_val_inc[i]
                stop = False
        if stop:
            break
        break
    par = {"l": params[6], "p": params[0], "p1": params[1], "w1": params[2], "w11": params[3], "l2": params[5],
           "w2": params[4], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def both_may_depth_2_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of Both-May algorithm in depth 2 using Indyk-Motwani and MitM for NN search

    [BotMay18] Both, L., May, A.: Decoding linear codes with high error rate and its impact for LPN security. In:
    International Conference on Post-Quantum Cryptography. pp. 25--46. Springer (2018)

    expected weight distribution::

        +-------------------+---------+-------------------+-------------------+
        | <--+ n - k - l+-->|<-+ l +->|<----+ k / 2 +---->|<----+ k / 2 +---->|
        |     w - w2 - 2p   |    w2   |         p         |         p         |
        +-------------------+---------+-------------------+-------------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import both_may_depth_2_complexity
        >>> both_may_depth_2_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """

    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [20, 160, 5, 4, 15]
    i_val_inc = [10, 10, 10, 6, 6]
    params = [-1 for _ in range(5)]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), i_val[1])):
                for w1 in range(max(params[2] - i_val_inc[2] // 2, 0), min(w, l + 1, i_val[2])):
                    for w2 in range(max(params[3] - i_val_inc[3] // 2, 0), min(w - 2 * p, l + 1, i_val[3], 2 * w1), 2):
                        for p1 in range(max(params[4] - i_val_inc[4] // 2, (p + 1) // 2), min(w, i_val[4])):
                            k1 = (k) // 2
                            reps = (binom(p, p / 2) * binom(k1 - p, p1 - p / 2)) ** 2 * binom(w2, w2 / 2) * binom(
                                l - w2,
                                w1 - w2 / 2)
                            reps = 1 if reps == 0 else reps
                            L1 = binom(k1, p1)

                            if log2(L1) > time:
                                continue

                            L12 = max(1, L1 ** 2 * binom(l, w1) // 2 ** l)

                            tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r))
                            if tmp_mem > mem:
                                continue
                            Tp = max(log2(binom(n, w)) - log2(binom(n - k - l, w - w2 - 2 * p)) - 2 * log2(
                                binom(k1, p)) - log2(binom(l, w2)) - solutions, 0)
                            Tg = _gaussian_elimination_complexity(n, k, r)

                            first_level_nn = _indyk_motwani_complexity(L1, l, w1, hmap)
                            second_level_nn = _indyk_motwani_complexity(L12, n - k - l, w - 2 * p - w2, hmap)
                            T_tree = 2 * first_level_nn + second_level_nn
                            T_rep = int(ceil(2 ** max(0, l - log2(reps))))

                            tmp = Tp + log2(Tg + T_rep * T_tree)
                            tmp += __memory_access_cost(tmp_mem, memory_access)

                            time = min(tmp, time)

                            if tmp == time:
                                memory = tmp_mem
                                params = [p, l, w1, w2, p1, log2(L1), log2(L12)]

        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                i_val[i] += i_val_inc[i]
                stop = False
        if stop:
            break

    par = {"l": params[1], "p": params[0], "p1": params[4], "w1": params[2], "w2": params[3], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def may_ozerov_complexity(n, k, w, mem=inf, hmap=1, only_depth_two=0, memory_access=0):
    """
    Complexity estimate of May-Ozerov algorithm using Indyk-Motwani for NN search

    [MayOze15] May, A. and Ozerov, I.: On computing nearest neighbors with applications to decoding of binary linear codes.
    In: Annual International Conference on the Theory and Applications of Cryptographic Techniques. pp. 203--228. Springer (2015)

    expected weight distribution::

        +-------------------------+---------------------+---------------------+
        | <-----+ n - k - l+----->|<--+ (k + l) / 2 +-->|<--+ (k + l) / 2 +-->|
        |           w - 2p        |        p            |        p            |
        +-------------------------+---------------------+---------------------+


    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import may_ozerov_complexity
        >>> may_ozerov_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    d2 = may_ozerov_depth_2_complexity(n, k, w, mem, hmap, memory_access)
    d3 = may_ozerov_depth_3_complexity(n, k, w, mem, hmap, memory_access)
    return d2 if d2["time"] < d3["time"] or only_depth_two else d3


def may_ozerov_depth_2_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of May-Ozerov algorithm in depth 2 using Indyk-Motwani for NN search

    [MayOze15] May, A. and Ozerov, I.: On computing nearest neighbors with applications to decoding of binary linear codes.
    In: Annual International Conference on the Theory and Applications of Cryptographic Techniques. pp. 203--228. Springer (2015)

    expected weight distribution::

        +-------------------------+---------------------+---------------------+
        | <-----+ n - k - l+----->|<--+ (k + l) / 2 +-->|<--+ (k + l) / 2 +-->|
        |           w - 2p        |        p            |        p            |
        +-------------------------+---------------------+---------------------+


    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import may_ozerov_depth_2_complexity
        >>> may_ozerov_depth_2_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [30, 300, 25]
    i_val_inc = [10, 10, 10]
    params = [-1 for _ in range(3)]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), i_val[1])):
                for p1 in range(max(params[2] - i_val_inc[2] // 2, (p + 1) // 2), min(w, i_val[2])):
                    k1 = (k + l) // 2
                    reps = (binom(p, p // 2) * binom(k1 - p, p1 - p // 2)) ** 2

                    L1 = binom(k1, p1)
                    if log2(L1) > time:
                        continue

                    L12 = L1 ** 2 // 2 ** l
                    L12 = max(L12, 1)
                    tmp_mem = log2((2 * L1 + L12) + _mem_matrix(n, k, r))
                    if tmp_mem > mem:
                        continue

                    Tp = max(
                        log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p)) - 2 * log2(binom(k1, p)) - solutions, 0)
                    Tg = _gaussian_elimination_complexity(n, k, r)

                    T_tree = 2 * _list_merge_complexity(L1, l, hmap) + _indyk_motwani_complexity(L12,
                                                                                                 n - k - l,
                                                                                                 w - 2 * p,
                                                                                                 hmap)
                    T_rep = int(ceil(2 ** max(l - log2(reps), 0)))

                    tmp = Tp + log2(Tg + T_rep * T_tree)
                    tmp += __memory_access_cost(tmp_mem, memory_access)

                    time = min(tmp, time)

                    if tmp == time:
                        memory = tmp_mem
                        params = [p, l, p1]

        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                i_val[i] += i_val_inc[i]
                stop = False
        if stop:
            break
        break

    par = {"l": params[1], "p": params[0], "p1": params[2], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par}
    return res


def may_ozerov_depth_3_complexity(n, k, w, mem=inf, hmap=1, memory_access=0):
    """
    Complexity estimate of May-Ozerov algorithm in depth 3 using Indyk-Motwani for NN search

    [MayOze15] May, A. and Ozerov, I.: On computing nearest neighbors with applications to decoding of binary linear codes.
    In: Annual International Conference on the Theory and Applications of Cryptographic Techniques. pp. 203--228. Springer (2015)

    expected weight distribution::

        +-------------------------+---------------------+---------------------+
        | <-----+ n - k - l+----->|<--+ (k + l) / 2 +-->|<--+ (k + l) / 2 +-->|
        |           w - 2p        |        p            |        p            |
        +-------------------------+---------------------+---------------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``mem`` -- upper bound on the available memory (as log2), default unlimited
    - ``hmap`` -- indicates if hashmap is being used (default: true)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import may_ozerov_depth_3_complexity
        >>> may_ozerov_depth_3_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """
    solutions = max(0, log2(binom(n, w)) - (n - k))
    time = inf
    memory = 0
    r = _optimize_m4ri(n, k, mem)

    i_val = [20, 200, 20, 10]
    i_val_inc = [10, 10, 10, 10]
    params = [-1 for _ in range(4)]
    while True:
        stop = True
        for p in range(max(params[0] - i_val_inc[0] // 2, 0), min(w // 2, i_val[0]), 2):
            for l in range(max(params[1] - i_val_inc[1] // 2, 0), min(n - k - (w - 2 * p), i_val[1])):
                k1 = (k + l) // 2
                for p2 in range(max(params[2] - i_val_inc[2] // 2, p // 2 + ((p // 2) % 2)), p + i_val[2], 2):
                    for p1 in range(max(params[3] - i_val_inc[3] // 2, (p2 + 1) // 2),
                                    min(p2 + i_val[3], k1 - p2 // 2)):
                        L1 = binom(k1, p1)
                        if log2(L1) > time:
                            continue

                        reps1 = (binom(p2, p2 // 2) * binom(k1 - p2, p1 - p2 // 2)) ** 2
                        l1 = int(ceil(log2(reps1)))

                        if l1 > l:
                            continue
                        L12 = max(1, L1 ** 2 // 2 ** l1)
                        reps2 = (binom(p, p // 2) * binom(k1 - p, p2 - p // 2)) ** 2

                        L1234 = max(1, L12 ** 2 // 2 ** (l - l1))
                        tmp_mem = log2((2 * L1 + L12 + L1234) + _mem_matrix(n, k, r))
                        if tmp_mem > mem:
                            continue

                        Tp = max(
                            log2(binom(n, w)) - log2(binom(n - k - l, w - 2 * p)) - 2 * log2(binom(k1, p)) - solutions,
                            0)
                        Tg = _gaussian_elimination_complexity(n, k, r)
                        T_tree = 4 * _list_merge_complexity(L1, l1, hmap) + 2 * _list_merge_complexity(L12,
                                                                                                       l - l1,
                                                                                                       hmap) + _indyk_motwani_complexity(
                            L1234,
                            n - k - l,
                            w - 2 * p,
                            hmap)
                        T_rep = int(ceil(2 ** (max(l - log2(reps2), 0) + 3 * max(l1 - log2(reps1), 0))))
                        tmp = Tp + log2(Tg + T_rep * T_tree)
                        tmp += __memory_access_cost(tmp_mem, memory_access)

                        if tmp < time:
                            time = tmp
                            memory = tmp_mem
                            params = [p, l, p2, p1]
        for i in range(len(i_val)):
            if params[i] >= i_val[i] - i_val_inc[i] / 2:
                i_val[i] += i_val_inc[i]
                stop = False
        if stop:
            break
        break
    par = {"l": params[1], "p": params[0], "p1": params[3], "p2": params[2], "depth": 3}
    res = {"time": time, "memory": memory, "parameters": par}

    return res


def quantum_prange_complexity(n, k, w, maxdepth=96, matrix_mult_constant=2.5):
    """
    Optimistic complexity estimate of quantum version of Prange's algorithm

    [Pra62] Prange, E.: The use of information sets in decoding cyclic codes. IRE Transactions
     on Information Theory 8(5), 5–9 (1962)

    [Ber10] Bernstein, D.J.: Grover vs. McEliece. In: International Workshop on Post-QuantumCryptography.
     pp. 73–80. Springer (2010)

    expected weight distribution::

        +--------------------------------+-------------------------------+
        | <----------+ n - k +---------> | <----------+ k +------------> |
        |                w               |              0                |
        +--------------------------------+-------------------------------+

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``maxdepth`` -- maximum allowed depth of the quantum circuit (default: 96)
    - ``matrix_mult_constant`` -- used matrix multiplication constant (default: 2.5)


    EXAMPLES::

        >>> from .estimator import quantum_prange_complexity
        >>> quantum_prange_complexity(n=100,k=50,w=10) # doctest: +SKIP

    """

    Tg = matrix_mult_constant * log2(n - k)
    if Tg > maxdepth:
        return 0

    full_circuit = Tg + (log2(binom(n, w)) - log2(binom(n - k, w))) / 2
    if full_circuit < maxdepth:
        return full_circuit

    time = log2(binom(n, w)) - log2(binom(n - k, w)) + 2 * Tg - maxdepth
    return time


def sd_estimate_display(n, k, w, memory_limit=inf, bit_complexities=1, hmap=1, skip=["BJMM-dw"], precision=1,
                        truncate=0,
                        all_parameters=0, theoretical_estimates=0, use_mo=1, workfactor_accuracy=1, limit_depth=0,
                        quantum_estimates=1,
                        maxdepth=96, matrix_mult_constant=2.5, memory_access=0):
    """
    Output estimates of complexity to solve the syndrome decoding problem

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``memory_limit`` -- upper bound on the available memory (in log2) (default: unlimited)
    - ``bit_complexities`` -- state security level in number of bitoperations, otherwise field operations (default: true)
    - ``hmap`` -- indicates if hashmap is used for sorting lists (default: true)
    - ``skip`` -- list of algorithms not to consider (default: ["BJMM-dw"] (this variant will take a long time to optimize))
    - ``precision`` -- amount of decimal places displayed for complexity estimates (default: 1)
    - ``truncate`` -- decimal places exceeding ``precision`` are truncated, otherwise rounded (default: false)
    - ``all_parameters`` -- print values of all hyperparameters (default: false)
    - ``theoretical_estimates`` -- compute theoretical workfactors for all algorithms (default: false)
    - ``use_mo`` -- use may-ozerov nearest neighbor search in theoretical workfactor computation (default: true)
    - ``workfactor_accuracy`` -- the higher the more accurate the workfactor computation, can slow down computations significantly, recommended range 0-2 (needs to be larger than 0)  (default: 1)
    - ``limit_depth`` -- restricts BJMM and May-Ozerov algorithms to depth two only (default: false)
    - ``quantum_estimates`` -- compute quantum estimates of all algorithms (default: true)
    - ``maxdepth`` -- maximum allowed depth of the quantum circuit (default: 96)
    - ``matrix_mult_constant`` -- used matrix multiplication constant (default: 2.5)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)

    EXAMPLES::

        >>> from .estimator import *
        >>> sd_estimate_display(n=600,k=400,w=22)
        =========================================================================
        Complexity estimation to solve the (600,400,22) syndrome decoding problem
        =========================================================================
        The following table states bit complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.
        The quantum estimate gives a very optimistic estimation of the cost for a quantum aided attack with a circuit of limitted depth (should be understood as a lowerbound).
        +----------------+---------------+---------+
        |                |    estimate   | quantum |
        +----------------+------+--------+---------+
        | algorithm      | time | memory |    time |
        +----------------+------+--------+---------+
        | Prange         | 60.1 |   17.3 |   37.1  |
        | Stern          | 47.0 |   24.5 |    --   |
        | Dumer          | 47.6 |   24.6 |    --   |
        | Ball Collision | 47.7 |   24.5 |    --   |
        | BJMM (MMT)     | 47.6 |   22.7 |    --   |
        | BJMM-pdw       | 47.7 |   21.7 |    --   |
        | May-Ozerov     | 46.5 |   22.6 |    --   |
        | Both-May       | 47.1 |   22.6 |    --   |
        +----------------+------+--------+---------+


        >>> from .estimator import *
        >>> sd_estimate_display(n=1000,k=500,w=100,all_parameters=1,theoretical_estimates=1,precision=2) # long time
        ===========================================================================
        Complexity estimation to solve the (1000,500,100) syndrome decoding problem
        ===========================================================================
        The following table states bit complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.
        The approximation is based on the theoretical workfactor of the respective algorithms, disregarding all polynomial factors and using further approximations that introduce additional polynomial inaccurcies.
        The quantum estimate gives a very optimistic estimation of the cost for a quantum aided attack with a circuit of limitted depth (should be understood as a lowerbound).
        +----------------+-----------------+-----------------+---------+--------------------------------------------------------------------+
        |                |     estimate    |  approximation  | quantum |                             parameters                             |
        +----------------+--------+--------+--------+--------+---------+--------------------------------------------------------------------+
        | algorithm      |   time | memory |   time | memory |    time | classical                                                          |
        +----------------+--------+--------+--------+--------+---------+--------------------------------------------------------------------+
        | Prange         | 134.46 |  19.26 | 108.03 |   0.00 |  76.39  | r  :   7                                                           |
        | Stern          | 117.04 |  38.21 | 104.02 |  31.39 |    --   | l  :  27 | p  :   4                                                |
        | Dumer          | 116.82 |  38.53 | 103.76 |  33.68 |    --   | l  :  28 | p  :   4                                                |
        | Ball Collision | 117.04 |  38.21 | 103.76 |  32.67 |    --   | l  :  27 | p  :   4 | pl :   0                                     |
        | BJMM (MMT)     | 112.39 |  73.15 |  90.17 |  67.76 |    --   | l  : 120 | p  :  16 | p1 :  10 | depth :   2                       |
        | BJMM-pdw       | 113.92 |  52.74 |     -- |     -- |    --   | l1 :  35 | p  :  10 | p1 :   6 | depth :   2 | l2 :  21 | w2 :   0 |
        | May-Ozerov     | 111.56 |  70.44 |  89.51 |  51.39 |    --   | l  :  69 | p  :  14 | p1 :  10 | depth :   2                       |
        | Both-May       | 113.68 |  68.58 |  87.60 |  64.13 |    --   | l  :  75 | p  :  14 | p1 :  10 | w1 :   2 | w2 :   2 | depth :   2 |
        +----------------+--------+--------+--------+--------+---------+--------------------------------------------------------------------+


    TESTS::

        >>> from .estimator import *
        >>> sd_estimate_display(24646,12323,142,all_parameters=True) # long time
        ==============================================================================
        Complexity estimation to solve the (24646,12323,142) syndrome decoding problem
        ==============================================================================
        The following table states bit complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.
        The quantum estimate gives a very optimistic estimation of the cost for a quantum aided attack with a circuit of limitted depth (should be understood as a lowerbound).
        +----------------+----------------+---------+--------------------------------------------------------------------+
        |                |    estimate    | quantum |                             parameters                             |
        +----------------+-------+--------+---------+--------------------------------------------------------------------+
        | algorithm      |  time | memory |    time | classical                                                          |
        +----------------+-------+--------+---------+--------------------------------------------------------------------+
        | Prange         | 182.1 |   28.4 |  114.5  | r  :  11                                                           |
        | Stern          | 160.6 |   39.8 |    --   | l  :  33 | p  :   2                                                |
        | Dumer          | 161.1 |   39.8 |    --   | l  :  28 | p  :   2                                                |
        | Ball Collision | 161.1 |   39.8 |    --   | l  :  28 | p  :   2 | pl :   0                                     |
        | BJMM (MMT)     | 160.9 |   54.2 |    --   | l  :  74 | p  :   4 | p1 :   3 | depth :   2                       |
        | BJMM-pdw       | 160.9 |   55.0 |    --   | l1 :  30 | p  :   4 | p1 :   3 | depth :   2 | l2 :  22 | w2 :   0 |
        | May-Ozerov     | 160.4 |   55.0 |    --   | l  :  30 | p  :   4 | p1 :   3 | depth :   2                       |
        | Both-May       | 161.1 |   37.8 |    --   | l  :   4 | p  :   2 | p1 :   1 | w1 :   1 | w2 :   0 | depth :   2 |
        +----------------+-------+--------+---------+--------------------------------------------------------------------+


        >>> from .estimator import *
        >>> sd_estimate_display(300,200,20,all_parameters=True, skip=[])
        =========================================================================
        Complexity estimation to solve the (300,200,20) syndrome decoding problem
        =========================================================================
        The following table states bit complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.
        The quantum estimate gives a very optimistic estimation of the cost for a quantum aided attack with a circuit of limitted depth (should be understood as a lowerbound).
        +----------------+---------------+---------+-------------------------------------------------------------------------------------------+
        |                |    estimate   | quantum |                                         parameters                                        |
        +----------------+------+--------+---------+-------------------------------------------------------------------------------------------+
        | algorithm      | time | memory |    time | classical                                                                                 |
        +----------------+------+--------+---------+-------------------------------------------------------------------------------------------+
        | Prange         | 52.5 |   15.3 |   33.5  | r  :   5                                                                                  |
        | Stern          | 40.7 |   21.5 |    --   | l  :  13 | p  :   2                                                                       |
        | Dumer          | 41.1 |   26.9 |    --   | l  :  18 | p  :   3                                                                       |
        | Ball Collision | 41.3 |   21.5 |    --   | l  :  12 | p  :   2 | pl :   0                                                            |
        | BJMM (MMT)     | 41.1 |   27.5 |    --   | l  :  25 | p  :   4 | p1 :   2 | depth :   2                                              |
        | BJMM-pdw       | 41.3 |   18.9 |    --   | l1 :   3 | p  :   2 | p1 :   1 | depth :   2 | l2 :   4 | w2 :   0                        |
        | BJMM-dw        | 41.3 |   19.7 |    --   | l  :   6 | p  :   2 | p1 :   1 | w1 :   0 | w11 :   1 | l2 :   5 | w2 :   0 | depth :   2 |
        | May-Ozerov     | 40.1 |   19.7 |    --   | l  :   2 | p  :   2 | p1 :   1 | depth :   2                                              |
        | Both-May       | 40.4 |   19.7 |    --   | l  :   2 | p  :   2 | p1 :   1 | w1 :   2 | w2 :   0 | depth :   2                        |
        +----------------+------+--------+---------+-------------------------------------------------------------------------------------------+



    """

    complexities = _sd_estimate(n, k, w, theoretical_estimates, memory_limit, bit_complexities, hmap, skip, use_mo,
                                workfactor_accuracy, limit_depth, quantum_estimates, maxdepth, matrix_mult_constant,
                                memory_access)

    headline = "Complexity estimation to solve the ({},{},{}) syndrome decoding problem".format(n, k, w)
    print("=" * len(headline))
    print(headline)
    print("=" * len(headline))
    if bit_complexities:
        print(
            "The following table states bit complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.")
    else:
        print(
            "The following table states complexity estimates of the corresponding algorithms including an approximation of the polynomial factors inherent to the algorithm.")
        print("The time complexity estimate is measured in the number of additions in (F_2)^n.")
        print("The memory complexity estimate is given in the number of vector space elements that need to be stored.")

    if theoretical_estimates:
        print(
            "The approximation is based on the theoretical workfactor of the respective algorithms, disregarding all polynomial factors and using further approximations that introduce additional polynomial inaccurcies.")
    if quantum_estimates:
        print(
            "The quantum estimate gives a very optimistic estimation of the cost for a quantum aided attack with a circuit of limitted depth (should be understood as a lowerbound).")
    tables = []
    table_fields = ['algorithm']

    tbl_names = PrettyTable(table_fields)
    tbl_names.padding_width = 1
    tbl_names.title = ' '

    for i in complexities.keys():
        tbl_names.add_row([i])
    tbl_names.align["algorithm"] = "l"
    tables.append(tbl_names)

    table_fields = ['time', 'memory']
    tbl_estimates = PrettyTable(table_fields)
    tbl_estimates.padding_width = 1
    tbl_estimates.title = 'estimate'
    tbl_estimates.align["time"] = "r"
    tbl_estimates.align["memory"] = "r"
    for i in complexities.keys():
        if complexities[i]["time"] != inf:
            T, M = __round_or_truncate_to_given_precision(complexities[i]["time"], complexities[i]["memory"], truncate,
                                                          precision)
        else:
            T, M = "--", "--"
        tbl_estimates.add_row([T, M])

    tables.append(tbl_estimates)

    if theoretical_estimates:
        table_fields = ['time', 'memory']
        tbl_approx = PrettyTable(table_fields)
        tbl_approx.padding_width = 1
        tbl_approx.title = 'approximation'
        tbl_approx.align["time"] = "r"
        tbl_approx.align["memory"] = "r"

        for i in complexities.keys():
            if complexities[i]["Workfactor time"] != 0:
                T, M = __round_or_truncate_to_given_precision(complexities[i]["Workfactor time"] * n,
                                                              complexities[i]["Workfactor memory"] * n, truncate,
                                                              precision)
            else:
                T, M = "--", "--"
            tbl_approx.add_row([T, M])

        tables.append(tbl_approx)

    if quantum_estimates:
        table_fields = ['  time']
        tbl_quantum = PrettyTable(table_fields)
        tbl_quantum.padding_width = 1
        tbl_quantum.title = "quantum"
        tbl_quantum.align["time"] = "r"
        for i in complexities.keys():
            if "quantum time" in complexities[i].keys() and complexities[i]["quantum time"] != 0:
                T, M = __round_or_truncate_to_given_precision(complexities[i]["quantum time"], 0, truncate, precision)
            else:
                T = "--"
            tbl_quantum.add_row([T])
        tables.append(tbl_quantum)

    if all_parameters:
        table_fields = ['classical']
        tbl_params = PrettyTable(table_fields)
        tbl_params.padding_width = 1
        tbl_params.title = "parameters"
        tbl_params.align['classical'] = "l"

        for i in complexities.keys():
            row = ""
            for j in complexities[i]["parameters"].keys():
                row += "{:<{align}}".format(j, align=max(2, len(j))) + " : " + '{:3d}'.format(
                    complexities[i]["parameters"][j]) + " | "
            tbl_params.add_row([row[:-3]])

        tables.append(tbl_params)

    tbl_join = __concat_pretty_tables(str(tables[0]), str(tables[1]))
    for i in range(2, len(tables)):
        tbl_join = __concat_pretty_tables(tbl_join, str(tables[i]))

    print(tbl_join)


def _add_theoretical_estimates(complexities, n, k, w, memory_limit, skip, use_mo, workfactor_accuracy):
    rate = k / n
    omega = w / n

    grid_std_accuracy = {"prange": [20, 150], "stern": [20, 150], "dumer": [20, 150], "ball_collision": [15, 150],
                         "bjmm": [10, 250], "may-ozerov": [5, 1000], "both-may": [5, 1000]}

    if workfactor_accuracy != 1:
        for i in grid_std_accuracy.keys():
            for j in range(2):
                grid_std_accuracy[i][j] = int(ceil(grid_std_accuracy[i][j] * workfactor_accuracy))

    for i in complexities.keys():
        complexities[i]["Workfactor time"] = 0
        complexities[i]["Workfactor memory"] = 0

    nr_algorithms = 7 - len(skip)
    nr_algorithms += 1 if "BJMM-dw" in skip else 0
    nr_algorithms += 1 if "BJMM-p-dw" in skip or "BJMM-pdw" in skip else 0
    bar = Bar('Computing theoretical workfactors\t', max=nr_algorithms)

    if "prange" not in skip:
        T, M = prange_workfactor(rate, omega, grid_std_accuracy["prange"][0], grid_std_accuracy["prange"][1],
                                 memory_limit)
        complexities["Prange"]["Workfactor time"] = T
        complexities["Prange"]["Workfactor memory"] = M
        bar.next()
    if "stern" not in skip:
        T, M = stern_workfactor(rate, omega, grid_std_accuracy["stern"][0], grid_std_accuracy["stern"][1], memory_limit)
        complexities["Stern"]["Workfactor time"] = T
        complexities["Stern"]["Workfactor memory"] = M
        bar.next()
    if "dumer" not in skip:
        T, M = dumer_workfactor(rate, omega, grid_std_accuracy["dumer"][0], grid_std_accuracy["dumer"][1], memory_limit)
        complexities["Dumer"]["Workfactor time"] = T
        complexities["Dumer"]["Workfactor memory"] = M
        bar.next()
    if "ball_collision" not in skip:
        T, M = ball_collision_workfactor(rate, omega, grid_std_accuracy["ball_collision"][0],
                                         grid_std_accuracy["ball_collision"][1], memory_limit)
        complexities["Ball Collision"]["Workfactor time"] = T
        complexities["Ball Collision"]["Workfactor memory"] = M
        bar.next()
    if "BJMM" not in skip and "MMT" not in skip:
        T, M = bjmm_workfactor(rate, omega, grid_std_accuracy["bjmm"][0], grid_std_accuracy["bjmm"][1], memory_limit)
        complexities["BJMM (MMT)"]["Workfactor time"] = T
        complexities["BJMM (MMT)"]["Workfactor memory"] = M
        bar.next()
    if "MO" not in skip and "May-Ozerov" not in skip:
        T, M = may_ozerov_workfactor(rate, omega, grid_std_accuracy["may-ozerov"][0],
                                     grid_std_accuracy["may-ozerov"][1], memory_limit, use_mo)
        complexities["May-Ozerov"]["Workfactor time"] = T
        complexities["May-Ozerov"]["Workfactor memory"] = M
        bar.next()
    if "BM" not in skip and "Both-May" not in skip:
        T, M = both_may_workfactor(rate, omega, grid_std_accuracy["both-may"][0], grid_std_accuracy["both-may"][1],
                                   memory_limit, use_mo)
        complexities["Both-May"]["Workfactor time"] = T
        complexities["Both-May"]["Workfactor memory"] = M
        bar.next()

    bar.finish()


def _sd_estimate(n, k, w, theoretical_estimates, memory_limit, bit_complexities, hmap, skip, use_mo,
                 workfactor_accuracy, limit_depth, quantum_estimates, maxdepth, matrix_mult_constant, memory_access):
    """
    Estimate complexity to solve syndrome decoding problem

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``w`` -- Hamming weight of error vector
    - ``memory_limit`` -- upper bound on the available memory (as log2(bits))
    - ``hmap`` -- indicates if hashmap should be used for sorting lists
    - ``skip`` -- list of algorithms not to consider
    - ``use_mo`` -- use may-ozerov nearest neighbor search in theoretical workfactor computation
    - ``workfactor_accuracy`` -- the higher the more accurate the workfactor computation, can slow down computations significantly, recommended range 0-2 (needs to be larger than 0)

    """

    complexities = {}
    if bit_complexities:
        memory_limit -= log2(n)

    nr_algorithms = 9 - len(skip)
    bar = Bar('Computing estimates\t\t\t', max=nr_algorithms)

    if "prange" not in skip:
        complexities["Prange"] = prange_complexity(n, k, w, mem=memory_limit, memory_access=memory_access)
        if quantum_estimates:
            complexities["Prange"]["quantum time"] = quantum_prange_complexity(n, k, w, maxdepth=maxdepth,
                                                                               matrix_mult_constant=matrix_mult_constant)
        bar.next()

    if "stern" not in skip:
        complexities["Stern"] = stern_complexity(n, k, w, mem=memory_limit, hmap=hmap, memory_access=memory_access)
        bar.next()
    if "dumer" not in skip:
        complexities["Dumer"] = dumer_complexity(n, k, w, mem=memory_limit, hmap=hmap, memory_access=memory_access)
        bar.next()
    if "ball_collision" not in skip:
        complexities["Ball Collision"] = ball_collision_decoding_complexity(n, k, w, mem=memory_limit, hmap=hmap,
                                                                            memory_access=memory_access)
        bar.next()
    if "BJMM" not in skip and "MMT" not in skip:
        complexities["BJMM (MMT)"] = bjmm_complexity(n, k, w, mem=memory_limit, hmap=hmap, only_depth_two=limit_depth,
                                                     memory_access=memory_access)
        bar.next()
    if "BJMM-pdw" not in skip and "BJMM-p-dw" not in skip:
        complexities["BJMM-pdw"] = bjmm_depth_2_partially_disjoint_weight_complexity(n, k, w, mem=memory_limit,
                                                                                     hmap=hmap,
                                                                                     memory_access=memory_access)
        bar.next()
    if "BJMM-dw" not in skip:
        complexities["BJMM-dw"] = bjmm_depth_2_disjoint_weight_complexity(n, k, w, mem=memory_limit, hmap=hmap,
                                                                          memory_access=memory_access)
        bar.next()
    if "MO" not in skip and "May-Ozerov" not in skip:
        complexities["May-Ozerov"] = may_ozerov_complexity(n, k, w, mem=memory_limit, hmap=hmap,
                                                           only_depth_two=limit_depth, memory_access=memory_access)
        bar.next()
    if "BM" not in skip and "Both-May" not in skip:
        complexities["Both-May"] = both_may_depth_2_complexity(n, k, w, mem=memory_limit, hmap=hmap,
                                                               memory_access=memory_access)
        bar.next()

    bar.finish()
    if theoretical_estimates:
        _add_theoretical_estimates(complexities, n, k, w, memory_limit, skip, use_mo, workfactor_accuracy)

    if bit_complexities:
        field_op = log2(n)
        for i in complexities.keys():
            complexities[i]["time"] += field_op
            complexities[i]["memory"] += field_op

    return complexities

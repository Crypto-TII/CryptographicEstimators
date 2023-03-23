from math import  log2, comb as binom, inf, ceil
from cryptographic_estimators.SDEstimator.sd_helper import _gaussian_elimination_complexity, _mem_matrix,\
    _list_merge_complexity, _list_merge_async_complexity

from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMM_plus
from cryptographic_estimators.SDEstimator import SDProblem


def _optimize_m4ri(n, k, mem=inf):
    """
    Find optimal blocksize for Gaussian elimination via M4RI
    INPUT:
    - ``n`` -- Row additions are performed on ``n`` coordinates
    - ``k`` -- Matrix consists of ``n-k`` rows
    """

    (r, v) = (0, inf)
    for i in range(n - k):
        tmp = log2(_gaussian_elimination_complexity(n, k, i))
        if v > tmp and r < mem:
            r = i
            v = tmp
    return r


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

        if stop is True:
            break

    par = {"l": params[1], "p": params[0], "p1": params[2],
           "l1": params[5], "reps": params[6], "depth": 2}
    res = {"time": time, "memory": memory, "parameters": par,
           "perms": params[4], "lists": lists}
    return time + log2(n), memory


ranges = 2.
def test_bjmm_plus1():
    t1, m = bjmm_depth_2_qc_complexity(1284, 1028, 24)
    t2 = BJMM_plus(SDProblem(1284, 1028, 24)).time_complexity()
    assert t1 - ranges <= t2 <= t1 + ranges
def test_bjmm_plus2():
    t1, m = bjmm_depth_2_qc_complexity(3488, 2720, 64)
    t2 = BJMM_plus(SDProblem(3488, 2720, 64)).time_complexity()
    print(t1, t2)
    assert t1 - ranges <= t2 <= t1 + ranges

#test_bjmm_plus1()
test_bjmm_plus2()
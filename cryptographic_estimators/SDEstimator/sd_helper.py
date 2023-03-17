# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from math import log2, comb, inf, ceil
from sage.all import RealField, matrix, identity_matrix


def binom(n: int, k: int):
    """
    binomial coefficient
    """
    return comb(int(n), int(k))


def min_max(a: int, b: int, s: bool):
    """
    Returns min(a,b) or max(a,b) depending on the switch s
        s =  false        true
    """
    if s:
        return max(a, b)
    else:
        return min(a, b)


def __truncate(x: float, precision: int):
    """
    Truncates a float

    INPUT:

    - ``x`` -- value to be truncated
    - ``precision`` -- number of decimal places to after which the ``x`` is truncated

    """

    return float(int(x * 10 ** precision) / 10 ** precision)


def __round_or_truncate_to_given_precision(T: float, M: float, truncate: bool, precision: int):
    """
    rounds or truncates the inputs `T`, `M`
    INPUT:
        - ``T`` -- first value to truncate or round
        - ``M`` -- second value to truncate or round
        - ``truncate`` -- if set the `true` the inputs are truncated otherwise rounded
        - ``precision`` -- precision of the truncation or rounding
    """
    if truncate:
        T, M = __truncate(T, precision), __truncate(M, precision)
    else:
        T, M = round(T, precision), round(M, precision)
    return '{:.{p}f}'.format(T, p=precision), '{:.{p}f}'.format(M, p=precision)


def _gaussian_elimination_complexity(n: int, k: int, r: int):
    """
    Complexity estimate of Gaussian elimination routine

    INPUT:

    - ``n`` -- Row additions are perfomed on ``n`` coordinates
    - ``k`` -- Matrix consists of ``n-k`` rows
    - ``r`` -- Blocksize of method of the four russian for inversion, default is zero

    [Bar07]_ Bard, G.V.: Algorithms for solving linear and polynomial systems of equations over finite fields
    with applications to cryptanalysis. Ph.D. thesis (2007)

    [BLP08] Bernstein, D.J., Lange, T., Peters, C.: Attacking and defending the mceliece cryptosystem.
    In: International Workshop on Post-Quantum Cryptography. pp. 31–46. Springer (2008)

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _gaussian_elimination_complexity
        sage: _gaussian_elimination_complexity(n=100,k=20,r=1) # random

    """

    if r != 0:
        return (r ** 2 + 2 ** r + (n - k - r)) * int(((n + r - 1) / r))

    return (n - k) ** 2


def _optimize_m4ri(n: int, k: int, mem=inf):
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


def _mem_matrix(n: int, k: int, r: int):
    """
    Memory usage of parity check matrix in vector space elements

    INPUT:

    - ``n`` -- length of the code
    - ``k`` -- dimension of the code
    - ``r`` -- block size of M4RI procedure

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _mem_matrix
        sage: _mem_matrix(n=100,k=20,r=0) # random

    """
    return n - k + 2 ** r


def _list_merge_complexity(L: float, l: int, hmap: bool):
    """
    Complexity estimate of merging two lists exact

    INPUT:

    - ``L`` -- size of lists to be merged
    - ``l`` -- amount of bits used for matching
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _list_merge_complexity
        sage: _list_merge_complexity(L=2**16,l=16,hmap=1) # random

    """

    if L == 1:
        return 1
    if not hmap:
        return max(1, 2 * int(log2(L)) * L + L ** 2 // 2 ** l)
    else:
        return 2 * L + L ** 2 // 2 ** l


def _list_merge_async_complexity(L1: float, L2: float, l: int, hmap: bool = True):
    """
    Complexity estimate of merging two lists exact

    INPUT:

    - ``L`` -- size of lists to be merged
    - ``l`` -- amount of bits used for matching
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _list_merge_async_complexity
        sage: _list_merge_async_complexity(L1=2**16,L2=2**14,l=16,hmap=1) # random

    """

    if L1 == 1 and L2==1:
        return 1
    if L1==1:
        return L2
    if L2==1:
        return L1
    if not hmap:
        return 0 #to be implemented
    else:
        return L1+L2 + L1*L2 // 2 ** l


def _indyk_motwani_complexity(L: float, l: int, w: int, hmap: bool):
    """
    Complexity of Indyk-Motwani nearest neighbor search

    INPUT:

    - ``L`` -- size of lists to be matched
    - ``l`` -- amount of bits used for matching
    - ``w`` -- target weight
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _indyk_motwani_complexity
        sage: _indyk_motwani_complexity(L=2**16,l=16,w=2,hmap=1) # random

    """

    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    lam = max(0, int(min(ceil(log2(L)), l - 2 * w)))
    return binom(l, lam) // binom(l - w, lam) * _list_merge_complexity(L, lam, hmap)


def _mitm_nn_complexity(L: float, l: int, w: int, hmap: bool):
    """
    Complexity of Indyk-Motwani nearest neighbor search

    INPUT:

    - ``L`` -- size of lists to be matched
    - ``l`` -- amount of bits used for matching
    - ``w`` -- target weight
    - ``hmap`` -- indicates if hashmap is being used (Default 0: no hashmap)

    EXAMPLES::

        sage: from cryptographic_estimators.SDEstimator import _indyk_motwani_complexity
        sage: _indyk_motwani_complexity(L=2**16,l=16,w=2,hmap=1) # random

    """
    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    L1 = L * binom(l / 2, w / 2)
    return _list_merge_complexity(L1, l, hmap)


def marcovchain_number_perms(n: int, k: int, w: int, c: int, p: int, l: int):
    """

    returns the number of expected iteration in logarithmic notation

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- weight
    - ``c`` -- number of coordinates to exchange during each gaussian elimination
    - ``p`` -- weight of the good state
    - ``l`` -- window

    EXAMPLES::
        p = 3
        n = 2918
        k = n//2
        w = 56
        l = 0
        c = 95
        number_perms(n,k,w,c,p,l)
    """
    R1 = RealField(150)

    def transition(u: int, d: int, c: int, n: int, k: int, w: int, l: int):
        # from u to u+d by exchanging c columns
        return R1(sum(binom(w-u, i) * binom(n-k-l-w+u, c-i) * binom(u, i-d) * binom(k+l-u, c+d-i)
                      for i in range(max(d, 0), min(w-u+1, c+1, c+d+1))))/R1(binom(n-k-l, c) * binom(k+l, c))
    A = matrix(R1, w+1, w+1)
    for i in range(w+1):
        for j in range(w+1):
            A[i,j] = transition(i, j-i, c, n, k, w, l)

    # transition matrix excluding success-state
    B = A[[i for i in range(w+1) if i!=p],[i for i in range(w+1) if i!=p]]

    # fundamental matrix of markov process
    R = (identity_matrix(R1, w, w)-B)**(-1)

    # initial state of markov chain
    state = [(binom(n-k,w-i)*binom(k,i))/binom(n,w) for i in range(w+1) if i!=p]

    # number of permutations
    return log2(sum(state[i]*sum(R[i,j] for j in range(w)) for i in range(w))) - log2(n-k)


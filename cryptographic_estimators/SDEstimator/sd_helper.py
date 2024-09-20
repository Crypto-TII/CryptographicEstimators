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


def binom(n: int, k: int):
    """Compute the binomial coefficient.

    Args:
        n (int): The total number of items.
        k (int): The number of items to be selected.

    Returns:
        int: The binomial coefficient, which represents the number of ways to
             select k items from a set of n items.
    """
    return comb(int(n), int(k))


def min_max(a: int, b: int, s: bool) -> int:
    """Returns the minimum or maximum of two integers based on a boolean switch.

    Args:
        a (int): The first integer.
        b (int): The second integer.
        s (bool): If True, returns the maximum of a and b. If False, returns the minimum of a and b.

    Returns:
        int: The minimum or maximum of a and b, depending on the value of s.
    """
    if s:
        return max(a, b)
    else:
        return min(a, b)


def __truncate(x: float, precision: int) -> float:
    """Truncates a float.

    Args:
        x (float): The value to be truncated.
        precision (int): The number of decimal places to truncate the input value `x`.

    Returns:
        float: The truncated value of `x`.
    """
    pass

    return float(int(x * 10**precision) / 10**precision)


def __round_or_truncate_to_given_precision(T: float, M: float, truncate: bool, precision: int) -> tuple:
    """Rounds or truncates the input values `T` and `M`.

    Args:
        T (float): The first value to truncate or round.
        M (float): The second value to truncate or round.
        truncate (bool): If set to `True`, the inputs are truncated. Otherwise, they are rounded.
        precision (int): The number of decimal places to round or truncate the values to.

    Returns:
        Tuple[str, str]: The rounded or truncated values of `T` and `M` as strings, formatted to the specified precision.
    """
    if truncate:
        T, M = __truncate(T, precision), __truncate(M, precision)
    else:
        T, M = round(T, precision), round(M, precision)
    return "{:.{p}f}".format(T, p=precision), "{:.{p}f}".format(M, p=precision)


def _gaussian_elimination_complexity(n: int, k: int, r: int):
    """Compute the complexity estimate of the Gaussian elimination routine. [Bar07]_ [BLP08]_

    Args:
        n (int): The number of rows on which row additions are performed.
        k (int): The number of rows in the matrix.
        r (int): The block size of the method of the four Russian for inversion. The default value is zero.

    Returns:
        The complexity estimate of the Gaussian elimination routine.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _gaussian_elimination_complexity
        >>> _gaussian_elimination_complexity(n=100,k=20,r=1) # random output # doctest: +SKIP
    """

    if r != 0:
        return (r**2 + 2**r + (n - k - r)) * int(((n + r - 1) / r))

    return (n - k) ** 2


def _optimize_m4ri(n: int, k: int, mem=float("inf")):
    """Finds the optimal blocksize for Gaussian elimination via M4RI.

    Args:
        n (int): The number of coordinates on which row additions are performed.
        k (int): The number of rows in the matrix.
        mem (float, optional): The memory limit. Defaults to infinity.

    Returns:
        The optimal blocksize for the given parameters.
    """
    pass

    (r, v) = (0, inf)
    for i in range(n - k):
        tmp = log2(_gaussian_elimination_complexity(n, k, i))
        if v > tmp and r < mem:
            r = i
            v = tmp
    return r


def _mem_matrix(n: int, k: int, r: int):
    """Compute the memory usage of the parity check matrix in vector space elements.

    Args:
        n (int): The length of the code.
        k (int): The dimension of the code.
        r (int): The block size of the M4RI procedure.

    Returns:
        The memory usage of the parity check matrix in vector space elements.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _mem_matrix
        >>> _mem_matrix(n=100,k=20,r=0) # random output # doctest: +SKIP
        ...
    """
    return n - k + 2**r


def _list_merge_complexity(L: float, l: int, hmap: bool):
    """Complexity estimate of merging two lists.

    Args:
        L (float): Size of lists to be merged.
        l (int): Amount of bits used for matching.
        hmap (bool): Indicates if a hash map is being used (Default is False, which means no hash map).

    Returns:
        The complexity estimate of merging two lists.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _list_merge_complexity
        >>> _list_merge_complexity(L=2**16,l=16,hmap=1) # random output # doctest: +SKIP
        ...
    """

    if L == 1:
        return 1
    if not hmap:
        return max(1, 2 * int(log2(L)) * L + L**2 // 2**l)
    else:
        return 2 * L + L**2 // 2**l


def _indyk_motwani_complexity(L: float, l: int, w: int, hmap: bool):
    """Complexity of Indyk-Motwani nearest neighbor search.

    Args:
        L (float): Size of lists to be matched.
        l (int): Amount of bits used for matching.
        w (int): Target weight.
        hmap (bool): Indicates if a hash map is being used (default is False: no hash map).

    Returns:
        The complexity of the Indyk-Motwani nearest neighbor search.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _indyk_motwani_complexity
        >>> _indyk_motwani_complexity(L=2**16,l=16,w=2,hmap=1) # random output # doctest: +SKIP
        ...
    """

    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    lam = max(0, int(min(ceil(log2(L)), l - 2 * w)))
    return binom(l, lam) // binom(l - w, lam) * _list_merge_complexity(L, lam, hmap)


def _mitm_nn_complexity(L: float, l: int, w: int, hmap: bool):
    """Complexity of Indyk-Motwani nearest neighbor search.

    Args:
        L (float): Size of lists to be matched.
        l (int): Amount of bits used for matching.
        w (int): Target weight.
        hmap (bool): Indicates if a hash map is being used (Default is False).

    Returns:
        The complexity of the Indyk-Motwani nearest neighbor search.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _indyk_motwani_complexity
        >>> _indyk_motwani_complexity(L=2**16, l=16, w=2, hmap=True) # random output # doctest: +SKIP
        ...
    """
    if w == 0:
        return _list_merge_complexity(L, l, hmap)
    L1 = L * binom(l / 2, w / 2)
    return _list_merge_complexity(L1, l, hmap)


def _list_merge_async_complexity(L1: float, L2: float, l: int, hmap: bool = True):
    """Compute the complexity of merging two different sized lists on l bits.

    Args:
        L1 (float): Size of the first list to be merged.
        L2 (float): Size of the second list to be merged.
        l (int): Number of bits used for matching.
        hmap (bool): Indicates whether a hashmap is being used (default is True).

    Returns:
        int: The complexity estimate of merging the two lists.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _list_merge_async_complexity
        >>> _list_merge_async_complexity(L1=2**16, L2=2**14, l=16, hmap=1) # random output # doctest: +SKIP
        ...
    """
    if L1 == 1 and L2 == 1:
        return 1
    if L1 == 1:
        return L2
    if L2 == 1:
        return L1
    if not hmap:
        L = max(L1, L2)
        return max(1, 2 * int(log2(L)) * L + (L1 * L2) // 2**l)
    else:
        return L1 + L2 + L1 * L2 // 2**l

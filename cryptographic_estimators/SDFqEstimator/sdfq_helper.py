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


from math import log2, comb, inf


def binom(n: int, k: int):
    """Computes the binomial coefficient.

    Args:
        n (int): The total number of items.
        k (int): The number of items to be selected.

    Returns:
        int: The binomial coefficient.
    """
    return comb(int(n), int(k))


def min_max(a: int, b: int, s: bool):
    """Returns the minimum or maximum of two integers, depending on a boolean switch.

    Args:
        a (int): The first integer to compare.
        b (int): The second integer to compare.
        s (bool): The switch that determines whether the minimum or maximum value is returned.

    Returns:
        int: The minimum of `a` and `b` if `s` is `False`, otherwise the maximum of `a` and `b`.
    """
    if s:
        return max(a, b)
    else:
        return min(a, b)


def __truncate(x: float, precision: int):
    """Truncates a float.

    Args:
        x (float): The value to be truncated.
        precision (int): The number of decimal places to which the value `x` is truncated.

    """
    return float(int(x * 10 ** precision) / 10 ** precision)


def __round_or_truncate_to_given_precision(T: float, M: float, truncate: bool, precision: int):
    """Rounds or truncates the input values `T` and `M`.

    Args:
        T (float): The first value to truncate or round.
        M (float): The second value to truncate or round.
        truncate (bool): If True, the inputs are truncated; otherwise, they are rounded.
        precision (int): The precision of the truncation or rounding.
    """
    if truncate:
        T, M = __truncate(T, precision), __truncate(M, precision)
    else:
        T, M = round(T, precision), round(M, precision)
    return '{:.{p}f}'.format(T, p=precision), '{:.{p}f}'.format(M, p=precision)


def _gaussian_elimination_complexity(n: int, k: int, r: int):
    """Complexity estimate of Gaussian elimination routine.

    Args:
        n (int): Row additions are performed on `n` coordinates.
        k (int): Matrix consists of `n-k` rows.
        r (int): Blocksize of method of the four Russian for inversion, default is zero.

    References: 
        .. [Bar07]_ 
        .. [BLP08]_ pp. 31–46.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _gaussian_elimination_complexity
        >>> _gaussian_elimination_complexity(n=100,k=20,r=1) # random output # doctest: +SKIP
    """

    if r != 0:
        return (r ** 2 + 2 ** r + (n - k - r)) * int(((n + r - 1) / r))

    return (n - k) ** 2


def _optimize_m4ri(n: int, k: int, mem=inf):
    """
    Find optimal blocksize for Gaussian elimination via M4RI.

    Args:
        n (int): Number of coordinates for row additions.
        k (int): The matrix consists of n-k rows.
    """

    (r, v) = (0, inf)
    for i in range(n - k):
        tmp = log2(_gaussian_elimination_complexity(n, k, i))
        if v > tmp and r < mem:
            r = i
            v = tmp
    return r


def _mem_matrix(n: int, k: int, r: int):
    """Calculates the memory usage of the parity check matrix in vector space elements.

    Args:
        n (int): The length of the code.
        k (int): The dimension of the code.
        r (int): The block size of the M4RI procedure.

    Returns:
        The memory usage of the parity check matrix in vector space elements.

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _mem_matrix
        >>> _mem_matrix(n=100,k=20,r=0) # random output # doctest: +SKIP
    """
    return n - k + 2 ** r


def _list_merge_complexity(L: float, l: int, hmap: bool):
    """Complexity estimate of merging two lists.

    Args:
        L (float): Size of lists to be merged.
        l (int): Amount of bits used for matching.
        hmap (bool): Indicates if a hashmap is being used (Default: False).

    Examples:
        >>> from cryptographic_estimators.SDEstimator import _list_merge_complexity
        >>> _list_merge_complexity(L=2**16,l=16,hmap=1) # random output # doctest: +SKIP
    """

    if L == 1:
        return 1
    if not hmap:
        return max(1, 2 * int(log2(L)) * L + L ** 2 // 2 ** l)
    else:
        return 2 * L + L ** 2 // 2 ** l

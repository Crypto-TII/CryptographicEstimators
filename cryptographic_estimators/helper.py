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

from enum import Enum
from bisect import bisect_left


class ComplexityType(Enum):
    """
    distinguish between normal optimisation and tilde O optimisation
    """

    ESTIMATE = 0
    TILDEO = 1


def concat_all_tables(tables):
    """

    INPUT:

    - ``tables`` -- list of `PrettyTable`
    """
    tbl_join = concat_pretty_tables(str(tables[0]), str(tables[1]))
    for i in range(2, len(tables)):
        tbl_join = concat_pretty_tables(tbl_join, str(tables[i]))
    return tbl_join


def concat_pretty_tables(t1: str, t2: str):
    """
    Merge two columns into one
    INPUT:

    - ``t1`` -- first column
    - ``t2`` -- second column

    """
    v = t1.split("\n")
    v2 = t2.split("\n")
    vnew = ""
    for i in range(len(v)):
        vnew += v[i] + v2[i][1:] + "\n"
    return vnew[:-1]


def _truncate(x: float, precision: int):
    """
    truncate a value

    INPUT:

    - ``x`` -- value to truncate
    - ``precision`` -- number of decimial digits to truncate to

    """
    return float(int(x * 10**precision) / 10**precision)


def round_or_truncate(x: float, truncate: bool, precision: int):
    """
    eiter rounds or truncates `x` if `truncate` is `true`

    INPUT:

    - ``x`` -- value to either truncate or round
    - ``truncate`` -- if `true`: `x` will be truncated else rounded
    - ``precision`` -- number of decimial digits

    """
    val = _truncate(x, precision) if truncate else round(float(x), precision)
    return "{:.{p}f}".format(val, p=precision)


# fmt: off
PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
    157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
    239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
    331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419,
    421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503,
    509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607,
    613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
    709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
    821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911,
    919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997
]
# fmt: on


def is_prime_power(n):
    """
    Determines if a given number is a power of a prime number.

    INPUT:

    - ``n`` -- The number to be checked.
    """
    global PRIMES

    def is_power(n, p):
        while n % p == 0:
            n //= p
        return n == 1

    if n <= 1:
        return False

    max_prime = PRIMES[-1]

    if n < max_prime:
        index = bisect_left(PRIMES, n)
        if index < len(PRIMES) and PRIMES[index] == n:
            return True

    for prime in PRIMES:
        if prime * prime > n:
            return True
        if n % prime == 0:
            return is_power(n // prime, prime)

    if max_prime % 6 == 5:
        prime_candidate = 6 * ((max_prime // 6) + 1) - 1
        increment = 2
    else:
        prime_candidate = 6 * (max_prime // 6) + 1
        increment = 4

    while prime_candidate * prime_candidate <= n:
        if n % prime_candidate == 0:
            return is_power(n // prime_candidate, prime_candidate)
        prime_candidate += increment
        increment = 6 - increment
    return True


def is_power_of_two_python(n):
    """
    Determines if a given number is a power of two.

    INPUT:

    - ``n`` -- The number to be checked.
    """
    return (n & (n - 1) == 0) and n != 0

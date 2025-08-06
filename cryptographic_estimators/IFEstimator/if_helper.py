# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************
from math import log2, log, ceil


def Lfunction(alpha, beta, logN):
    """Implements the *exponent* of the L-function 
    L[alpha, beta] = exp((beta)*logN**alpha * log(logN)**(1-alpha) )

    Args:
        alpha (float): main constant in the L-function
        beta (float): another constant in the L-function
        logN (float): ln(N) of the number to factor

    Returns:
        float: the exponent of the L-function

    Examples:
        >>> from cryptographic_estimators.IFEstimator.if_helper import Lfunction
        >>> n = 1024
        >>> Lfunction(0.5, 1, n)
        84.2486031274931
    """
    assert alpha >= 0
    assert beta > 0
    assert alpha <= 1
    return beta*(logN**alpha)*(log(logN))**(1-alpha)


def pifunction(x):
    """Implements the prime counting function π(x) which counts the number of primes less than or equal to x.

    Args:
        x (float): the upper limit for counting primes

    Returns: 
        int: the number of primes less than or equal to x, rounded up

    Examples:
        >>> from cryptographic_estimators.IFEstimator.if_helper import M
        >>> pifunction(127)
        27
    """
    return ceil(x/log(x))


# Thresholds determining when to switch btw multiplication algorithms depending on the number of bits in a number
# as per [GMPlink]_ https://gmplib.org/repo/gmp/file/tip/mpn/arm/gmp-mparam.h
limb = 32
Karatsuba_threshold = limb * 36
ToomCook3_threshold = limb * 125
FFT_threshold = limb * 5760

# complexity of multiplication of 2 n-bit integers


def multipication_complexity(n):
    """Computes the time complexity of multiplying two n-bit integers.

    Args:
        n (int): bit length of the integers to multiply

    Returns:
        float: the time complexity of the multiplication operation

    Examples:
        >>> from cryptographic_estimators.IFEstimator.if_helper import multipication_complexity
        >>> n = 1024
        >>> multipication_complexity(n)
        1048576
    """
    if n < Karatsuba_threshold:
        return n**2                                         # naive schoolbook multiplicatio
    elif n < ToomCook3_threshold:
        # Karatsuba with constant in bigOh being 1
        return n**(log(5)/log(3))
    elif n < FFT_threshold:
        # Toom-Cook3 with constant in bigOh being 1
        return n**(log(3)/log(2))
    else:
        # Schonhage-Strassen with constant in bigOh being 1
        return n*log2(n)*log2(log2(n))


def division_complexity(n):
    """Computes the time complexity of dividing a 2n-bit integer by an n-bit integer.
        See Thm. 1.4.2 in [BZ10]_ https://arxiv.org/pdf/1004.4710

    Args:
        n (int): bit length of the divisor

    Returns:
        float: the time complexity of the division operation

    Examples:
        >>> from cryptographic_estimators.IFEstimator.if_helper import division_complexity
        >>> n = 1024
        >>> division_complexity(n)
        1051648
    """
    if (n < 200):
        return n**2
    else:
        return 2*division_complexity(ceil(n/2))+2*multipication_complexity(ceil(n/2)) + n


def primality_testing(n):
    """Computes the time complexity of the Miller-Rabin primality test for an n-bit integer.
        Miller-Rabin primality test with #trials = k = 64 -> n is probably prime with probability at most 2^-2k

    Args:
        n (int): bit length of the integer to test for primality

    Returns:
        float: the time complexity of the Miller-Rabin primality test

    Examples:
        >>> from cryptographic_estimators.IFEstimator.if_helper import primality_testing
        >>> n = 1024
        >>> primality_testing(n)
        68719476736
    """
    # number of trials in the Miller-Rabin test
    k = 64
    return k*n**3

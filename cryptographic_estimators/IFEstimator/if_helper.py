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
from math import log2, log, ceil

def Lfunction(alpha, beta, logN):
    """
    implements the *exponent* of the L-function 
    L[alpha, beta] = exp((beta+o(1))*logN**alpha * log(logN)**(1-alpha) )


    INPUT:
    - ``alpha`` -- main constant in the L-function
    - ``beta`` -- another constant in the L-function
    - ``logN`` -- ln(N) of the number to factor
    """

    assert alpha >= 0
    assert beta  > 0
    assert alpha <= 1
    return beta*(logN**alpha)*(log(logN))**(1-alpha)

def pifunction(x):
    return ceil(x/log(x))

#as per https://gmplib.org/repo/gmp/file/tip/mpn/arm/gmp-mparam.h
limb = 32
Karatsuba_threshold = limb * 36
ToomCook3_threshold = limb * 125
FFT_threshold       = limb * 5760

#complexity of multiplication of 2 n-bit integers
def M(n):
    if   n<Karatsuba_threshold: return n**2                                         # naive schoolbook multiplicatio
    elif n<ToomCook3_threshold: return n**(log(5)/log(3))                 # Karatsuba with constant in bigOh being 1    
    elif n<FFT_threshold:       return n**(log(3)/log(2))                 # Toom-Cook3 with constant in bigOh being 1
    else:                       return n*log2(n)*log2(log2(n))       # Schonhage-Strassen with constant in bigOh being 1

#complexity of division of 2n-bit integer by n-bit integer
# Thm. 1.4.2 in https://arxiv.org/pdf/1004.4710
def D(n):
    if (n<200): return n**2
    else: return 2*D(ceil(n/2))+2*M(ceil(n/2)) + n

# Miller-Rabin primality test with #trials = k = 128 -> n is probably prime with probability at most 2^-2k
# input: bitsize of the number to test for primality
def primality_testing(n):
    k = 64
    return k*n**3
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

from math import comb as binomial, log2, factorial
from random import randint


def gv_distance(n: int, k: int, q: int):
    """Gilbert Varsharmov bound."""
    d = 1
    right_term = q ** (n - k)
    left_term = 0
    while left_term <= right_term:
        left_term += binomial(n, d) * (q - 1) ** d
        d += 1
    d = d - 1
    return d


def number_of_weight_d_codewords(n: int, k: int, q: int, d: int):
    """Returns the number of weight d code words in a (n,k,q) code."""
    return binomial(n, d) * (q - 1) ** d // q ** (n - k)

def random_sparse_vec_orbit(n: int, w: int, q: int):
    counts = [0] * (q - 1)
    s = 0
    while s < w:
        a = randint(0, q - 2)
        s += 1
        counts[a] += 1
    orbit_size = factorial(n) // factorial(n - w)
    for c in counts:
        orbit_size //= factorial(c)
    return log2(orbit_size)


def median_size_of_random_orbit(n: int, w: int, q: int):
    S = []
    for x in range(100):
        S.append(random_sparse_vec_orbit(n, w, q))
    S.sort()
    return S[49]


def hamming_ball(n: int, q: int, w: int):
    S = 0
    for i in range(0, w + 1):
        S += binomial(n, i) * (q - 1) ** i
    return log2(S)

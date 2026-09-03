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

from ..MQEstimator.MQAlgorithms import BooleanSolveFXL
from ..MQEstimator import MQProblem
from ..MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
from ..MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
from math import log2, inf, floor


def _optimize_k(n: int, m: int, k: int, q: int, w: float):
    """Find the optimal parameter `K` from Furue, Nakamura, and Takagi strategy.

    Args:
        n (int): Number of variables
        m (int): Number of polynomials
        k (int): Whipping parameter
        q (int): Order of the finite field
        w (float): Description not provided in original docstring
    """
    (K, time) = (0, inf)

    for i in range(0, n-1):
        m_tilde = m - floor((n-i)/(m-i)) + 1
        n_tilde = m_tilde - i

        if n_tilde < 1: break

        E = BooleanSolveFXL(MQProblem(n=n_tilde, m=m_tilde, q=q), bit_complexities=False, w=w)
        t = i * log2(q) + E.time_complexity()

        if t < time:
            time = t
            K = i

    return K


def fi_attack_compute_admissible_values_k(n: int, neqs: int, alpha: int, p: int, l: int):
    """Return the solving degrees and the number of columns of truncated Macaulay matrix width of every admissible k.

    A value k is admissible if
    H(n-k, neqs, s, d) <= T(alpha-k, s, d) for some 2 <= d <= (alpha - k) * (s - 1),
    where s = p^l is the truncation of the ring R(p^l).
    The solving degree D for a given k is the minimum d satisfying the above inequality.

    Args:
        n (int): Number of variables of the system before any coordinate is guessed.
        neqs (int): Number of linearly independent quadratic equations.
        alpha (int): Dimension of the linear solution space.
        p (int): Characteristic of the field, q = p^e.
        l (int): Truncation exponent l, giving the truncation s = p^l.
    Returns:
        A dictionary mapping each admissible k to the pair (D, ncols), where ncols is the number of
        columns of the truncated Macaulay matrix at degree D. A k with no solving degree, or whose
        matrix has no column, is dropped as outside the model.

    Examples:
        >>> from cryptographic_estimators.MAYOEstimator.mayo_helper import fi_attack_compute_admissible_values_k
        >>> fi_attack_compute_admissible_values_k(24, 10, 10, 2, 1)  # Equation (11) for (q, n, m) = (2, 24, 10)
        {0: (8, 735427), 1: (8, 490306), 2: (7, 170537), 3: (7, 116280)}
        >>> fi_attack_compute_admissible_values_k(24, 28, 6, 2, 1)  # Equation (13) for the same, alpha = 3m - n
        {0: (5, 42499), 1: (5, 33649)}
    """
    if not isinstance(l, int) or l < 1:
        raise ValueError("The truncation exponent l must be an integer with l >= 1.")

    s = p**l
    max_d = alpha * (s - 1)  # the degree bound at k = 0, the largest one

    # The monomial counts T(n-k, s, ) and T(alpha-k, s, ) of [FI26]_, and the left-hand side of the
    # condition, all at k = 0 to begin with.
    T_n = TruncatedNMonomialSeries(n, s, max_d + 1)
    T_a = TruncatedNMonomialSeries(alpha, s, max_d + 1)
    H = TruncatedHilbertSeries(n, neqs, s, max_d + 1)

    data = {}
    for k in range(min(alpha, n)):
        if k:
            T_n, T_a, H = T_n.remove_variable(), T_a.remove_variable(), H.remove_variable()

        D = next(
            (
                d
                for d in range(2, (alpha - k) * (s - 1) + 1)
                if H.coefficient_of_degree(d) <= T_a.nmonomials_of_degree(d)
            ),
            0,
        )
        if D == 0:
            continue

        ncols = T_n.nmonomials_of_degree(D) - T_a.nmonomials_of_degree(D) + 1
        if ncols > 0:
            data[k] = (D, ncols)

    return data


def fi_attack_first_admissible_l(n: int, neqs: int, alpha: int, p: int, max_l: int):
    """Return the first working l and its admissible values of k.

    Args:
        n (int): Number of variables before guessing coordinates.
        neqs (int): Number of linearly independent quadratic equations.
        alpha (int): Dimension of the linear solution space.
        p (int): Characteristic of the field.
        max_l (int): Largest truncation exponent to scan.
    Examples:
        >>> from cryptographic_estimators.MAYOEstimator.mayo_helper import fi_attack_first_admissible_l
        >>> l, admissible_values_k = fi_attack_first_admissible_l(24, 10, 10, 2, 1)
        >>> l
        1
        >>> admissible_values_k[0]
        (8, 735427)
        >>> fi_attack_first_admissible_l(2, 0, 1, 2, 1)
        (None, {})
    """
    for l in range(1, max_l + 1):
        admissible_values_k = fi_attack_compute_admissible_values_k(n, neqs, alpha, p, l)
        if admissible_values_k:
            return l, admissible_values_k
    return None, {}

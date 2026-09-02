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


def fi_attack_compute_admissible_values_k(
    n: int, neqs: int, alpha: int, p: int, l: int, precomputed_admissible_values_l: dict
):
    """Return the solving degree and the truncated Macaulay matrix width of every admissible k.

    A value k is admissible if
    H(n-k, neqs, s, d) <= T(alpha-k, s, d) for some 2 <= d <= (alpha - k) * (s - 1),
    where s = p^l is the truncation of the ring R(p^l).
    The solving degree D for a given k is the minimum d satisfying the above inequality.

    This is the scan shared by the attacks of [FI26]_ over R(p^l), each setting (neqs, alpha) to its
    own: Equation (11) to the m equations and the oil space of dimension o, Equation (13) to the
    3m - 2 equations and the intersection of the two oil spaces.

    Guessing k of the n coordinates leaves the system in n - k of them, so k runs up to
    min(alpha, n) - 1.

    The scan is expensive and each caller runs it for several l, so its result is stored in the
    caller's `precomputed_admissible_values_l` under l. Every call sharing that mapping must share
    (n, neqs, alpha, p) too.

    Args:
        n (int): Number of variables of the system before any coordinate is guessed.
        neqs (int): Number of linearly independent quadratic equations.
        alpha (int): Dimension of the linear solution space.
        p (int): Characteristic of the field, q = p^e.
        l (int): Truncation exponent l, giving the truncation s = p^l.
        precomputed_admissible_values_l (dict): Mapping of each l already scanned to the admissible
            values of k it gave, read and written in place.

    Returns:
        A dictionary mapping each admissible k to the pair (D, ncols), where ncols is the number of
        columns of the truncated Macaulay matrix at degree D. A k with no solving degree, or whose
        matrix has no column, is dropped as outside the model.

    Examples:
        >>> from cryptographic_estimators.MAYOEstimator.mayo_helper import fi_attack_compute_admissible_values_k
        >>> precomputed_admissible_values_l = {}
        >>> fi_attack_compute_admissible_values_k(24, 10, 10, 2, 1, precomputed_admissible_values_l)  # Equation (11) for (q, n, m) = (2, 24, 10)
        {0: (8, 735427), 1: (8, 490306), 2: (7, 170537), 3: (7, 116280)}
        >>> precomputed_admissible_values_l[1] is fi_attack_compute_admissible_values_k(24, 10, 10, 2, 1, precomputed_admissible_values_l)
        True
        >>> fi_attack_compute_admissible_values_k(24, 28, 6, 2, 1, {})  # Equation (13) for the same, alpha = 3m - n
        {0: (5, 42499), 1: (5, 33649)}
    """
    if l in precomputed_admissible_values_l:
        return precomputed_admissible_values_l[l]

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

    precomputed_admissible_values_l[l] = data
    return data


def fi_attack_are_parameters_invalid(k: int, admissible_values_k: dict):
    """Return whether k is outside the optimisation at the truncation it was scanned for.

    Which truncation exponents ell are offered at all is not shared, and stays with each attack.

    Args:
        k (int): Number of guessed coordinates.
        admissible_values_k (dict): Output of `fi_attack_compute_admissible_values_k` for the
            truncation in question.

    Examples:
        >>> from cryptographic_estimators.MAYOEstimator.mayo_helper import fi_attack_are_parameters_invalid
        >>> fi_attack_are_parameters_invalid(1, {0: (5, 42499), 1: (5, 33649)})
        False
        >>> fi_attack_are_parameters_invalid(2, {0: (5, 42499), 1: (5, 33649)})
        True
    """
    return k not in admissible_values_k

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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...base_algorithm import optimal_parameter
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from ...helper import gf_order_to_characteristic, gf_order_to_degree
from ...MQEstimator.series.truncated_hilbert import TruncatedHilbertSeries
from ...MQEstimator.series.truncated_nmononials import TruncatedNMonomialSeries
from math import log2, inf, comb as binomial


class ReconciliationFI(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of the Furue-Ikematsu reconciliation attack estimator.

        This is the reconciliation attack of Furue and Ikematsu carried out over the
        p^ell-truncated polynomial ring R(p^ell) = F_q[x_1, ..., x_n] / <x_1^(p^ell), ..., x_n^(p^ell)>,
        where q = p^e. Section 4.3 of [FI26]_.
        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            **kwargs: Additional keyword arguments.
                max_l (int): Upper bound on the truncation exponent ell (default: e, where q = p^e).
                    Equation (11) of [FI26]_ ranges over 1 <= ell <= e; lowering this bound cuts the
                    upward scan short, and has no effect whenever ell = 1 is already admissible.
                h (int, optional): External hybridization parameter. Defaults to 0.
                memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                    or deploy custom function which takes as input the logarithm of the total memory usage.
                complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
                bit_complexities (int, optional): Determines if complexity is given in bit operations or
                    basic operations. Defaults to 1 (in bit).

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E
            ReconciliationFI estimator for the MAYO signature scheme with parameters (n, m, o, k, q) = (86, 78, 8, 10, 16)
        """
        super().__init__(problem, **kwargs)

        _, _, o, _, q = self.problem.get_parameters()
        self._p = gf_order_to_characteristic(q)
        self._e = gf_order_to_degree(q)
        self._o = o
        self._max_l = kwargs.get("max_l", self._e)

        if not isinstance(self._max_l, int) or not 1 <= self._max_l <= self._e:
            raise ValueError(f"max_l must be in the range 1 <= max_l <= {self._e}")

        self._series_data = {}
        # 0 marks the first admissible truncation exponent as not yet computed; None marks the
        # computed absence of one, so the two cases must not be conflated.
        self._first_l = 0
        self.set_parameter_ranges("k", 0, self._o - 1)
        self.set_parameter_ranges("l", 1, self._max_l)
        self._name = "ReconciliationFI"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    def _truncation(self, l: int):
        """Return the truncation s = p^ell of the ring R(p^ell).

        Args:
            l (int): Truncation exponent ell.
        """
        if not isinstance(l, int) or not 1 <= l <= self._e:
            raise ValueError(
                f"The truncation exponent l must be an integer with 1 <= l <= {self._e}."
            )
        return self._p**l

    def _compute_admissible_values_k(self, l: int):
        """Return the solving degree and the number of columns of the truncated Macaulay matrix
        width of every admissible k, for a fixed ell.

        A value k is admissible if H(n-k, m, p^l, d) <= T(o-k, p^l, d) (Equation (11) of [FI26]_)
        for some 2 <= d <= max_d, where max_d = (o - k) * (p^ell - 1). The minimum d fulfilling the
        above inequality is the solving degree for (k, l).

        The scan is exact and needs a single pass. Its degree range is widest at k = 0, so expanding
        the series once to max_d = o * (p^ell - 1) covers every k: a k with no solving degree here
        has none at all, and there is no truncation status to report or expansion to grow and retry.
        The result is cached per ell in `_series_data`.

        Args:
            l (int): Truncation exponent ell.
        """
        if l in self._series_data:
            return self._series_data[l]

        n, m, o, _, _ = self.problem.get_parameters()
        s = self._truncation(l)  # p^l
        max_d = (o - 0) * (s - 1)  # the degree bound of Equation (11) at k = 0, the largest one

        # The monomial counts T(n-k, p^l, ) and T(o-k, p^l, ) of [FI26]_, and the left-hand side of
        # Equation (11). They start at k = 0 and are pushed to the next k by removing one variable,
        # which is one exact series division each rather than a fresh expansion.
        T_n = TruncatedNMonomialSeries(n, s, max_d + 1)  # Initially symply T(n, p^l, )
        T_o = TruncatedNMonomialSeries(o, s, max_d + 1)  # The monomial counts T(o, p^l, )
        H_n_m = TruncatedHilbertSeries(n, m, s, max_d + 1)

        data = {}
        for k in range(o):
            if k:
                T_n, T_o, H_n_m = T_n.remove_variable(), T_o.remove_variable(), H_n_m.remove_variable()

            max_d = (o - k) * (s - 1)
            D = next(
                (
                    d
                    for d in range(2, max_d + 1)
                    if H_n_m.coefficient_of_degree(d) <= T_o.nmonomials_of_degree(d)
                ),
                0,
            )
            if D == 0:
                continue

            # ncols is the number of columns of the truncated Macaulay matrix dimension
            ncols = T_n.nmonomials_of_degree(D) - T_o.nmonomials_of_degree(D) + 1
            if ncols > 0:
                data[k] = (D, ncols)

        self._series_data[l] = data
        return data

    def _first_admissible_truncation_exponent(self):
        """Return the smallest ell in [1, max_l] for which some k admits a solving degree.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E._first_admissible_truncation_exponent()
            3
        """
        if self._first_l == 0:
            self._first_l = next(
                (l for l in range(1, self._max_l + 1) if self._compute_admissible_values_k(l)),
                None,
            )
        return self._first_l

    def _are_parameters_invalid(self, parameters: dict):
        """Return whether the given parameters are outside the optimisation.

        Only the first admissible truncation exponent is considered, and only those k that admit a
        solving degree for it.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        l, k = parameters["l"], parameters["k"]
        if l != self._first_admissible_truncation_exponent():
            return True
        return k not in self._compute_admissible_values_k(l)

    @optimal_parameter
    def k(self):
        """Return the optimal number k of guessed coordinates.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.k()
            2
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def l(self):
        """Return the truncation exponent ell, the first one admitting a solving degree.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.l()
            3
        """
        return self._get_optimal_parameter("l")

    def D(self):
        """Return the degree D of the Macaulay matrix at the optimal parameters.

        D is deliberately not an `@optimal_parameter`, and so does not appear in
        `optimal_parameters()` nor in the parameters column of `table(show_all_parameters=True)`.
        It is not a free parameter: Equation (11) of [FI26]_ determines it from (k, ell) as the
        least admissible degree, so it is a function of the optimum rather than a dimension of the
        search. Decorating it would enrol it in the cartesian product enumerated by
        `_valid_choices`, whose only effect would be to reject every value but the derived one, at a
        cost of |k| * |ell| * |D| iterations instead of |k| * |ell| -- for uov-V that is 18.8 million
        rather than 768, seconds of enumeration per estimate rather than milliseconds. `D()` is
        therefore exposed as a plain method here and on the UOV algorithm that delegates to it.

        Returns None when the attack has no valid parameters, as `l()` and `k()` do.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.D()
            41
            >>> E.optimal_parameters()
            {'k': 2, 'l': 3}
        """
        l, k = self.l(), self.k()
        if l is None or k is None:
            return None
        return self._compute_admissible_values_k(l)[k][0]

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.time_complexity()
            238.16366360451318
            >>> (E.l(), E.k(), E.D())
            (3, 2, 41)
        """
        n, _, _, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = self._compute_admissible_values_k(l)
        if k not in data:
            return inf
        _, ncols = data[k]
        # Equation (12) of [FI26]_, in log2 of F_q operations. The base class converts this to gates
        # via MAYOProblem.to_bitcomplexity_time; with theta=None that factor is 2*log2(q)^2 + log2(q),
        # which is the conversion Section 5 of [FI26]_ applies to produce its tables. The squaring is
        # the Wiedemann cost of a sparse system, not dense linear algebra, so `w` does not occur.
        return log2(3 * binomial(n - k + 1, 2) * ncols**2)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        [FI26]_ gives no memory complexity. We report the number of field elements needed to store
        the sparse Macaulay matrix, namely its number of columns times the number
        binomial(n-k+1, 2) of nonzero entries per row used by the time complexity.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_fi import ReconciliationFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = ReconciliationFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.memory_complexity()
            123.60524223063307
        """
        n, _, _, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = self._compute_admissible_values_k(l)
        if k not in data:
            return inf
        _, ncols = data[k]
        return log2(binomial(n - k + 1, 2) * ncols)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

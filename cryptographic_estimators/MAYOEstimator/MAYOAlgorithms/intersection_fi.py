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
from ..mayo_helper import (
    fi_attack_are_parameters_invalid,
    fi_attack_compute_admissible_values_k,
)
from math import log2, inf, comb as binomial


class IntersectionFI(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of the Furue-Ikematsu intersection attack estimator.

        This is the intersection attack of Beullens [Beu20]_ carried out over the
        p^ell-truncated polynomial ring R(p^ell) = F_q[x_1, ..., x_n] / <x_1^(p^ell), ..., x_n^(p^ell)>,
        where q = p^e. Section 4.3 of [FI26]_.

        The two oil spaces meet in dimension 3o - n when n < 3o, and only with probability
        q^-(n - 3o + 1) otherwise. Every instance is estimated by Equations (13) to (16) of [FI26]_
        as written, including one whose oil space is larger than its vinegar space; where those
        equations admit no k the attack is reported as inapplicable, as for any other parameters.

        An oil space of dimension o > n would make the public key trivially invertible and the
        instance solvable in polynomial time, but no such instance can be built: `MAYOProblem`
        requires k < n - o, which rejects every o >= n at construction for the k >= 0 that MAYO
        allows. There is therefore no such case to estimate here.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            **kwargs: Additional keyword arguments.
                max_l (int): Upper bound on the truncation exponent ell (default: e, where q = p^e).
                    Equations (13) and (15) of [FI26]_ range over 1 <= ell <= e, and the estimate is
                    the cheapest over that range; lowering this bound restricts the minimisation to
                    1 <= ell <= max_l, which is only worth doing to shorten the search.
                h (int, optional): External hybridization parameter. Defaults to 0.
                memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                    or deploy custom function which takes as input the logarithm of the total memory usage.
                complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
                bit_complexities (int, optional): Determines if complexity is given in bit operations or
                    basic operations. Defaults to 1 (in bit).

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E
            IntersectionFI estimator for the MAYO signature scheme with parameters (n, m, o, k, q) = (86, 78, 8, 10, 16)
        """
        super().__init__(problem, **kwargs)

        n, m, o, _, q = self.problem.get_parameters()
        self._p = gf_order_to_characteristic(q)
        self._e = gf_order_to_degree(q)
        self._max_l = kwargs.get("max_l", self._e)

        if not isinstance(self._max_l, int) or not 1 <= self._max_l <= self._e:
            raise ValueError(f"max_l must be in the range 1 <= max_l <= {self._e}")

        # The number of linearly independent equations of the system (4) of [FI26]_: 3m equations,
        # two of which are dependent.
        self._neqs = 3 * m - 2

        if n < 3 * o:
            # v < 2o: the two subspaces always meet, in dimension 2o - v = 3o - n.
            self._alpha = 3 * o - n
            self._log_repetitions = 0.0
        else:
            # 2o <= v: they meet with probability q^-(v - 2o + 1), and [FI26]_ counts only the
            # intersections of dimension 1, larger ones being both rarer and no cheaper.
            self._alpha = 1
            self._log_repetitions = (n - 3 * o + 1) * log2(q)

        self._precomputed_admissible_values_l = {}
        self.set_parameter_ranges("k", 0, self._alpha - 1)
        self.set_parameter_ranges("l", 1, self._max_l)
        self._name = "IntersectionFI"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    def _are_parameters_invalid(self, parameters: dict):
        """Return whether the given parameters are outside the optimisation.

        Every pair (ell, k) admitting a solving degree is a candidate, the optimiser keeping the
        cheapest, as the code of Appendix D of [FI26]_ does. A larger ell is not always dearer, six
        rows of Table 8 of [FI26]_ being cheapest at ell > 1 though admissible at ell = 1.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        l, k = parameters["l"], parameters["k"]
        # Equation (13) of [FI26]_ is the shared scan with the 3m - 2 equations of this attack and
        # with the intersection of the two oil spaces, of dimension alpha, as the solution space;
        # with alpha = 1 it is Equation (15), whose right-hand side T(1, s, d) is 1 throughout.
        n, _, _, _, _ = self.problem.get_parameters()
        return fi_attack_are_parameters_invalid(
            k,
            fi_attack_compute_admissible_values_k(
                n, self._neqs, self._alpha, self._p, l, self._precomputed_admissible_values_l
            ),
        )

    @optimal_parameter
    def k(self):
        """Return the optimal number k of guessed coordinates.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.k()
            0
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def l(self):
        """Return the truncation exponent ell minimising Equation (14) of [FI26]_.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.l()
            4
        """
        return self._get_optimal_parameter("l")

    def D(self):
        """Return the degree D of the Macaulay matrix at the optimal parameters.

        Returns None when the attack has no valid parameters, as `l()` and `k()` do.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.D()
            9
            >>> E.optimal_parameters()
            {'k': 0, 'l': 4}
        """
        l, k = self.l(), self.k()
        if l is None or k is None:
            return None

        n, _, _, _, _ = self.problem.get_parameters()
        return fi_attack_compute_admissible_values_k(
            n, self._neqs, self._alpha, self._p, l, self._precomputed_admissible_values_l
        )[k][0]

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.time_complexity()
            350.52849102410624
            >>> (E.l(), E.k(), E.D())
            (4, 0, 9)
        """
        n, _, _, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = fi_attack_compute_admissible_values_k(
            n, self._neqs, self._alpha, self._p, l, self._precomputed_admissible_values_l
        )
        if k not in data:
            return inf
        _, ncols = data[k]
        return log2(3 * binomial(n - k + 1, 2) * ncols**2) + self._log_repetitions

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        [FI26]_ gives no memory complexity. We report the number of field elements needed to store
        the sparse Macaulay matrix, namely its number of columns times the number
        binomial(n-k+1, 2) of nonzero entries per row used by the time complexity. The repetitions
        of Equation (16) of [FI26]_ reuse that storage, so they do not enter here.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = IntersectionFI(MAYOProblem(n=86, m=78, o=8, k=10, q=16))
            >>> E.memory_complexity()
            53.82140588624681
        """
        n, _, _, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = fi_attack_compute_admissible_values_k(
            n, self._neqs, self._alpha, self._p, l, self._precomputed_admissible_values_l
        )
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

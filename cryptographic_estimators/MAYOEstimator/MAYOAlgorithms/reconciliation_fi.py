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
    fi_attack_first_admissible_l,
)
from math import log2, inf, comb as binomial


class ReconciliationFI(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of the Furue-Ikematsu reconciliation attack estimator.

        This is the reconciliation attack of Furue and Ikematsu carried out over the
        p^ell-truncated polynomial ring R(p^ell) = F_q[x_1, ..., x_n] / <x_1^(p^ell), ..., x_n^(p^ell)>,
        where q = p^e [FI26]_.

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

        self._first_working_l = None
        self._admissible_values_k = {}
        self._first_working_l_is_computed = False
        self.set_parameter_ranges("k", 0, self._o - 1)
        self.set_parameter_ranges("l", 1, self._max_l)
        self._name = "ReconciliationFI"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    def _are_parameters_invalid(self, parameters: dict):
        """Return whether the given parameters are outside the optimisation.

        Only the first admissible truncation exponent is considered, and only those k that admit a
        solving degree for it.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        l, k = parameters["l"], parameters["k"]
        n, m, o, _, _ = self.problem.get_parameters()
        if not self._first_working_l_is_computed:
            self._first_working_l, self._admissible_values_k = fi_attack_first_admissible_l(
                n, m, o, self._p, self._max_l
            )
            self._first_working_l_is_computed = True
        return l != self._first_working_l or k not in self._admissible_values_k

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

        n, m, o, _, _ = self.problem.get_parameters()
        return self._admissible_values_k[k][0]

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
        n, m, o, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = self._admissible_values_k
        if k not in data:
            return inf
        _, ncols = data[k]
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
        n, m, o, _, _ = self.problem.get_parameters()
        l, k = parameters["l"], parameters["k"]
        data = self._admissible_values_k
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

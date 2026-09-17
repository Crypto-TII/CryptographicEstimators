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


from ..uov_algorithm import UOVAlgorithm
from ..uov_problem import UOVProblem
from ...base_algorithm import optimal_parameter
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from ...MAYOEstimator.MAYOAlgorithms.intersection_fi import IntersectionFI as IntersectionFIMAYO
from ...MAYOEstimator.mayo_problem import MAYOProblem


class IntersectionFI(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of the Furue-Ikematsu intersection attack estimator.

        This is the intersection attack of Beullens [Beu20]_, carried out over the
        p^ell-truncated polynomial ring R(p^ell) = F_q[x_1, ..., x_n] / <x_1^(p^ell), ..., x_n^(p^ell)>,
        where q = p^e. Section 4.3 of [FI26]_. A UOV public key is a MAYO public key with o = m and
        k = 1, so the estimate is the one of the MAYO algorithm of the same name.

        Note that the parameter k below is the number of guessed coordinates of [FI26]_, unlike the
        k of `UOVEstimator.UOVAlgorithms.intersection_attack.IntersectionAttack`, which is the
        number of public key matrices combined by [Beu20]_. Here that number is fixed at two, the
        setting [FI26]_ found most efficient against the proposed parameters.

        Args:
            problem (UOVProblem): An instance of the UOVProblem class.
            **kwargs: Additional keyword arguments.
                max_l (int): Upper bound on the truncation exponent ell (default: e, where q = p^e).
                    Equations (13) and (15) of [FI26]_ range over 1 <= ell <= e; lowering this bound
                    cuts the upward scan short, and has no effect whenever ell = 1 is already
                    admissible.
                h (int, optional): External hybridization parameter. Defaults to 0.
                memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                    Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                    or deploy custom function which takes as input the logarithm of the total memory usage.
                complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
                bit_complexities (int, optional): Determines if complexity is given in bit operations or
                    basic operations. Defaults to 1 (in bit).

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E
            IntersectionFI estimator for the UOV signature scheme with parameters (q, n, m) = (256, 112, 44)
        """
        super().__init__(problem, **kwargs)

        n, m, q = self.problem.get_parameters()
        mayo_kwargs = {"bit_complexities": 0}
        if "max_l" in kwargs:
            mayo_kwargs["max_l"] = kwargs["max_l"]
        self._E = IntersectionFIMAYO(MAYOProblem(n=n, m=m, o=m, q=q, k=1), **mayo_kwargs)
        self.set_parameter_ranges("k", 0, self._E._alpha - 1)
        self.set_parameter_ranges("l", 1, self._E._max_l)
        self._name = "IntersectionFI"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    def _are_parameters_invalid(self, parameters: dict):
        """Return whether the given parameters are outside the optimisation.

        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self._E._are_parameters_invalid(parameters)

    @optimal_parameter
    def k(self):
        """Return the optimal number k of guessed coordinates.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E.k()
            7
        """
        return self._E._get_optimal_parameter("k")

    @optimal_parameter
    def l(self):
        """Return the truncation exponent ell, the first one admitting a solving degree.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E.l()
            1
        """
        return self._E._get_optimal_parameter("l")

    def D(self):
        """Return the degree D of the Macaulay matrix at the optimal parameters.

        As on the MAYO algorithm this delegates to, D is derived from (k, ell) by Equation (13) of
        [FI26]_ rather than searched, so it is not an `@optimal_parameter` and does not appear in
        `optimal_parameters()` or in the parameters column of the estimator tables. See
        `MAYOEstimator.MAYOAlgorithms.intersection_fi.IntersectionFI.D`.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E.D()
            13
            >>> E.optimal_parameters()
            {'k': 7, 'l': 1}
        """
        return self._E.D()

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E.time_complexity()
            128.37924912118416
            >>> (E.l(), E.k(), E.D())
            (1, 7, 13)
        """
        return self._E._compute_time_complexity(parameters)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_fi import IntersectionFI
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionFI(UOVProblem(n=112, m=44, q=256, theta=None))
            >>> E.memory_complexity()
            69.07449487572099
        """
        return self._E._compute_memory_complexity(parameters)

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

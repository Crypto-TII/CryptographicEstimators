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
from math import log2, inf, floor, comb as binomial
from cryptographic_estimators.base_constants import BASE_KEY_RECOVERY_ATTACK


class WedgeAttack(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of WedgeAttack estimator.

        The wedge attack is a key-recovery attack introduced by Larns Ran in [Ran24]_.

        Args:
            problem (MAYOProblem): Object including all necessary parameters
            w: Linear algebra constant (default: obtained from MAYOAlgorithm)
            h (int, optional): External hybridization parameter. Defaults to 0.
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                or deploy custom function which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
            bit_complexities (int, optional): Determines if complexity is given in bit operations or basic operations. Defaults to 1 (in bit).
        """
        super().__init__(problem, **kwargs)

        n, m, o, _, q = self.problem.get_parameters()
        v = n - o
        self.set_parameter_ranges('o_prime', 2 * v // m + 1 + 1, o)
        self._name = "WedgeAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    @optimal_parameter
    def o_prime(self):
        """Return the optimal parameter k used in the algorithm optimization.

            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.wedge_attack import WedgeAttack
            >>> E = WedgeAttack(MAYOProblem(n=80, m=60, o=17, k=9, q=16))
            >>> E.o_prime()
            13
        """
        return self._get_optimal_parameter("o_prime")

    def is_admissible(self, o_prime: int):
        """Return True if the wedge attack would work with the input parameters."""
        n, m, o, _, _ = self.problem.get_parameters()
        v = n - o
        tmp = sum([pow(-1, i) * binomial(m + i - 1, i) * binomial(v + o_prime, v + 2 * i) for i in range(0, floor(o_prime/2))])
        if tmp <= 1:
            return True
        return False

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.wedge_attack import WedgeAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = WedgeAttack(MAYOProblem(n=81, m=64, o=17, k=9, q=16))
            >>> E.time_complexity()
            112.59106798593434
        """
        n, m, o, _, _ = self.problem.get_parameters()
        o_prime = parameters["o_prime"]
        if self.is_admissible(o_prime):
            v = n - o
            return log2(3) + log2(binomial(v + 2, 2)) + 2 * log2(binomial(v + o_prime, v))
        return inf

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.wedge_attack import WedgeAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = WedgeAttack(MAYOProblem(n=81, m=64, o=17, k=9, q=16))
            >>> E.memory_complexity()
            105.83618048377087
        """
        n, m, o, _, q = self.problem.get_parameters()
        o_prime = parameters["o_prime"]
        if self.is_admissible(o_prime):
            v = n - o
            return log2(binomial(v + o_prime, v)) - log2(log2(q)) + log2(binomial(v + 2, 2)) + log2(binomial(v + o_prime, v))
        return inf

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

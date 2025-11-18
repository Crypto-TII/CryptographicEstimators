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
from math import log2, inf, floor, comb as binomial
from cryptographic_estimators.base_constants import BASE_KEY_RECOVERY_ATTACK
from ...MAYOEstimator.MAYOAlgorithms.wedge_attack import WedgeAttack as WedgeAttackMAYO
from ...MAYOEstimator.mayo_problem import MAYOProblem

class WedgeAttack(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of WedgeAttack estimator.

        The wedge attack is a key-recovery attack introduced by Larns Ran in [Ran24]_.

        Args:
            problem (UOVProblem): Object including all necessary parameters
            w: Linear algebra constant (default: obtained from MAYOAlgorithm)
            h (int, optional): External hybridization parameter. Defaults to 0.
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                or deploy custom function which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
            bit_complexities (int, optional): Determines if complexity is given in bit operations or basic operations. Defaults to 1 (in bit).
        """
        super().__init__(problem, **kwargs)

        n, m, q = self.problem.get_parameters()
        v = n - m
        self.set_parameter_ranges('o_prime', 2 * v // m + 1 + 1, m)
        self._name = "WedgeAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK
        self._E = WedgeAttackMAYO(MAYOProblem(n=n, m=m, o=m, q=q, k=1), bit_complexities=0)


    @optimal_parameter
    def o_prime(self):
        """Return the optimal parameter k used in the algorithm optimization.

            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.wedge_attack import WedgeAttack
            >>> E = WedgeAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.o_prime()
            7
        """
        return self._E._get_optimal_parameter("o_prime")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.wedge_attack import WedgeAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = WedgeAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.time_complexity()
            42.146339998376874
        """
        n, m, _ = self.problem.get_parameters()
        o_prime = parameters["o_prime"]
        if self._E.is_admissible(o_prime):
            v = n - m
            return log2(3) + log2(binomial(v + 2, 2)) + 2 * log2(binomial(v + o_prime, v))
        return inf

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.wedge_attack import WedgeAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = WedgeAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.memory_complexity()
            40.56137749765571
        """
        n, m, q = self.problem.get_parameters()
        o_prime = parameters["o_prime"]
        if self._E.is_admissible(o_prime):
            v = n - m
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

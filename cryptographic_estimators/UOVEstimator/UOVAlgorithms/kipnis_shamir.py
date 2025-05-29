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
from math import log2
from cryptographic_estimators.base_constants import BASE_KEY_RECOVERY_ATTACK


class KipnisShamir(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of Kipnis-Shamir estimator.

        In [Beu20]_, Kipnis and Shamir proposed a powerful attack against the balanced Oil
        and Vinegar signature scheme (n = 2v), which finds an equivalent private key in
        polynomial time. This key can then be used to generate signatures for arbitrary
        messages.

        Args:
            problem (UOVProblem): An instance of the UOVProblem class.
            **kwargs: Additional keyword arguments.
                memory_access: Specifies the memory access cost model (default: 0, choices: 
                    0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy 
                    custom function which takes as input the logarithm of the total memory usage).
                complexity_type: Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).
        """

        super().__init__(problem, **kwargs)

        n, m, _ = self.problem.get_parameters()
        
        if n <= 2 * m:
            raise ValueError('n should be greater than 2 * m')

        self._name = "Kipnis-Shamir"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.kipnis_shamir import KipnisShamir
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = KipnisShamir(UOVProblem(n=24, m=10, q=2))
            >>> E.time_complexity()
            16.837895002019238
        """
        n, m, q = self.problem.get_parameters()
        time = (n - 2 * m) * log2(q)
        return time + log2(n) * 2.8

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.kipnis_shamir import KipnisShamir
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = KipnisShamir(UOVProblem(n=24, m=10, q=2))
            >>> E.memory_complexity()
            12.491853096329674
        """
        n, m, _ = self.problem.get_parameters()
        return log2(m * (n ** 2))
    
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

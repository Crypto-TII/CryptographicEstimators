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


from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.helper import is_power_of_two
from math import log2


class KPG(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of KPG estimator.

        The KPG is an algorithm to solve a quadratic system of equations over fields of even characteristic [KPG99]_.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            w (float): Linear algebra constant (2 <= w <= 3). (default: 2.81)
            memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
            complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O comp).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E
            KPG estimator for the MQ problem with 183 variables and 12 polynomials

        Tests:
            >>> E.problem.nvariables() == E.nvariables_reduced()
            True
        """

        n, m, q = problem.get_problem_parameters()
        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if not is_power_of_two(q):
            raise ValueError("the order of finite field q must be a power of 2")

        if m * (m + 1) >= n:
            raise ValueError("The condition m(m + 1) < n must be satisfied")

        super().__init__(problem, **kwargs)
        self._name = "KPG"
        self._n_reduced = n
        self._m_reduced = m

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E.time_complexity()
            26.628922047916475
        """
        n, m, _ = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        return log2(m * n**w)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.kpg import KPG
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = KPG(MQProblem(n=183, m=12, q=4), w=2.8)
            >>> E.memory_complexity()
            19.61636217728924
        """
        n, m, _ = self.problem.get_problem_parameters()
        return log2(m * n**2)

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters."""
        return 0

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Computes the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
        """
        return 0

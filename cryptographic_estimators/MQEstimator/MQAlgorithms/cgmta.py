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


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from math import log2, sqrt, floor, comb as binomial


class CGMTA(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of CGMT-A estimator.

        CGMT-A is an algorithm to solve the MQ problem over any finite field. It works when there is an integer $k$ such that $m - 2k < 2k^2 \\leq n - 2k$ [CGMT02]_.

        Note:
            In this module the complexities are computed for k = min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2)))).

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
            h (Optional[float]): External hybridization parameter (default: 0).
            memory_access (Optional[int]): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
            complexity_type (Optional[int]): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = CGMTA(MQProblem(n=41, m=10, q=3))
            >>> E
            CGMT-A estimator for the MQ problem with 41 variables and 10 polynomials

        Tests:
            >>> E.problem.nvariables() == E.nvariables_reduced()
            True
        """

        n, m, q = problem.get_problem_parameters()
        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if m > n:
            raise ValueError("m must be <= n")

        super().__init__(problem, **kwargs)
        self._k = min(m / 2, floor(sqrt(n / 2 - sqrt(n / 2))))

        if 2 * self._k**2 > n - 2 * self._k or m - 2 * self._k >= 2 * self._k**2:
            raise ValueError("The condition m - 2k < 2k^2 <= n - 2k must be satisfied")

        self._name = "CGMT-A"
        self._n_reduced = n
        self._m_reduced = m

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = CGMTA(MQProblem(n=41, m=10, q=3), bit_complexities=False)
            >>> E.time_complexity()
            23.137080884841787
        """
        n, m, q = self.problem.get_problem_parameters()
        k = self._k
        time = (m - k) * log2(q)
        time += log2(2 * k * binomial(n - k, 2))
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Compute the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary containing the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.cgmta import CGMTA
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = CGMTA(MQProblem(n=41, m=10, q=3), bit_complexities=False)
            >>> E.memory_complexity()
            7.339850002884624
        """
        q = self.problem.order_of_the_field()
        k = self._k
        memory = k * log2(q)
        memory += log2(2 * k)
        return memory

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
        """
        _, m, q = self.problem.get_problem_parameters()
        k = self._k
        return (m - k) * log2(q)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Compute the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        q = self.problem.order_of_the_field()
        k = self._k
        return k * log2(q)

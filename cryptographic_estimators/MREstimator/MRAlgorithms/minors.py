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

from ...MREstimator.mr_algorithm import MRAlgorithm
from ...MREstimator.mr_problem import MRProblem
from ...base_algorithm import optimal_parameter
from ..mr_constants import MR_SERIES_PRECISION
from math import log2, inf
from ..mr_helper import determinantal_series, predict_solving_degree, linear_monomial_series
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS

def minors_series(q, m, n, k, r, precision=None):
    """Return the Minors series with field equations."""
    return determinantal_series(q, m, n, k, r, dc=0, precision=precision)


class Minors(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of Minors estimator.

        Args:
            problem (MRProblem): An instance of the MRProblem class
            **kwargs: Additional keyword arguments
                w (int): Linear algebra constant (default: 3)
                theta (int): Exponent of the conversion factor (default: 2)

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> E = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> E
            Minors estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """
        super(Minors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()

        if k >= (m - r) * (n - r):
            raise ValueError(
                "It should hold that k < (m - r) * (n - r)")

        self.set_parameter_ranges('a', 0, min(n - r, (k - 1) // m))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self._name = "Minors"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. number of vectors to guess in the kernel of the low-rank matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> ME.a()
            1

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """Return the optimal `lv`, i.e. number of entries to guess in the solution.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> ME.lv()
            3

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.lv()
            0
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _ME_time_memory_complexity_helper_(self, q, m, n_reduced, k_reduced, r, time_mem):
        """Return the cost of Minors with field equations from [ABCPSV]_."""
        if k_reduced <= 0 or n_reduced <= r:
            return 0
        series = minors_series(q, m, n_reduced, k_reduced, r)
        D = predict_solving_degree(series, MR_SERIES_PRECISION)
        ncols = linear_monomial_series(q, k_reduced, D)
        if time_mem == 'time':
            return self._w * log2(ncols)
        return 2 * log2(ncols)

    def _are_parameters_invalid(self, parameters):
        """Reject guesses that leave no instance for the internal solver."""
        return self._are_hybrid_parameters_invalid(parameters['a'], parameters['lv'])

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.time_complexity()
            145.10336785629784
        """
        if self._are_parameters_invalid(parameters):
            return inf
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ME_time_memory_complexity_helper_(q, m, n_reduced, k_reduced, r, "time")
        reduction_cost = self.hybrid_reduction_cost(a, lv)
        time += self._log2_sum(time_complexity, reduction_cost)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.memory_complexity()
            16.11756193939414
        """

        if self._are_parameters_invalid(parameters):
            return inf
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory_attack = self._ME_time_memory_complexity_helper_(q, m, n_reduced, k_reduced, r, "memory")
        memory_store_matrices = log2((k + 1) * m * n)
        memory = max(memory_attack, memory_store_matrices)
        return memory

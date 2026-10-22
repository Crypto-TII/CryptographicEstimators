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
from math import log2, ceil, inf
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS


class KernelSearch(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of KernelSearch estimator.

        Uses the improved kernel-search cost from [ABCPSV]_ on each reduced instance,
        falling back to the original kernel search when only one kernel vector is needed.

        Args:
            problem (MRProblem): An instance of the MRProblem class
            **kwargs: Additional keyword arguments
                w (int): Linear algebra constant (default: 3)
                theta (int): Exponent of the conversion factor (default: 2)

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> E = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> E
            KernelSearch estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """
        super(KernelSearch, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, (k - 1) // m))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self._name = "KernelSearch"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. number of vectors to guess in the kernel of the low-rank matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> KS.a()
            1

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.a()
            4
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """Return the optimal `lv`, i.e. number of entries to guess in the solution.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> KS.lv()
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.lv()
            3
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _rank_check_cost(self, m, n, k):
        """Return the logarithmic cost of constructing the matrix and checking its rank."""
        return log2(k * m * n + max(m, n) * min(m, n) ** (self._w - 1))

    def _process_guess_kernel_cost(self, m, k, r, a):
        """Return the logarithmic cost of steps 2 and 3 of the original kernel search."""
        comp_step_2 = a * (k + 1) * r * m
        comp_step_3 = max(a * m, k + 1) * min(a * m, k + 1) ** (self._w - 1)
        return log2(comp_step_2 + comp_step_3)

    def _kernel_search(self, q, m, n, k, r):
        """Return the original kernel-search cost."""
        a = ceil(k / m)
        log_cpsi_ker = self._process_guess_kernel_cost(m, k, r, a)
        log_check = -(a * m - k) * log2(q) + self._rank_check_cost(m, n, k)
        return a * r * log2(q) + self._log2_sum(log_cpsi_ker, log_check)

    def _process_guess_improved_cost(self, q, m, n, k_p, r, a):
        """Return the logarithmic cost of improved guess processing."""
        comp_step_2 = (a - 1) * (k_p + 1) * r * m
        comp_step_3 = (k_p + 1) * ((a - 1) * m) ** (self._w - 1)
        comp_step_5 = (k_p + 1) * r * m
        comp_step_6 = m * (a - 1) * m * (k_p + 1 - m * (a - 1))
        log_check = -(a * m - k_p) * log2(q) + self._rank_check_cost(m, n, k_p)
        # Keep the q^r repetitions in logarithmic scale to avoid overflow.
        log_last_vector = self._log2_sum(log2(comp_step_5 + comp_step_6), log_check)
        return self._log2_sum(log2(comp_step_2 + comp_step_3), r * log2(q) + log_last_vector)

    def _improved_kernel_search(self, q, m, n, k, r):
        """Return the improved kernel-search cost, falling back to the original for a = 1."""
        if k <= 0 or n <= r:
            return 0
        a = ceil(k / m)
        if a == 1:
            return self._kernel_search(q, m, n, k, r)
        cpsi = self._process_guess_improved_cost(q, m, n, k, r, a)
        return (a - 1) * r * log2(q) + cpsi

    def _are_parameters_invalid(self, parameters):
        """Reject guesses that leave no instance for the internal solver."""
        return self._are_hybrid_parameters_invalid(parameters['a'], parameters['lv'])

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.time_complexity()
            149.1876655994923
        """
        if self._are_parameters_invalid(parameters):
            return inf
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._improved_kernel_search(q, m, n_reduced, k_reduced, r)
        reduction_cost = self.hybrid_reduction_cost(a, lv)
        time += self._log2_sum(time_complexity, reduction_cost)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.memory_complexity()
            16.11756193939414
        """
        q, m, n, k, r = self.problem.get_parameters()
        memory_store_matrices = log2((k + 1) * m * n)
        memory_linear_system = log2(k ** 2)
        memory = max(memory_store_matrices, memory_linear_system)
        return memory

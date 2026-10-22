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
from math import log2, ceil
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
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
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

    def _ks_time_complexity_helper_(self, q: int, m: int, n_reduced: int, k_reduced: int, r: int):
        """Return the kernel-search cost in logarithmic field operations.

        Sections 4.3 and 4.4 of [ABCPSV]_ include the expected rank-check cost
        for each guess. The improved version reuses the elimination of the first
        ``ceil(k_reduced / m) - 1`` kernel vectors while enumerating the last one.
        """
        if k_reduced <= 0 or n_reduced <= r:
            return 0

        w = self._w
        a = (k_reduced + m - 1) // m
        log_q = log2(q)
        rank_check = k_reduced * m * n_reduced + max(m, n_reduced) * min(m, n_reduced) ** (w - 1)
        expected_check = 2 ** (-(a * m - k_reduced) * log_q) * rank_check

        if a == 1:
            # Original kernel search: construct and solve the full linear system.
            build_system = a * (k_reduced + 1) * r * m
            elimination = max(a * m, k_reduced + 1) * min(a * m, k_reduced + 1) ** (w - 1)
            return a * r * log_q + log2(build_system + elimination + expected_check)

        # Improved kernel search: prepare a - 1 vectors, then enumerate the last.
        initial_cost = (a - 1) * (k_reduced + 1) * r * m
        initial_cost += (k_reduced + 1) * ((a - 1) * m) ** (w - 1)
        last_vector_cost = (k_reduced + 1) * r * m
        last_vector_cost += m * (a - 1) * m * (k_reduced + 1 - m * (a - 1))
        last_vector_cost += expected_check

        # Sum in logarithmic scale to avoid constructing q ** r.
        initial_time = log2(initial_cost)
        last_vector_time = r * log_q + log2(last_vector_cost)
        processing_time = max(initial_time, last_vector_time)
        processing_time += log2(1 + 2 ** (-abs(initial_time - last_vector_time)))
        return (a - 1) * r * log_q + processing_time

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.time_complexity()
            149.18766136573913
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ks_time_complexity_helper_(q, m, n_reduced, k_reduced, r)
        reduction_cost = self.cost_reduction(a, lv)
        time += max(time_complexity, reduction_cost)
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

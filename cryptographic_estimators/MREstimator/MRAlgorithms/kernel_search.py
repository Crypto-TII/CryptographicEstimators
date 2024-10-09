# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************

from ...MREstimator.mr_algorithm import MRAlgorithm
from ...MREstimator.mr_problem import MRProblem
from ...base_algorithm import optimal_parameter
from math import log2, ceil
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS


class KernelSearch(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of KernelSearch estimator.

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
        self.set_parameter_ranges('lv', 0, r)
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

    def _ks_time_complexity_helper_(self, q, m, k, r):
        time = 0
        w = self._w
        if k > 0:
            a = ceil(k / m)
            time = (a * r) * log2(q) + w * log2(k)
        return time

    def _ks_memory_complexity_helper_(self, m, n, k):
        memory = 0
        if k > 0:
            memory = max(1, 2 * k * m * n)
            memory = log2(memory)

        return memory

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> KS.time_complexity()
            147.72067178682556
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ks_time_complexity_helper_(q, m, k_reduced, r)
        reduction_cost = self.cost_reduction(a)
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
            14.273212809854334
        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory = self._ks_memory_complexity_helper_(m, n_reduced, k_reduced)
        return memory

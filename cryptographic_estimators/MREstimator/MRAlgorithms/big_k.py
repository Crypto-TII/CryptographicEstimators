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


class BigK(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of BigK estimator.

        Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
                w (int): Linear algebra constant (default: 3).
                theta (int): Exponent of the conversion factor (default: 2).

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> E = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> E
            BigK estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """

        super(BigK, self).__init__(problem, **kwargs)
        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m) - 1))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self._name = "BigK"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. number of vectors to guess in the kernel of the low-rank matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> BK.a()
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BK.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """Return the optimal `lv`, i.e. number of entries to guess in the solution.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> BK.lv()
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BK.lv()
            3
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _bk_time_complexity_helper_(self, q: int, m: int, n_reduced: int, k_reduced: int, r: int):
        time = 0
        w = self._w
        if k_reduced > 0 and n_reduced > r:
            time = max(log2(q) * (max(0, m * (n_reduced - r) - k_reduced + 1)) + w * log2((m * (n_reduced - r))), 0)
        return time

    def _bk_memory_complexity_helper_(self, m: int, n_reduced: int, r: int):
        memory = 0
        if n_reduced > r:
            memory = max((m * (n_reduced - r)) ** 2, 1)
            memory = log2(memory)
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BK.time_complexity()
            154.68645607148764
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._bk_time_complexity_helper_(q, m, n_reduced, k_reduced, r)
        reduction_cost = self.cost_reduction(a, lv)
        time += max(time_complexity, reduction_cost)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BK.memory_complexity()
            16.11756193939414
        """
        q, m, n, k, r = self.problem.get_parameters()
        memory_store_matrices = log2((k + 1) * m * n)
        memory_attack = log2(k ** 2)
        memory = max(memory_store_matrices, memory_attack)
        return memory

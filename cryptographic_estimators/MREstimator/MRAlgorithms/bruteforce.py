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


class BruteForce(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of BruteForce estimator.

        Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
                w (int): Linear algebra constant (default: 3).
                theta (int): Exponent of the conversion factor (default: 2).

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> E = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> E
            BruteForce estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """

        super(BruteForce, self).__init__(problem, **kwargs)

        _, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self._name = "BruteForce"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> BFE.a()
            1

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BFE.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """Return the optimal `lv`, i.e. number of entries to guess in the solution.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> BFE.lv()
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BFE.lv()
            0
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _BFE_time_complexity_helper_(self, q: int, n: int, k_reduced: int, r: int):
        time = 0
        w = self._w
        if k_reduced > 0 and n > r:
            time = k_reduced * log2(q) + w * log2(r)
        return time

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BFE.time_complexity()
            143.75488750216346
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, _, n, _, r = self.problem.get_parameters()
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._BFE_time_complexity_helper_(q, n, k_reduced, r)
        reduction_cost = self.cost_reduction(a, lv)
        time += max(time_complexity, reduction_cost)
        if abs(time_complexity - reduction_cost) < 0:
            time += 1
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> BFE.memory_complexity()
            16.11756193939414
        """
        q, m, n, k, _ = self.problem.get_parameters()
        memory = log2((k + 1) * m * n)
        return memory

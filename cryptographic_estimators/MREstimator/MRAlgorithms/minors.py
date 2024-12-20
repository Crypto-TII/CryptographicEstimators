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
from math import comb as binomial
from ..mr_helper import minors_polynomial_degree
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS

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

        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
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
            2

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
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.lv()
            0
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _ME_time_memory_complexity_helper_(self, m: int, n_reduced: int, k_reduced: int, r: int, time_mem: str):
        out = 0
        if k_reduced > 0 and n_reduced > r:
            D = minors_polynomial_degree(m, n_reduced, k_reduced, r) + 1
            if time_mem == "time":
                w = self._w
                out = w * log2(binomial(k_reduced + D, D))
            elif time_mem == "memory":
                out = 2 * log2(binomial(k_reduced + D, D))
        return out

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.time_complexity()
            144.72067178682556
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ME_time_memory_complexity_helper_(m, n_reduced, k_reduced, r, "time")
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
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> ME.memory_complexity()
            16.11756193939414
        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory_attack = self._ME_time_memory_complexity_helper_(m, n_reduced, k_reduced, r, "memory")
        memory_store_matrices = log2((k + 1) * m * n)
        memory = max(memory_attack, memory_store_matrices)
        return memory

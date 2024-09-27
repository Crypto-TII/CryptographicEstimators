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
    r"""
    Construct an instance of BigK estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 3)
    - ``theta`` -- exponent of the conversion factor (default: 2)


    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
        sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
        sage: E = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
        sage: E
        BigK estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
    """

    def __init__(self, problem: MRProblem, **kwargs):
        super(BigK, self).__init__(problem, **kwargs)
        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m) - 1))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self._name = "BigK"

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: BK.a()
            0

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BK.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: BK.lv()
            0

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BK.lv()
            3
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _bk_time_complexity_helper_(self, q, m, n, k, r):
        time = 0
        if k > 0:
            time = max(log2(q) * (max(0, m * (n - r) - k + 1))  +   self._w * log2((m * (n - r))), 0)
        return time

    def _bk_memory_complexity_helper_(self, m, n, r):
        memory = max((m * (n - r)) ** 2, 1)
        memory = log2(memory)
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters


        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BK.time_complexity()
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
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.big_k import BigK
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BK = BigK(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BK.memory_complexity()
            13.813781191217037

        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, _, _ = self.get_problem_parameters_reduced(a, lv)
        memory = self._bk_memory_complexity_helper_(m, n_reduced, r)
        return memory

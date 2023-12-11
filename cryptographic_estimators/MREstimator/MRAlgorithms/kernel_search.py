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
from ..mr_constants import *


class KernelSearch(MRAlgorithm):
    r"""
    Construct an instance of KernelSearch estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 3)
    - ``theta`` -- exponent of the conversion factor (default: 2.81)

    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
        sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
        sage: E = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
        sage: E
        KernelSearch estimator for the MinRank problem with (q, m, n, k, r) = (7,9,10,15,4)

    """

    def __init__(self, problem: MRProblem, **kwargs):

        super(KernelSearch, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
        self.set_parameter_ranges('lv', 0, r)
        self._name = "KernelSearch"

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: KS = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: KS.a()
            1
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: KS = KernelSearch(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: KS.lv()
            0
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
        memory=0
        if k>0:
           memory = max(1, 2 * k * m * n)
           memory = log2(memory)

        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: KS.lv()
            3
            sage: KS.a()
            4
            sage: KS.time_complexity(a=4, lv=4)
            151.4220647661728
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ks_time_complexity_helper_(q, m, k_reduced, r)
        reduction_cost = self.cost_reduction(a)
        time += max(time_complexity, reduction_cost)
        if abs(time_complexity - reduction_cost) < 0:
            time += 1
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.kernel_search import KernelSearch
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: KS = KernelSearch(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: KS.memory_complexity(a=4, lv=4)
            14.17367713630342

        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory = self._ks_memory_complexity_helper_(m, n_reduced, k_reduced)
        return memory

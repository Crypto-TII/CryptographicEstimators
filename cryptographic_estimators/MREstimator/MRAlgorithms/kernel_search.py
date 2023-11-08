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
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- exponent of the conversion factor (default: 2.81)
    """

    def __init__(self, problem: MRProblem, **kwargs):
        self._name = "kernel_search"
        super(KernelSearch, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min (n - r, ceil(k / m)))
        self.set_parameter_ranges('lv', 0, r)

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
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _sm_time_complexity_helper_(self, q, m, K, r):

        a = ceil(K / m)
        main_factor = q ** (a * r)
        second_factor = max(1, K ** self._w)
        time = main_factor * second_factor
        time = log2(time)
        return time

    def _sm_memory_complexity_helper_(self, m, n, K):
        memory = max(1, 2 * K * m * n)
        memory = log2(memory)
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]

        q, m, n, k, r = self.problem.get_parameters()

        time = ((a * r)+lv)*log2(q)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            time += self._sm_time_complexity_helper_(q, m, k_hybrid, r)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        k_hybrid = k - a * m - lv
        memory = 0
        if k_hybrid > 0:
            memory = self._sm_memory_complexity_helper_(m, n - a, k_hybrid)
        return memory

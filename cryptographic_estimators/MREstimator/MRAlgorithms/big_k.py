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


class BigK(MRAlgorithm):
    r"""
    Construct an instance of BigK estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- exponent of the conversion factor (default: 2.81)
    """

    def __init__(self, problem: MRProblem, **kwargs):
        self._name = "big_k"
        super(BigK, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)) - 1)
        self.set_parameter_ranges('lv', 0, r - 1)

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
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _sm_time_complexity_helper_(self, q, m, n, K, r):
        time = 0
        if K > 0:
            time = max(q ** (max(0, m * (n - r) - K + 1)) * (m * (n - r)) ** self._w, 1)
            time = log2(time)
        return time

    def _sm_memory_complexity_helper_(self, m, n, r):
        memory = max((m * (n - r)) ** 2, 1)
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

        time = self.hybridization_factor(a, lv)
        k_hybrid = k - a * m - lv
        time += log2(2 ** self._sm_time_complexity_helper_(q, m, n - a, k_hybrid, r) + min(k, (a * m)) ** self._w)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        memory = self._sm_memory_complexity_helper_(m, n - a, r)
        return memory

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
from .mr_helper import minors_polynomial
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS


class Minors(MRAlgorithm):
    r"""
    Construct an instance of Minors estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 3)
    - ``theta`` -- exponent of the conversion factor (default: 2.81)

    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
        sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
        sage: E = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
        sage: E
        Minors estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
    """

    def __init__(self, problem: MRProblem, **kwargs):

        super(Minors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
        self.set_parameter_ranges('lv', 0, r)
        self._name = "Minors"

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: ME.a()
            2

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: ME.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: ME.lv()
            0

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: ME.lv()
            0
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _ME_time_complexity_helper_(self, m, n_reduced, k_reduced, r):
        time = 0
        poly = minors_polynomial(m, n_reduced, k_reduced, r)
        D = poly.degree()
        w = self._w
        if k_reduced > 0:
            time = w * log2(binomial(k_reduced + D, D))
        return time

    def _ME_memory_complexity_helper_(self, m, n_reduced, k_reduced, r):
        memory = 0
        poly = minors_polynomial(m, n_reduced, k_reduced, r)
        D = poly.degree()
        if k_reduced > 0:
            memory = 2 * log2(binomial(k_reduced + D, D))
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: ME.time_complexity()
            143.1769522683363
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._ME_time_complexity_helper_(m, n_reduced, k_reduced, r)
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

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.minors import Minors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: ME = Minors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: ME.memory_complexity()
            14.784634845557521
        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, n, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory = self._ME_memory_complexity_helper_(m, n_reduced, k_reduced, r)
        return memory

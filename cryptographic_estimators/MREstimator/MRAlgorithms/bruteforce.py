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
from ..mr_helper import minors_polynomial
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, MR_NUMBER_OF_COEFFICIENTS_TO_GUESS


class BruteForce(MRAlgorithm):
    """
    Construct an instance of BruteForce estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 3)
    - ``theta`` -- exponent of the conversion factor (default: 2)

    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
        sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
        sage: E = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
        sage: E
        BruteForce estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)

    """

    def __init__(self, problem: MRProblem, **kwargs):

        super(BruteForce, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m)))
        self.set_parameter_ranges('lv', 0, r)
        self._name = "BruteForce"

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: BFE.a()
            1

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BFE.a()
            5

        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: BFE.lv()
            0

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BFE.lv()
            0

        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    def _BFE_time_complexity_helper_(self, q: int, k_reduced: int, r: int):
        time = 0
        w = self._w
        if k_reduced > 0:
            time = k_reduced * log2(q)  +  w * log2(r)
        return time

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BFE.time_complexity()
            143.75488750216346

        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        q, m, _, k, r = self.problem.get_parameters()
        _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        time = self.hybridization_factor(a, lv)
        time_complexity = self._BFE_time_complexity_helper_(q, k_reduced, r)
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

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.bruteforce import BruteForce
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: BFE = BruteForce(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: BFE.memory_complexity()
            16.11756193939414

        """

        q, m, n, k, r = self.problem.get_parameters()
        memory = log2(k + 1) +  log2(m * n)
        return memory

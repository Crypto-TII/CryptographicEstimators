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

from cryptographic_estimators.MREstimator.minrank_algorithm import MRAlgorithm
from cryptographic_estimators.MREstimator.minrank_problem import MRProblem
from math import log2, inf, ceil
from sage.function.other import binomial
from .mr_constants import *
from .mr_helper import _strassen_complexity_, _bw_complexity_




class SupportMinors(MRAgorithm):
    r"""
    Construct an instance of SupportMinors estimator

    Add reference to corresponding paper here.

    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    """

    def __init__(self, problem: MRProblem, **kwargs):
        self._name = "support_minors"
        super(Support_Minors, self).__init__(problem, **kwargs)

        _, m, n, k, _ = self.problem.get_problem_parameters()
        self.set_parameter_ranges('a', 0, ceil(k/m))
        self.set_parameter_ranges('lv', 0, k)
        self.set_parameter_ranges('b', 1, n)
        self.set_parameter_ranges('nprime', 1, n)

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        """
        return self._get_optimal_parameter('a')

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        """
        return self._get_optimal_parameter('lv')

    @optimal_parameter
    def b(self):
        """
        Return the optimal `b`, i.e. the degree of the linear variables in the Macaulay matrix

        """
        return self._get_optimal_parameter('b')

    @optimal_parameter
    def nprime(self):
        """
        Return the optimal `nprime`, i.e. the number of columns to be selected

        """
        return self._get_optimal_parameter('nprime')

    @optimal_parameter
    def variant(self):
        """
        Return the optimal `variant`

        """
        return self._get_optimal_parameter('nprime')


    def _expected_dimension_of_support_minors_equations(self,q, m, n, K, r, b):
        """
        Return the expected number of linearly independent support minors equations

        """
        if q == 2:
            temp = 0
            for j in range(1, b + 1):
                temp += sum([(-1) ** (i + 1) * binomial(n, r + i) * binomial(m + i - 1, i) * binomial(K, j - i) for i in
                             range(1, j + 1)])
        else:
            temp = sum(
                [(-1) ** (i + 1) * binomial(n, r + i) * binomial(m + i - 1, i) * binomial(K + b - i - 1, b - i) for i in
                 range(1, b + 1)])
        return temp


    def _dimension(self,q, n, K, r, b):
        """
        Dimension of the smallest vector space spanned by monomials containing the support minors equations
        """
        if q == 2:
            temp = binomial(n, r) * sum([binomial(K, j) for j in range(1, b + 1)])
        else:
            temp = binomial(n, r) * binomial(K + b - 1, b)
        return temp


    def _are_parameters_invalid(self, parameters: dict):
        """
        Specifies constraints on the parameters
        """
        a = parameters["a"]
        lv = parameters["lv"]
        b = parameters["b"]
        nprime = parameters["nprime"]
        q, m, _, k_reduced, r =  self.get_problem_parameters_reduced(a, lv)
        dim = self._dimension(q, nprime, k_reduced +  1, r, b) - 1
        exp = self._expected_dimension_of_support_minors_equations(q, m, nprime, k_reduced + 1, r, b)
        return dim < exp


    def _sm_time_complexity_helper_(self, q, K, r, nprime, b, variant):
        if variant == MR_BLOCK_WIEDEMANN:
            time = _bw_complexity_(row_density=K * (r + 1), ncols=self._dimension(q, nprime, K, r, b))

        else:
            time = _strassen_complexity_(rank=self._dimension(q, nprime, K, r, b) - 1,
                                                            ncols=self.dimension(q, nprime, K, r, b))
        return time

    def _sm_memory_complexity_helper_(self, q, K, r, nprime, b, variant):
        ncols = self._dimension(q, nprime, K, r, b)
        if variant == MR_BLOCK_WIEDEMANN:
            memory = log2(log2(q)) + log2(2 * ncols)

        else:
            memory = 2 * log2(ncols)
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]
        variant = parameters[MR_VARIANT]
        q, m, n, k, r = self.get_parameters()
        time = _strassen_complexity_(m, n)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            time = _sm_time_complexity_helper_(q=q, K=k_hybrid + 1, r=r, nprime=nprime, b=b, variant=variant)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]
        variant = parameters[MR_VARIANT]

        q, m, n, k, r = self.get_parameters()

        memory = log2(log2(q)) +  log2(m * n) +  log2(k)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            memory = _sm_memory_complexity_helper_(q=q, K=k_hybrid + 1, r=r, nprime=nprime, b=b, variant=variant)
        return memory


    
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
from math import log2, inf, ceil
from sage.arith.misc import binomial
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, \
    MR_NUMBER_OF_COEFFICIENTS_TO_GUESS, \
    MR_REDUCED_NUMBER_OF_COLUMNS, \
    MR_LINEAR_VARIABLES_DEGREE, MR_VARIANT
from ...MREstimator.mr_helper import Variant, _strassen_complexity_, _bw_complexity_


class SupportMinors(MRAlgorithm):
    r"""
    Construct an instance of SupportMinors estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 3)
    - ``theta`` -- exponent of the conversion factor (default: 2)

    EXAMPLES::

        sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
        sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
        sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
        sage: SM
        SupportMinors estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
    """

    def __init__(self, problem: MRProblem, **kwargs):

        super(SupportMinors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m) - 1))
        self.set_parameter_ranges('lv', 0, r - 1)
        self.set_parameter_ranges('b', 1, r + 1)
        self.set_parameter_ranges('nprime', r + 1, n)
        self.set_parameter_ranges('variant', 1, 2)
        self._name = "SupportMinors"

    @optimal_parameter
    def a(self):
        """
        Return the optimal `a`, i.e. no. of vectors to guess in the kernel of the low-rank matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: SM.a()
            1

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """
        Return the optimal `lv`, i.e. no. of entries to guess in the solution

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: SM.lv()
            0

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.lv()
            0

        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    @optimal_parameter
    def b(self):
        """
        Return the optimal `b`, i.e. the degree of the linear variables in the Macaulay matrix

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: SM.b()
            1

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.b()
            1
        """
        return self._get_optimal_parameter(MR_LINEAR_VARIABLES_DEGREE)

    @optimal_parameter
    def nprime(self):
        """
        Return the optimal `nprime`, i.e. the number of columns to be selected

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: SM.nprime()
            8

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.nprime()
            8
        """
        return self._get_optimal_parameter(MR_REDUCED_NUMBER_OF_COLUMNS)

    @optimal_parameter
    def variant(self):
        """
        Return the optimal `variant`,i.e, either 1 ('strassen')  or 2 ('block_wiedemann').

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=9, k=20, r=4))
            sage: SM.variant()
            'block_wiedemann'

        Tests::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.variant()
            'block_wiedemann'

        """
        optimal_variant = self._get_optimal_parameter(MR_VARIANT)
        if optimal_variant is not None:
            return Variant(self._get_optimal_parameter(MR_VARIANT)).name
        return None

    def _expected_dimension_of_support_minors_equations(self, q, m, n, K, r, b):
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

    def _dimension(self, q, n, K, r, b):
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
        q, m, n_reduced, k_reduced, r = self.get_problem_parameters_reduced(a, lv)
        if nprime < r + b or nprime > n_reduced:
            return True
        dim = self._dimension(q, nprime, k_reduced + 1, r, b) - 1
        exp = self._expected_dimension_of_support_minors_equations(q, m, nprime, k_reduced + 1, r, b)
        return dim >= exp

    def _sm_time_complexity_helper_(self, q, K, r, nprime, b, variant):
        if variant == Variant.block_wiedemann.value:
            time = _bw_complexity_(row_density=K * (r + 1), ncols=self._dimension(q, nprime, K, r, b))

        else:
            time = _strassen_complexity_(rank=self._dimension(q, nprime, K, r, b) - 1,
                                         ncols=self._dimension(q, nprime, K, r, b))
        return time

    def _sm_memory_complexity_helper_(self, q, K, r, nprime, b, variant):
        ncols = self._dimension(q, nprime, K, r, b)
        if variant == Variant.block_wiedemann.value:
            memory = log2(log2(q)) + log2(2 * ncols)

        else:
            memory = 2 * log2(ncols)
        return memory

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters


        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.time_complexity()
            144.00702726689397

            sage: SM = SupportMinors(MRProblem(q=2, m=10, n=10, k=70, r=4))
            sage: SM.time_complexity()
            inf
        """
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]
        variant = parameters[MR_VARIANT]

        q, m, n, k, r = self.problem.get_parameters()
        time = self.hybridization_factor(a, lv)
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        reduction_cost = self.cost_reduction(a, lv)
        if k_reduced > 0:
            time_complexity = self._sm_time_complexity_helper_(q=q, K=k_reduced + 1, r=r, nprime=nprime, b=b, variant=variant)
            time += max(time_complexity, reduction_cost)
        else:
            time += _strassen_complexity_(m, n)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            sage: SM.memory_complexity()
            11.807354922057604
        """

        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]
        variant = parameters[MR_VARIANT]

        q, m, n, k, r = self.problem.get_parameters()

        memory = log2(log2(q)) + log2(m * n) + log2(k)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            memory = self._sm_memory_complexity_helper_(q=q, K=k_hybrid + 1, r=r, nprime=nprime, b=b, variant=variant)
        return memory

    def get_optimal_parameters_dict(self):
        """
        Returns the optimal parameters dictionary

        """

        if self._optimal_parameters != {}:
            self._optimal_parameters['variant'] = Variant(self._optimal_parameters['variant']).name
        return self._optimal_parameters

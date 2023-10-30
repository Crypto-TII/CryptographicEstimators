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
from ..mr_constants import *
from ..mr_helper import _strassen_complexity_, _bw_complexity_


class SupportMinors(MRAlgorithm):
    r"""
    Construct an instance of SupportMinors estimator


    INPUT:

    - ``problem`` -- an instance of the MRProblem class
    - ``w`` -- linear algebra constant (default: 2)
    - ``theta`` -- exponent of the conversion factor (default: 2.81)
    """

    def __init__(self, problem: MRProblem, **kwargs):
        self._name = "support_minors"
        super(SupportMinors, self).__init__(problem, **kwargs)

        _, m, n, k, _ = self.problem.get_problem_parameters()
        self.set_parameter_ranges('a', 0, ceil(k/m))
        self.set_parameter_ranges('lv', 0, k)
        self.set_parameter_ranges('b', 1, n)
        self.set_parameter_ranges('nprime', 1, n)

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
            4
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
            4
        """
        return self._get_optimal_parameter(MR_REDUCED_NUMBER_OF_COLUMNS)

    @optimal_parameter
    def variant(self):
        """
        Return the optimal `variant`

        EXAMPLES::

            sage: from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            sage: SM.nprime()
            'strassen'
        """
        return self._get_optimal_parameter(MR_VARIANT)


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

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters based on the `_parameter_ranges` and already
        set parameters in `_optimal_parameters`

        """
        new_ranges = self._fix_ranges_for_already_set_parameters()
        _ = new_ranges.pop(MR_VARIANT)
        indices = {i: new_ranges[i]["min"] for i in new_ranges}
        variant = MR_STRASSEN
        keys = [i for i in indices]
        stop = False
        while not stop:
            if not self._are_parameters_invalid(indices):
                aux = indices.copy()
                aux.update({MR_VARIANT: variant})
                yield aux
            indices[next(iter(indices))] += 1
            for i in range(len(keys)):
                if indices[keys[i]] > new_ranges[keys[i]]["max"]:
                    indices[keys[i]] = new_ranges[keys[i]]["min"]
                    if i != len(keys) - 1:
                        indices[keys[i + 1]] += 1
                    elif i == len(keys) - 1 and MR_VARIANT == MR_STRASSEN:
                        variant = MR_BLOCK_WIEDEMANN
                        indices = {i: new_ranges[i]["min"] for i in new_ranges}
                    else:
                        stop = True
                else:
                    break

    def _sm_time_complexity_helper_(self, q, K, r, nprime, b, variant):
        if variant == MR_BLOCK_WIEDEMANN:
            time = _bw_complexity_(row_density=K * (r + 1), ncols=self._dimension(q, nprime, K, r, b))

        else:
            time = _strassen_complexity_(rank=self._dimension(q, nprime, K, r, b) - 1,
                                                            ncols=self._dimension(q, nprime, K, r, b))
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
        q, m, n, k, r = self.problem.get_problem_parameters()
        time = _strassen_complexity_(m, n)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            time = self._sm_time_complexity_helper_(q=q, K=k_hybrid + 1, r=r, nprime=nprime, b=b, variant=variant)
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

        q, m, n, k, r = self.problem.get_problem_parameters()

        memory = log2(log2(q)) +  log2(m * n) +  log2(k)
        k_hybrid = k - a * m - lv
        if k_hybrid > 0:
            memory = self._sm_memory_complexity_helper_(q=q, K=k_hybrid + 1, r=r, nprime=nprime, b=b, variant=variant)
        return memory


    
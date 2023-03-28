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


from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.mq_helper import sum_of_binomial_coefficients
from ...base_algorithm import optimal_parameter
from math import log2
from sage.rings.infinity import Infinity
from sage.functions.other import floor


class DinurSecond(MQAlgorithm):
    """
    Construct an instance of Dinur's second estimator

    Dinur's second is a probabilistic algorithm to solve the MQ problem over GF(2) [Din21b]_. It is based on ideas from
    [Din21a]_.

    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = DinurSecond(MQProblem(n=10, m=12, q=2))
        sage: E
        Dinur2 estimator for the MQ problem with 10 variables and 12 polynomials

    """

    def __init__(self, problem: MQProblem, **kwargs):
        if problem.order_of_the_field() != 2:
            raise TypeError("q must be equal to 2")
        super().__init__(problem, **kwargs)

        self._name = "Dinur2"
        self._k = floor(log2(2 ** self.problem.nsolutions + 1))
        n, m, _ = self.get_reduced_parameters()
        self.set_parameter_ranges('n1', 1, n// 2 - 1)

    @optimal_parameter
    def n1(self):
        """
        Return the optimal parameter $n_1$

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2))
            sage: E.n1()
            4
        """
        return self._get_optimal_parameter('n1')

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.time_complexity(n1=4)
            15.809629225117881

            sage: E.time_complexity(n1=2, bit_complexities=False)
            15.844709299018824

            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.time_complexity()
            15.809629225117881

        """
        n1 = parameters['n1']
        n = self.nvariables_reduced()
        time = 16 * log2(n) * 2 ** n1 * sum_of_binomial_coefficients(n - n1, n1 + 3) + \
            n1 * n * 2 ** (n - n1) + 2 ** (n - 2 * n1 + 1) * \
            sum_of_binomial_coefficients(n, 2)
        h = self._h
        return h + log2(time)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.memory_complexity(n1=4)
            11.321928094887362

            sage: E.memory_complexity(n1=2)
            12.35974956032233

            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2))
            sage: E.memory_complexity()
            11.321928094887362

        """
        n = self.nvariables_reduced()
        n1 = parameters['n1']
        return log2(8 * (n1 + 1) * sum_of_binomial_coefficients(n - n1, n1 + 3))

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Compute and return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.time_complexity(n1=2)
            8.148148148148149
        """
        n = self.nvariables_reduced()
        h = self._h
        return h + ((1 - 1./(2.7*2)) * n)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Compute and return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.memory_complexity(n1=2)
            6.3
        """
        n = self.nvariables_reduced()
        return n * 0.63

    def _find_optimal_tilde_o_parameters(self):
        """
        Return the Ō time complexity of Bjorklund et al.'s algorithm

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur2 import DinurSecond
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurSecond(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.optimal_parameters()
            {'n1': 1.8518518518518516}
        """
        n = self.nvariables_reduced()
        self._optimal_parameters['n1'] = n/(2.7 * 2)

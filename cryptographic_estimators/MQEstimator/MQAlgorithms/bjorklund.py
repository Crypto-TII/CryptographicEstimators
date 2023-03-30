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
from sage.functions.other import floor, ceil


class Bjorklund(MQAlgorithm):
    r"""
    Construct an instance of Bjorklund et al.'s estimator

    Bjorklund et al.'s is a probabilistic algorithm to solve the MQ problem of GF(2) [BKW19]_. It finds a solution of a qudractic
    system by computing the parity of it number of solutions.

    INPUT:

    - ``problem`` --MQProblem object including all necessary parameters
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = Bjorklund(MQProblem(n=10, m=12, q=2))
        sage: E
        Björklund et al. estimator for the MQ problem with 10 variables and 12 polynomials

    """

    def __init__(self, problem: MQProblem, **kwargs):
        if problem.order_of_the_field() != 2:
            raise TypeError("q must be equal to 2")
        super().__init__(problem, **kwargs)
        self._name = "Björklund et al."
        self._k = floor(log2(2 ** self.problem.nsolutions + 1))
        n, m, _ = self.get_reduced_parameters()

        self.set_parameter_ranges('lambda_', 3 / n, min(m, n - 1)/n)

    @optimal_parameter
    def lambda_(self):
        """
        Return the optimal lambda_

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2))
            sage: E.lambda_()
            3/10
        """
        return self._get_optimal_parameter('lambda_')

    def _valid_choices(self):
        n, _, _ = self.get_reduced_parameters()
        ranges = self._parameter_ranges
        l_min = max(3, ceil(ranges['lambda_']['min'] * n))
        l_max = min(ceil(ranges['lambda_']['max'] * n), n)
        l = l_min
        stop = False
        while not stop:
            temp_lambda = l / n
            yield {'lambda_': temp_lambda}
            l += 1
            if l > l_max:
                stop = True

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.time_complexity(lambda_=7/10)
            49.97565549640329
        """
        lambda_ = parameters['lambda_']
        n, m, _ = self.get_reduced_parameters()
        k = self._k
        h = self._h
        time = 8 * k * log2(n) * sum([Bjorklund._internal_time_complexity_(
            n - i, m + k + 2, lambda_) for i in range(1, n)])
        return h + log2(time)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.memory_complexity(lambda_=7/10)
            10.225233514599497
        """
        lambda_ = parameters['lambda_']

        def _internal_memory_complexity_(_n, _m, _lambda):
            if _n <= 1:
                return 0
            else:
                s = 48 * _n + 1
                l = floor(_lambda * _n)
                return _internal_memory_complexity_(l, l + 2, _lambda) + 2 ** (_n - l) * log2(s) + _m * sum_of_binomial_coefficients(_n, 2)

        n, m, _ = self.get_reduced_parameters()
        return log2(_internal_memory_complexity_(n, m, lambda_))

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of Bjorklund et al.'s algorithm

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.time_complexity(lambda_=7/10)
            8.03225
        """
        n = self.nvariables_reduced()
        h = self._h
        return h + 0.803225 * n

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of Bjorklund et al.'s algorithm

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.memory_complexity(lambda_=7/10)
            3
        """
        n = self.nvariables_reduced()
        lambda_ = parameters['lambda_']
        return (1 - lambda_) * n

    def _find_optimal_tilde_o_parameters(self):
        """
        Return the Ō time complexity of Bjorklund et al.'s algorithm

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.bjorklund import Bjorklund
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = Bjorklund(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.optimal_parameters()
            {'lambda_': 0.19677}
        """
        self._optimal_parameters['lambda_'] = 0.19677

    @staticmethod
    def _internal_time_complexity_(n: int, m: int, lambda_: float):
        """
        Helper function. Computes the runtime of the algorithm for given n, m and lambda
        """
        if n <= 1:
            return 1
        else:
            l = floor(lambda_ * n)
            T1 = (n + (l + 2) * m * sum_of_binomial_coefficients(n, 2) +
                  (n - l) * 2 ** (n - l))
            s = 48 * n + 1
            return s * sum_of_binomial_coefficients(n - l, l + 4) * (Bjorklund._internal_time_complexity_(l, l + 2, lambda_) + T1)

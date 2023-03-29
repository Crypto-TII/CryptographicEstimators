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


from ...base_algorithm import optimal_parameter
from ...MQEstimator.mq_helper import sum_of_binomial_coefficients
from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...helper import ComplexityType
from math import log2
from sage.functions.other import floor


class DinurFirst(MQAlgorithm):
    r"""
    Construct an instance of Dinur's first estimator

    The Dinur's first is a probabilistic algorithm to solve the MQ problem over GF(2) [Din21a]_. It computes the parity
    of the number of solutions of many quadratic polynomial systems. These systems come from the specialization, in the
    original system, of the values in a fixed set of variables.


    INPUT:

    - ``problem`` -- MQProblem object including all necessary parameters
    - ``nsolutions`` -- number of solutions (default: 1)
    - ``h`` -- external hybridization parameter (default: 0)

    EXAMPLES::

        sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
        sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        sage: E = DinurFirst(MQProblem(n=10, m=12, q=2))
        sage: E
        Dinur1 estimator for the MQ problem with 10 variables and 12 polynomials
    """

    def __init__(self, problem: MQProblem, **kwargs):
        if problem.order_of_the_field() != 2:
            raise TypeError("q must be equal to 2")
        super().__init__(problem, **kwargs)
        self._name = "Dinur1"
        self._k = floor(log2(2 ** self.problem.nsolutions + 1))
        n, m, _ = self.get_reduced_parameters()
        self.set_parameter_ranges('kappa', 1 / n, 1/3)
        self.set_parameter_ranges('lambda_', 1 / (n - 1), 0.999)

    @optimal_parameter
    def lambda_(self):
        """
        Return the optimal lambda_

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2))
            sage: E.lambda_()
            2/9
        """
        return self._get_optimal_parameter('lambda_')

    @optimal_parameter
    def kappa(self):
        """
        Return the optimal kappa

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2))
            sage: E.kappa()
            1/3
        """
        return self._get_optimal_parameter('kappa')

    def _valid_choices(self):
        """
        Generator which yields on each call a new set of valid parameters for the optimization routine based.

        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        n, m, _ = self.get_reduced_parameters()
        n1_min = max(2, floor(new_ranges['kappa']['min'] * (n - 1)))
        n1_max = min(floor(new_ranges['kappa']
                     ['max'] * (n - 1)), (n - 1) // 3 + 1)
        n1 = n1_min
        n2 = 1
        kappa = n1 / (n - 1)
        lambda_ = (n1 - n2) / (n - 1)
        stop = False
        while not stop:
            yield {'kappa': kappa, 'lambda_': lambda_}
            n2 += 1
            if n2 >= n1:
                n2 = 1
                n1 += 1
                if n1 > n1_max:
                    stop = True

            kappa = n1 / (n - 1)
            lambda_ = (n1 - n2) / (n - 1)

    def _T(self, n: int, n1: int, w: int, lambda_: float):
        t = 48 * n + 1
        n2 = floor(n1 - lambda_ * n)
        l = n2 + 2
        k = self._k
        m = self.npolynomials_reduced()

        if n2 <= 0:
            return n * sum_of_binomial_coefficients(n - n1, w) * 2 ** n1
        else:
            temp1 = self._T(n, n2, n2 + 4, lambda_)
            temp2 = n * \
                sum_of_binomial_coefficients(n - n1, w) * 2 ** (n1 - n2)
            temp3 = n * sum_of_binomial_coefficients(n - n2, n2 + 4)
            temp4 = l * (m + k + 2) * sum_of_binomial_coefficients(n, 2)
            return t * (temp1 + temp2 + temp3 + temp4)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2))
            sage: E.time_complexity(kappa=0.9, lambda_=0.9)
            16.73237302312492

            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.time_complexity()
            26.81991353901186

        """
        lambda_ = parameters['lambda_']
        kappa = parameters['kappa']
        k = self._k
        n = self.nvariables_reduced()

        def w(i, kappa):
            return floor((n - i) * (1 - kappa))

        def n1(i, kappa):
            return floor((n - i) * kappa)

        time = 8 * k * \
            log2(n) * sum([self._T(n - i, n1(i, kappa),
                                   w(i, kappa), lambda_) for i in range(1, n)])
        h = self._h
        return h + log2(time)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.memory_complexity(kappa=0.9, lambda_=0.9)
            8.909893083770042

            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), bit_complexities=False)
            sage: E.memory_complexity()
            14.909893083770042

        """
        kappa = parameters['kappa']
        n = self.nvariables_reduced()
        memory = log2(48 * n + 1) + floor((1 - kappa) * n)
        return memory

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        EXAMPLES::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.time_complexity(kappa=0.9, lambda_=0.9)
            6.9430000000000005

            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.time_complexity()
            6.9430000000000005
        """
        n = self.nvariables_reduced()
        h = self._h
        return h + 0.6943 * n

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        kappa = parameters['kappa']
        n = self.nvariables_reduced()
        memory = (1 - kappa) * n
        return memory

    def _find_optimal_tilde_o_parameters(self):
        """
        Return the Ō time complexity of DinurFirst et al.'s algorithm

        TESTS::

            sage: from cryptographic_estimators.MQEstimator.MQAlgorithms.dinur1 import DinurFirst
            sage: from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            sage: E = DinurFirst(MQProblem(n=10, m=12, q=2), complexity_type=1)
            sage: E.optimal_parameters()
            {'kappa': 0.3057, 'lambda_': 0.3010299956639812}
        """
        n = self.nvariables_reduced()
        lambda_ = 1 / log2(n)
        kappa = 0.3057
        self._optimal_parameters['kappa'] = kappa
        self._optimal_parameters['lambda_'] = lambda_

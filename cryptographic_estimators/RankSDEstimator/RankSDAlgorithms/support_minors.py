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


from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_problem import RankSDProblem
from ...base_algorithm import optimal_parameter
from math import log2
from math import comb as binomial


class SupportMinors(RankSDAlgorithm):
    """
    Construct an instance of SupportMinors estimator

    This algorith is introduced in [BBBGT23].

     Args:
         problem (RankSDAlgorithm): An instance of the RankSDAlgorithm class.
         **kwargs: Additional keyword arguments.
         w (int): Linear algebra constant (default: 3).
         theta (int): Exponent of the conversion factor (default: 2).

    Examples:
         >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
         >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
         >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
         >>> SM
         SupportMinors estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(SupportMinors, self).__init__(problem, **kwargs)
        _, _, _, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('b', 1, r + 1)
        self.set_parameter_ranges('a', 0, k)
        self._name = "SupportMinors"

    @optimal_parameter
    def b(self):
        """Return the optimal `b`, such that Nb>=Mb-1,where Nb is the number rows and Mb is the number of columns.

           Examples:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> SM.b()
                1

           Tests:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> SM.b()
                2
        """
        return self._get_optimal_parameter('b')

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. the number of columns specialized in X.
           Examples:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> SM.a()
                11

           Tests:
                >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
                >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
                >>> SM = SupportMinors(RankSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> SM.a()
                14
        """
        return self._get_optimal_parameter("a")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
              >>> SM.time_complexity()
              155.10223904640839
        """

        a = parameters['a']
        b = parameters['b']

        q, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, 0)
        N, M = self._compute_N_and_M(b, m, n_red, k_red, r)
        w = self._w

        time_complexity = (a * r) * log2(q) + 2 * log2(m) + log2(N) + (w - 1) * log2(M)

        return time_complexity

    def _compute_N_and_M(self, b, m, n, k, r):
        N = 0
        for i in range(1, k + 1):
            N = N + binomial(n - i, r) * binomial(k + b - 1 - i, b - 1)

        N = N - binomial(n - k - 1, r) * binomial(k + b - 1, b)
        N1 = 0
        for i in range(1, b + 1):
            N1 = N1 + (-1) ** (i + 1) * binomial(k + b - i - 1, b - i) * binomial(n - k - 1, r + i)

        N = N - (m - 1) * N1

        M = binomial(k + b - 1, b) * (binomial(n, r) - m * binomial(n - k - 1, r))

        return N, M

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        Args:
              parameters (dict): Dictionary including the parameters.

        Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.support_minors import SupportMinors
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> SM = SupportMinors(RankSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
              >>> SM.memory_complexity()
              35.19384642563464
        """
        a = parameters['a']
        b = parameters['b']

        _, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, 0)
        N, M = self._compute_N_and_M(b, m, n_red, k_red, r)
        memory_complexity = log2(N * M)

        return memory_complexity

    def _are_parameters_invalid(self, parameters: dict):
        """
        Specifies constraints on the parameters
        """

        a = parameters['a']
        b = parameters['b']

        _, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, 0)

        if n_red <= 0 or k_red <= 0 or n_red < k_red or n_red - k_red - 1 < r:
            return True

        N, M = self._compute_N_and_M(b, m, n_red, k_red, r)

        return N < (M - 1) or M < 0 or N < 0

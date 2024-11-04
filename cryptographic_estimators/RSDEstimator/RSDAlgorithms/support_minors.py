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


from ..rsd_algorithm import RSDAlgorithm
from ..rsd_problem import RSDProblem
from ...base_algorithm import optimal_parameter
from math import log2
from math import comb as binomial


class SupportMinors(RSDAlgorithm):
    """
    Construct an instance of SupportMinors estimator

    M. Bardet, P. Briaud, M. Bros, P. Gaborit, and J.-P. Tillich,
    “Revisiting algebraic attacks on MinRank and on the rank decoding problem.

     INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(SupportMinors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('b', 1, r + 1)
        self.set_parameter_ranges('a', 0, k)
        # self.set_parameter_ranges('p', 0, 0)
        self._name = "SupportMinors"

    @optimal_parameter
    def b(self):
        return self._get_optimal_parameter('b')

    @optimal_parameter
    def a(self):
        return self._get_optimal_parameter("a")

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        a = parameters['a']
        b = parameters['b']

        _, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, 0)
        N, M = self._compute_N_and_M(b, m, n_red, k_red, r)
        w = self.w

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

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q, m, n, k, r = self.problem.get_parameters()
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

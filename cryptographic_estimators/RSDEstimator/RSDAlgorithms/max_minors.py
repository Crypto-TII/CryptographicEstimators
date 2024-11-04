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


class MaxMinors(RSDAlgorithm):
    """
    Construct an instance of MaxMinors estimator

    M. Bardet, P. Briaud, M. Bros, P. Gaborit, and J.-P. Tillich,
    “Revisiting algebraic attacks on MinRank and on the rank decoding problem.

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(MaxMinors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, k)
        self.set_parameter_ranges('p', 0, n)
        self._name = "MaxMinors"

    @optimal_parameter
    def a(self):
        return self._get_optimal_parameter("a")

    @optimal_parameter
    def p(self):
        return self._get_optimal_parameter("p")

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        a = parameters['a']
        p = parameters['p']
        _, _, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)
        w = self.w
        bin2 = binomial(n_red, r)
        time_complexity = a * r * log2(q) + w * log2(bin2)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q, m, n, k, r = self.problem.get_parameters()
        a = parameters['a']
        p = parameters['p']
        _, _, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)

        n_rows = m * binomial(n_red - k_red - 1, r)
        n_columns = binomial(n_red, r)
        memory_complexity = log2(n_rows * n_columns)
        return memory_complexity

    def _are_parameters_invalid(self, parameters: dict):
        """
        Specifies constraints on the parameters
        """
        q, m, n, k, r = self.problem.get_parameters()
        a = parameters['a']
        p = parameters['p']
        _, _, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)

        if (n_red - k_red - 1) >= r and n_red >= r:
            bin1 = m * binomial(n_red - k_red - 1, r)
            bin2 = binomial(n_red, r) - 1
            return bin1 < bin2

        return True

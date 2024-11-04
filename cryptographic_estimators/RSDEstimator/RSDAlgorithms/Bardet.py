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


class Bardet(RSDAlgorithm):
    """
    Construct an instance of Bardet estimator

    M. Bardet, P. Briaud, M. Bros, P. Gaborit, V. Neiger, O. Ruatta, and J.P. Tillich,
    “An algebraic attack on rank metric code-based cryptosystems,

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(Bardet, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self._name = "Bardet"

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()

        bin1 = m * binomial(n - k - 1, r)
        bin2 = binomial(n, r)
        w = self.w
        if bin1 < bin2:
            a = r + 1
        else:
            a = r
        time_complexity = self.w * (a * (log2(m + n) + log2(r)) - sum([log2(i) for i in range(1, a + 1)]))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        return 0

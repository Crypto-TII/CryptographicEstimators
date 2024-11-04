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
from math import log2, ceil, floor


class ImprovedGRS(RSDAlgorithm):
    """
    Construct an instance of ImprovedGRS estimator

    N. Aragon, P. Gaborit, A. Hauteville, and J. Tillich,
    “A new algorithm for solving the rank syndrome decoding problem,”

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(ImprovedGRS, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()

        self._name = "ImprovedGRS"

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()

        t1 = self.w * log2((n - k) * m)

        mu1 = r * ceil(((k + 1) * m) / n) - m
        time_complexity = t1 + max(0, mu1 * log2(q))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q, m, n, k, r = self.problem.get_parameters()
        r1 = floor((n - (k + 1) * m / n))
        n_columns = r1 * n
        n_rows = (n - k - 1) * m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

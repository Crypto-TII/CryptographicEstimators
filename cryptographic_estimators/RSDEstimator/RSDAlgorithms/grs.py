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
from math import log2, floor


class GRS(RSDAlgorithm):
    """
    Construct an instance of GRS estimator

    P. Gaborit, O. Ruatta, and J. Schrek, “On the complexity of the rank syndrome decoding problem,”

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        self._name = "GRS"
        super(GRS, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        t1 = self.w * log2(n - k) + self.w * log2(m)
        mu1 = r * floor(k * m / n)
        time_complexity_1 = t1 + mu1 * log2(q)

        return time_complexity_1

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        r_1 = floor((n - k) * m / n)
        n_columns = r_1 * n
        n_rows = (n - k) * m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

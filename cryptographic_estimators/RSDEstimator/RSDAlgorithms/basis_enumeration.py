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


from ..rsd_algorithm import RANKSDAlgorithm
from ..rsd_problem import RANKSDProblem
from math import log2


class BasisEnumeration(RANKSDAlgorithm):
    """
    Construct an instance of RANKSDAlgorithm1 estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the RANKSDProblem class
    """

    def __init__(self, problem: RANKSDProblem, **kwargs):
        self._name = "RANKSDAlgorithm1"
        super(BasisEnumeration, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()

        time_complexity = 3 * log2(n * r + m) + (m - r) * (r - 1) * log2(q)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return 0

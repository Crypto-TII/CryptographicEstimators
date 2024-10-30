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
from math import log2


class BasisEnumeration(RSDAlgorithm):
    """
    Construct an instance of Basis Enumerator estimator
    Florent Chabaud and Jacques Stern.
    The Cryptographic Security of the Syndrome Decoding Problem for Rank Distance Codes. ASIACRYPT ’96
    This algorithm enumerates the possible supports for the vector x.

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        self._name = "BasisEnumeration"
        super(BasisEnumeration, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()

        time_complexity = self.w * log2(n * r + m) + (m - r) * (r - 1) * log2(q)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q, m, n, k, r = self.problem.get_parameters()
        n_rows = (n - k) * m
        n_columns = n * r + m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

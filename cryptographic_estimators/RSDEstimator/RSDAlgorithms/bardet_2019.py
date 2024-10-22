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
from math import comb as binomial
from math import log2


class Bardet2019(RSDAlgorithm):
    """
    Construct an instance of RSDAlgorithm1 estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(Bardet2019, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()

        self._name = "Bardet2019"

    def _bardet_time_complexity_helper_(self, r):
        time = 0
        for i in range(1, r + 1):
            time = time + log2(i)
        return time

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()

        binom_1 = m * binomial(n - k - 1, r)
        binom_2 = binomial(n, r)
        w = 2.807
        if binom_1 < binom_2:
            param = r + 1

        else:
            param = r

        t = self._bardet_time_complexity_helper_(param)
        time_complexity = w * (param * log2((m + n) * r) - t)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return 0

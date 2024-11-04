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
from math import log2, ceil, floor


class GuessingEnhancedGRS(RSDAlgorithm):
    """
    Construct an instance of GuessingEnhancedGRS estimator

    G. D’Alconzo2, A. Esser, A. Gangemi, and C. Sanna,
    “Ryde with mira: Partial key exposure attacks on rank-based schemes,”

    INPUT:

    - ``problem`` -- an instance of the RSDProblem class
    - ``w`` -- linear algebra constant (default: 3)

    EXAMPLES::


    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(GuessingEnhancedGRS, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('t', 0, n * m)
        self._name = "GuessingEnhancedGRS"

    @optimal_parameter
    def t(self):
        return self._get_optimal_parameter("t")

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        t = parameters['t']
        t1 = self.w * log2((n - k) * m + t)

        mu1 = r * ceil(((k + 1) * m - t) / n) - m + t
        time_complexity = t1 + max(0, mu1 * log2(q))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        q, m, n, k, r = self.problem.get_parameters()
        t = parameters['t']
        r_1 = floor(((n - k - 1) * m + t) / n)
        n_columns = r_1 * n
        n_rows = (n - k - 1) * m + t
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

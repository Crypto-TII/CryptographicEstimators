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


from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from math import log2


class RegularISDPerm(RegSDAlgorithm):
    """
    Construct an instance of RegularISD-Perm estimator from [ES23]_

    INPUT:

    - ``problem`` -- an instance of the RegSDProblem class
    """

    def __init__(self, problem: RegSDProblem, **kwargs):
        self._name = "RegularISD-Perm"
        super(RegularISDPerm, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        n, k, w = self.problem.get_parameters()

        # add parity-checks
        k_prime = k - w

        # success pr
        p_iter = log2(1 - k_prime / n) * w

        # cost of one iteration
        T_iter = log2(n - k_prime) * 2

        return T_iter - log2(p_iter)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        n, k, w = self.problem.get_parameters()
        return n - k + w

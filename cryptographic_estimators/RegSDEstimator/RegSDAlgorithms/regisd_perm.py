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
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of RegularISD-Perm estimator from [ES23]_.

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDPerm
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDPerm(RegSDProblem(n=100,k=50,w=10))
            >>> A
            RegularISD-Perm estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(RegularISDPerm, self).__init__(problem, **kwargs)

        self._name = "RegularISD-Perm"
    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()

        # add parity-checks
        k_prime = k - w

        # success pr
        p_iter = log2(1 - k_prime / n) * w

        # cost of one iteration
        T_iter = log2(n - k_prime) * 2

        return T_iter - p_iter

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()
        return log2(n - k + w)

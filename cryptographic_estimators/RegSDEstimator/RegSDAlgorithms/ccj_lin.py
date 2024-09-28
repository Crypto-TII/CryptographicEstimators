# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************

from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from math import log2


class CCJLin(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of CCJ-Linearization estimator from [CCJ23]_.

        (concrete formulas taken from [ES23]_)

        Args:
            problem: An instance of the RegSDProblem class

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import CCJLin
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = CCJLin(RegSDProblem(n=100,k=50,w=10))
            >>> A
            CCJ-Linearization estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(CCJLin, self).__init__(problem, **kwargs)
        n, k, w = self.problem.get_parameters()
        self._name = "CCJ-Linearization"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()

        iterations = log2((n - w) / (n - k)) * (w * (1 - w / n))
        T_iter = (n - k) ** 2 * n
        return log2(T_iter) + iterations


    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()
        return log2(n - k)


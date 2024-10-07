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


from ..base_algorithm import BaseAlgorithm
from .regsd_problem import RegSDProblem


class RegSDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Base class for RegSD algorithms complexity estimator.

        Args:
            problem (RegSDProblem): RegSDProblem object including all necessary parameters
        """
        super(RegSDAlgorithm, self).__init__(problem, **kwargs)
        self._name = "sample_name"

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Returns the time and memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self._compute_time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self._compute_time_and_memory_complexity(parameters)[1]

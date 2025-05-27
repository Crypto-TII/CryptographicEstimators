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
from .if_problem import IFProblem


class IFAlgorithm(BaseAlgorithm):
    def __init__(self, problem: IFProblem, **kwargs):
        """Base class for Integer Factoring Estimator algorithms complexity estimator

        Args:
            problem (IFProblem) -- IFProblem object including all necessary parameters

        """
        super(IFAlgorithm, self).__init__(problem, **kwargs)
   
    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError
        
    def _compute_time_complexity(self, parameters: dict):
        """
        Args:
            parameters (dict): Dictionary of parameters used for time complexity computation
        """
        return self._time_and_memory_complexity(parameters)[0]
    
    def _compute_memory_complexity(self, parameters: dict):
        """Compute and return the memory complexity of the algorithm for the given parameter set.

        Args:
            parameters (dict): A dictionary of parameters used for the memory complexity computation.
        """
        return self._time_and_memory_complexity(parameters)[1]
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Compute and return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): A dictionary containing the parameters.
        """
        return self._tilde_o_time_and_memory_complexity(parameters)[0]
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Compute and return the memory complexity of the algorithm for the given parameter set.

        Args:
            parameters (dict): A dictionary of parameters used for the memory complexity computation.
        """
        return self._tilde_o_time_and_memory_complexity(parameters)[1]

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError
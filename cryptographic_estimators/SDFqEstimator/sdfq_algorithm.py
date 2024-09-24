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
from .sdfq_problem import SDFqProblem


class SDFqAlgorithm(BaseAlgorithm):
    """Base class for Syndrome Decoding over FQ algorithms complexity estimator.

    Args:
        problem (SDFqProblem): An SDFqProblem object including all necessary parameters.
        hmp (bool, optional): Indicates if a hashmap is used for list matching. If False, sorting is used instead. Defaults to True.
    """

    def __init__(self, problem: SDFqProblem, **kwargs):
        super(SDFqAlgorithm, self).__init__(problem, **kwargs)
        self._hmap = kwargs.get("hmap", 1)
        self._adjust_radius = kwargs.get("adjust_radius", 10)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[1]

    def _get_verbose_information(self):
        """Returns a dictionary containing information about the object.
    
        Returns:
            dict: A dictionary with the following keys:
                - CONSTRAINTS
                - PERMUTATIONS
                - TREE
                - GAUSS
                - REPRESENTATIONS
                - LISTS
        """
        verb = dict()
        _ = self._time_and_memory_complexity(self.optimal_parameters(), verbose_information=verb)
        return verb


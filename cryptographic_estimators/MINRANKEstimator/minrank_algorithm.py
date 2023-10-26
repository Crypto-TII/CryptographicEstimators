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
from .minrank_problem import MINRANKProblem
from math import log2


class MINRANKAlgorithm(BaseAlgorithm):
    def __init__(self, problem: MINRANKProblem, **kwargs):
        """
        Base class for MINRANK algorithms complexity estimator

        INPUT:

        - ``problem`` -- MINRANKProblem object including all necessary parameters

        """
        super(MINRANKAlgorithm, self).__init__(problem, **kwargs)
        self._name = "sample_name"
        
        
    def _ngates(self, nmul):
    
        q = self.problem.parameters["q"]
    
        if q != 2:
            nmul = nmul * log2(q) ** 2
        return nmul

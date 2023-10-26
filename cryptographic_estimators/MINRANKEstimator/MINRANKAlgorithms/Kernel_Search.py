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


from ..minrank_algorithm import MINRANKAlgorithm
from ..minrank_problem import MINRANKProblem
from math import ceil, log2
from ..minrank_constants import *

class Kernel_Search(MINRANKAlgorithm):
    """
    Construct an instance of Kernel_Search estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the MINRANKProblem class
    """

    def __init__(self, problem: MINRANKProblem, **kwargs):
        self._name = "Kernel_Search"
        super(Kernel_Search, self).__init__(problem, **kwargs)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        q = self.problem.parameters[MR_Q]
        m = self.problem.parameters[MR_M]
        n = self.problem.parameters[MR_N]
        k = self.problem.parameters[MR_K]
        r = self.problem.parameters[MR_R]
        use_gate_count= self.problem.parameters[MR_USE_GATE_COUNT]
        
        time = 0
        w=2
        use_gate_count= True
        if k > 0:
            a = ceil(k / m)
            main_factor = q ** (a * r)
            second_factor = max(1, k ** w)
            time = main_factor * second_factor
            
            if use_gate_count:
                time = self._ngates(time)
            
            time = log2(time)
        
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        
        q = self.problem.parameters[MR_Q]
        m = self.problem.parameters[MR_M]
        n = self.problem.parameters[MR_N]
        k = self.problem.parameters[MR_K]
        r = self.problem.parameters[MR_R]
        use_gate_count= self.problem.parameters[MR_USE_GATE_COUNT]
        
        memory  = 0
        
        if k > 0:
            memory = max(1, 2 * k * m * n)
            if use_gate_count:
                memory = log2(q) * memory
        
            memory = log2(memory)
    
        return memory

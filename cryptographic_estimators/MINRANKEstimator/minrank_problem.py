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


from ..base_problem import BaseProblem
from .minrank_constants import *


class MINRANKProblem(BaseProblem):
    """
    Construct an instance of MINRANKProblem. Contains the parameters to optimize
    over.

    INPUT: 
        - Fill with parameters

    """

    def __init__(self, q: int, m: int, n: int, k: int, r: int, use_gate_count=False, **kwargs): # Fill with parameters
        super().__init__(**kwargs)
        self.parameters[MR_Q] = q
        self.parameters[MR_M] = m
        self.parameters[MR_N] = n
        self.parameters[MR_K] = k
        self.parameters[MR_R] = r
        self.parameters[MR_USE_GATE_COUNT]=use_gate_count
        

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        return basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        return elements_to_store

    def expected_number_solutions(self):
        """
        Return the logarithm of the expected number of existing solutions to the problem

        """
        pass

    def get_parameters(self):
        """
        Return the optimizations parameters
        """
        return list(self.parameters.values())

    def __repr__(self):
        return "MINRANKProblem"

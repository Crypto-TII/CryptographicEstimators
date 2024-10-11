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


from math import inf


class BaseProblem(object):
    def __init__(self, **kwargs):
        """Construct an instance of BaseProblem.

        Args:
            parameters (dict): Parameters of the problem.
            nsolutions (int): Number of solutions of the problem.
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.
        """
        self.parameters = {}
        self.nsolutions = None
        self.memory_bound = inf if "memory_bound" not in kwargs else kwargs["memory_bound"]

        if self.memory_bound < 0:
            raise ValueError("memory_bound must be either inf or a number >= 0")

    def expected_number_solutions(self):
        """Returns the expected number of existing solutions to the problem."""
        return NotImplementedError

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity associated to a given number of basic-operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        return NotImplementedError

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory elements (logarithmic)
        """
        return NotImplementedError

    def get_parameters(self):
        """Return the optimizations parameters."""
        return list(self.parameters.values())

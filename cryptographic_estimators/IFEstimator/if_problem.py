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


class IFProblem(BaseProblem):
    """Construct an instance of Integer Factoring Problem. 

     Args:
        n (int): bit length of RSA integer to factored

    """

    def __init__(self, n:int , **kwargs): 
        super().__init__(**kwargs)
        self.parameters["n"] = n

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to a certain amount of basic_operations

        Args:
            basic_operations (float): The number of field additions (in logarithmic scale).

        Returns:
            The bit-complexity corresponding to the given number of field additions.
        """
        return basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store

        Args:
            elements_to_store (float): The number of memory operations (logarithmic).

        Returns:
            The memory bit-complexity associated with the given number of elements to store.
        """
        return elements_to_store

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem
        """
        pass

    def get_parameters(self):
        """Returns the optimizations parameters
        """
        return list(self.parameters.values())

    def __repr__(self):
        return "Integer Factoring Problem with parameter n = "  + str(self.parameters["n"])

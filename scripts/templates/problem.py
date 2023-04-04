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


class $$UPPER_CASE_PREFIX$$Problem(BaseProblem):
    """
    Construct an instance of $$UPPER_CASE_PREFIX$$Problem. Contains the parameters to optimize
    over.

    INPUT: 
        - Fill with parameters

    """

    def __init__(self, **kwargs): # Fill with parameters
        super().__init__(**kwargs)

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        pass

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        pass

    def expected_number_solutions(self):
        """
        Return the logarithm of the expected number of existing solutions to the problem

        """
        pass

    def get_parameters(self):
        """
        Return the optimizations parameters
        """
        pass

    def __repr__(self):
        pass
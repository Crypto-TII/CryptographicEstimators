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
    """
    Construct an instance of BaseProblem

    INPUT:

    - ``parameters`` -- dict of parameters of the problem.
    - ``nsolutions`` -- number of solutions of the problem
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem (default: inf)

    """

    def __init__(self, **kwargs):
        self.parameters = {}
        self.nsolutions = None
        self.memory_bound = inf if "memory_bound" not in kwargs else kwargs["memory_bound"]

    def expected_number_solutions(self):
        """
        Returns the expected number of existing solutions to the problem

        """
        return NotImplementedError

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity associated to a given number of basic-operations

        INPUT:

        - ``basic_operations`` -- number of basic operations (logarithmic)

        """
        return NotImplementedError

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory elements (logarithmic)

        """
        return NotImplementedError

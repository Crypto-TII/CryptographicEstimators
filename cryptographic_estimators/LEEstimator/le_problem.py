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
from .le_constants import *
from math import log2, factorial


class LEProblem(BaseProblem):
    """
    Construct an instance of the Linear (Code) Equivalence Problem

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``q`` -- field size
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    - ``memory_bound`` -- maximum allowed memory to use for solving the problem

    """

    def __init__(self, n: int, k: int, q: int, **kwargs):
        super().__init__(**kwargs)
        self.parameters[LE_CODE_LENGTH] = n
        self.parameters[LE_CODE_DIMENSION] = k
        self.parameters[LE_FIELD_SIZE] = q
        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations Fq additions

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        _, _, q = self.get_parameters()
        return basic_operations + log2(log2(q))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of Fq elements to store

        INPUT:

        - ``elements_to_store`` -- number of elements to store (logarithmic)

        """
        _, _, q = self.get_parameters()
        return elements_to_store + log2(log2(q))

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        n, k, q = self.get_parameters()
        return log2(q) * k * k + log2(factorial(n)) - log2(q) * n * (k - 1)

    def __repr__(self):
        n, k, q = self.get_parameters()
        rep = "permutation equivalence problem with (n,k,q) = " \
              + "(" + str(n) + "," + str(k) + "," + str(q) + ")"

        return rep

    def get_parameters(self):
        """
        Returns n, k, q
        """
        return self.parameters.values()

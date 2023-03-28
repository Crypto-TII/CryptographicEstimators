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
from .pk_constants import *
from math import log2, factorial


class PKProblem(BaseProblem):
    """
    Construct an instance of the Permuted Kernel Problem

    INPUT:

    - ``n`` -- columns of the matrix
    - ``m`` -- rows of the matrix
    - ``q`` -- size of the field
    - ``ell`` -- number of rows of the matrix whose permutation should lie in the kernel (default: 1)
    - ``use_parity_row`` -- enables trick of appending extra (all one) row to the matrix, i.e., m -> m+1 (default: false)
    - ``nsolutions`` -- number of solutions of the problem in logarithmic scale (default: expected_number_solutions)

    """


    def __init__(self, n: int, m: int, q: int, ell=1, **kwargs):
        super().__init__(**kwargs)

        self.parameters[PK_COLUMNS] = n
        self.parameters[PK_ROWS] = m
        self.parameters[PK_FIELD_SIZE] = q
        self.parameters[PK_DIMENSION] = ell

        if q ** ell < n:
            raise ValueError("q^ell should be at least n, otherwise possible number of permutations is not maximal")

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))
        if kwargs.get("use_parity_row", False):
            self.parameters[PK_ROWS] += 1

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of Fq additions (logarithmic)

        """
        return basic_operations + log2(log2(self.parameters[PK_FIELD_SIZE]))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of Fq elements the algorithm needs to store (logarithmic)

        """
        return elements_to_store + log2(log2(self.parameters[PK_FIELD_SIZE]))

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        n, m, q, ell = self.get_parameters()
        return log2(factorial(n)) - log2(q) * m * ell

    def __repr__(self):
        n, m, q, ell = self.get_parameters()
        rep = "permuted kernel problem with (n,m,q,ell) = " \
              + "(" + str(n) + "," + str(m) + "," + str(q) + "," + str(ell) + ")"

        return rep

    def get_parameters(self):
        return self.parameters.values()

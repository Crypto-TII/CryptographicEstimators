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
from math import comb, inf, log2
from sage.all import GF
from .sd_constants import *


class SDProblem(BaseProblem):
    """
    Construct an instance of the Syndrome Decoding Problem

    INPUT:

    - ``n`` -- code length
    - ``k`` -- code dimension
    - ``w`` -- error weight
    - ``q`` -- size of the basefield of the code
    - ``nsolutions`` -- number of (expected) solutions of the problem in logarithmic scale
    """

    def __init__(self, n: int, k: int, w: int, q=2, **kwargs):
        super().__init__(**kwargs)
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n - k:
            raise ValueError("w must be smaller or equal to n-k")
        if w <= 0 or k <= 0:
            raise ValueError("w and k must be at least 1")
        self.parameters[SD_CODE_LENGTH] = n
        self.parameters[SD_CODE_DIMENSION] = k
        self.parameters[SD_ERROR_WEIGHT] = w
        self.baseField = GF(q)

        self.nsolutions = kwargs.get("nsolutions", max(
            self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Returns the bit-complexity corresponding to basic_operations field additions

        INPUT:

        - ``basic_operations`` -- Number of field additions (logarithmic)

        """
        q = self.baseField.characteristic()
        n = self.parameters[SD_CODE_LENGTH]
        return log2(log2(q)) + log2(n) + basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Returns the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        return self.to_bitcomplexity_time(elements_to_store)

    def expected_number_solutions(self):
        """
        Returns the logarithm of the expected number of existing solutions to the problem

        """
        # TODO fix for fq
        n, k, w, _ = self.get_parameters()
        return log2(comb(n, w)) - (n - k)

    def __repr__(self):
        """
        """
        n, k, w, _ = self.get_parameters()
        rep = "syndrome decoding problem with (n,k,w) = " \
              + "(" + str(n) + "," + str(k) + "," + \
            str(w) + ") over " + str(self.baseField)

        return rep

    def get_parameters(self):
        """
        Returns the ISD paramters n, k, w, q
        """
        n = self.parameters[SD_CODE_LENGTH]
        k = self.parameters[SD_CODE_DIMENSION]
        w = self.parameters[SD_ERROR_WEIGHT]
        q = self.baseField.characteristic()
        return n, k, w, q

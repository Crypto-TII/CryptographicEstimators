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
from math import log2, comb
from .sdfq_constants import *


class SDFqProblem(BaseProblem):
    def __init__(self, n: int, k: int, w: int, q: int, **kwargs):
        """Construct an instance of the Syndrome Decoding over Fq Problem.

        Args:
            n (int): The code length.
            k (int): The code dimension.
            w (int): The error weight.
            q (int): The size of the base field of the code.
            nsolutions (int): The number of (expected) solutions of the problem in logarithmic scale.
            is_syndrome_zero (bool, optional): If set to true, special algorithmic optimizations can be applied. Defaults to True.
        """
        super().__init__(**kwargs)
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n - k:
            raise ValueError("w must be smaller or equal to n-k")
        if w <= 0 or k <= 0:
            raise ValueError("w and k must be at least 1")
        if q <= 2:
            raise ValueError("q must be at least 3")
        self.parameters[SDFQ_CODE_LENGTH] = n
        self.parameters[SDFQ_CODE_DIMENSION] = k
        self.parameters[SDFQ_ERROR_WEIGHT] = w
        self.parameters[SDFQ_ERROR_FIELD_SIZE] = q

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))
        self.is_syndrome_zero = kwargs.get("is_syndrome_zero", True)

    def to_bitcomplexity_time(self, basic_operations: float):
        """Calculates the bit-complexity corresponding to the number of field additions.
    
        Args:
            basic_operations (float): The number of field additions (logarithmic).
        """
        _,_,_,q=self.get_parameters()
        return basic_operations + log2(log2(q))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated with a given number of elements to store.
    
        Args:
            elements_to_store (float): The number of elements to store (in logarithmic scale).
        """
        return self.to_bitcomplexity_time(elements_to_store)

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem."""
        n, k, w, q = self.get_parameters()
        Nw = log2(comb(n, w)) + log2(q-1)*w + log2(q)*(k - n)
        return max(Nw, 0)

    def __repr__(self):
        n, k, w, q = self.get_parameters()
        rep = "syndrome decoding problem with (n,k,w) = " \
              + "(" + str(n) + "," + str(k) + "," + str(w) + ") over Finite Field of size " + str(q)

        return rep

    def get_parameters(self):
        """Returns the ISD parameters n, k, w, q.
    
        Returns:
            tuple: A tuple containing the ISD parameters n, k, w, q.
        """
        n = self.parameters[SDFQ_CODE_LENGTH]
        k = self.parameters[SDFQ_CODE_DIMENSION]
        w = self.parameters[SDFQ_ERROR_WEIGHT]
        q = self.parameters[SDFQ_ERROR_FIELD_SIZE]
        return n, k, w, q

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
from math import log2
from .regsd_constants import *


class RegSDProblem(BaseProblem):
    def __init__(self, n: int, k: int, w: int, **kwargs):
        """Construct an instance of the Regular Syndrome Decoding Problem.

        Args:
            n (int): Code length
            k (int): Code dimension
            w (int): Error weight
            **kwargs: Additional keyword arguments
                nsolutions: Number of (expected) solutions of the problem in logarithmic scale
                memory_bound: Maximum allowed memory to use for solving the problem
        """
        super().__init__(**kwargs)
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n - k:
            raise ValueError("w must be smaller or equal to n-k")
        if w > n // 2:
            raise ValueError("w must be smaller or equal to n/2")
        if n % w != 0:
            raise ValueError("w must divide n")

        if w <= 0 or k <= 0:
            raise ValueError("w and k must be at least 1")
        if w >= k:
            raise ValueError("w mst be smaller than k to ensure problem hardness")
        self.parameters[RegSD_CODE_LENGTH] = n
        self.parameters[RegSD_CODE_DIMENSION] = k
        self.parameters[RegSD_ERROR_WEIGHT] = w

        self.block_length = n // w
        self.nsolutions = kwargs.get("nsolutions", max(
            self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """Return the bit-complexity corresponding to a certain amount of basic_operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        n, _, _ = self.get_parameters()
        return basic_operations + log2(n)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Return the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory operations (logarithmic)
        """
        n, _, _ = self.get_parameters()
        return elements_to_store + log2(n)

    def expected_number_solutions(self):
        """Return the logarithm of the expected number of existing solutions to the problem."""
        n, k, w = self.get_parameters()
        return log2(n / w) * w - (n - k)

    def get_parameters(self):
        """Return the optimizations parameters."""
        return list(self.parameters.values())

    def __repr__(self):
        n, k, w = self.get_parameters()
        return "RegSDProblem with parameters (n, k, w) = ("+ str(n) + ", " + str(k) + ", " + str(w)+")"

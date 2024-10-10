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
from .rsd_constants import *
from math import log2, ceil
from cryptographic_estimators.helper import is_prime_power, ngates


class RSDProblem(BaseProblem):
    """
    Construct an instance of RSDProblem. Contains the parameters to optimize
    over.

    INPUT: 
        - Fill with parameters

    """

    def __init__(self, q: int, m: int, n: int, k: int, r: int, **kwargs):  # Fill with parameters
        super().__init__(**kwargs)
        self.parameters[RSD_q] = q
        self.parameters[RSD_m] = m
        self.parameters[RSD_n] = n
        self.parameters[RSD_k] = k
        self.parameters[RSD_r] = r
        self._theta = kwargs.get("theta", 2)

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if k < 1:
            raise ValueError("k must be >= 1")

        if r < 1:
            raise ValueError("r must be >= 1")

        if self._theta is not None and not (0 <= self._theta <= 2):
            raise ValueError("theta must be either None or 0<=theta <= 2")

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        q = self.parameters[RSD_q]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        q = self.parameters[RSD_q]

        return log2(ceil(log2(q))) + elements_to_store

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
        return "RSDProblem"

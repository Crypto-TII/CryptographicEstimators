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
from sage.arith.misc import is_prime_power


class UOVProblem(BaseProblem):
    """
    Construct an instance of UOVProblem.

    INPUT: 
        
        - ``n`` -- number of variables
        - ``m`` -- number of polynomials
        - ``q`` -- order of the finite field (default: None)

    """

    def __init__(self, n: int, m: int, q:int, **kwargs):
        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if q is not None and not is_prime_power(q):
            raise ValueError("q must be a prime power")
        
        super().__init__(**kwargs)
        self.parameters["UOV_NUMBER_VARIABLES"] = n
        self.parameters["UOV_NUMBER_POLYNOMIALS"] = m
        self.parameters["UOV_FIELD_SIZE"] = q

    def to_bitcomplexity_time(self, basic_operations: float):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)

        """
        return basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        return elements_to_store

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
        n, m, q = self.get_problem_parameters()
        return f"UOV instance with (n,m,q) = {n}, {m}, {q}"

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
from .mayo_constants import *
from ..helper import is_prime_power, ngates
from math import log2, ceil


class MAYOProblem(BaseProblem):
    def __init__(self, n: int, m: int, o: int, k: int, q: int, **kwargs):
        """Construct an instance of MAYOProblem.

        Args:
            n (int): Number of variables
            m (int): Number of polynomials
            o (int): Dimension of the oil space
            k (int): Whipping parameter
            q (int): Order of the finite field
            **kwargs: Additional keyword arguments
                theta (float or None): Exponent of the conversion factor. If 0 <= theta <= 2,
                    every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
                    If None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q)
                    binary operation. Default is None.
                cost_one_hash (int): Bit complexity of computing one hash value. Default is 17.
                memory_bound (float): Maximum allowed memory to use for solving the problem.
                    Default is inf.
        """
        super().__init__(**kwargs)

        theta = kwargs.get("theta", None)
        cost_one_hash = kwargs.get("cost_one_hash", 17)

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if n <= m:
            raise ValueError("n must be > m")
        
        if o < 1:
            raise ValueError("o must be >= 1")
        
        if k >= n - o:
            raise ValueError("k must be < n - o")

        if not is_prime_power(q):
            raise ValueError("q must be a prime power")
        
        if theta is not None and not (0 <= theta <= 2):
            raise ValueError("theta must be either None or 0 <= theta <= 2")

        if cost_one_hash < 0:
            raise ValueError("The cost of computing one hash must be >= 0")
        
        self.parameters[MAYO_NUMBER_VARIABLES] = n
        self.parameters[MAYO_NUMBER_POLYNOMIALS] = m
        self.parameters[MAYO_OIL_SPACE] = o
        self.parameters[MAYO_WHIPPING_PARAMETER] = k
        self.parameters[MAYO_FIELD_SIZE] = q
        self._theta = theta
        self._cost_one_hash = cost_one_hash

    def hashes_to_basic_operations(self, number_of_hashes: float):
        """Return the number basic operations corresponding to a certain amount of hashes.
    
        Args:
            number_of_hashes (float): Number of hashes (logarithmic)
        """
        bit_complexity_one_hash = self._cost_one_hash
        bit_complexity_all_hashes = number_of_hashes + bit_complexity_one_hash
        bit_complexity_one_basic_operation = self.to_bitcomplexity_time(1)
        number_of_basic_operations =  bit_complexity_all_hashes - bit_complexity_one_basic_operation
        return number_of_basic_operations

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to a certain amount of basic_operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        q = self.parameters[MAYO_FIELD_SIZE]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory operations (logarithmic)
        """
        q = self.parameters[MAYO_FIELD_SIZE]
        return log2(ceil(log2(q))) + elements_to_store

    def get_parameters(self):
        """Returns the optimizations parameters."""
        return list(self.parameters.values())
    
    def npolynomials(self):
        """Return the number of polynomials."""
        return self.parameters[MAYO_NUMBER_POLYNOMIALS]
    
    def nvariables(self):
        """Return the number of variables."""
        return self.parameters[MAYO_NUMBER_VARIABLES]
    

    def order_oil_space(self):
        """Return the dimension of the oil space."""
        return self.parameters[MAYO_OIL_SPACE]
    
    def whipping_parameter(self):
        """Return the whipping parameter."""
        return self.parameters[MAYO_WHIPPING_PARAMETER]

    def order_of_the_field(self):
        """Return the order of the field."""
        return self.parameters[MAYO_FIELD_SIZE]

    @property
    def theta(self):
        """Returns the runtime of the algorithm."""
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """Sets the runtime."""
        self._theta = value

    @property
    def cost_one_hash(self):
        """Returns the bit-complexity of computing one hash."""
        return self._cost_one_hash

    @cost_one_hash.setter
    def cost_one_hash(self, value: float):
        """Sets the bit-complexity of computing one hash."""
        self._cost_one_hash = value

    def __repr__(self):
        n, m, o, k, q = self.get_parameters()
        return f"MAYO instance with (n, m, o, k, q) = ({n}, {m}, {o}, {k}, {q})"

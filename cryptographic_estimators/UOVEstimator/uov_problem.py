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
from ..MQEstimator.mq_helper import ngates
from .uov_constants import *
from math import log2
from sage.functions.other import ceil

class UOVProblem(BaseProblem):
    """
    Construct an instance of UOVProblem.

    INPUT: 
        
        - ``n`` -- number of variables
        - ``m`` -- number of polynomials
        - ``q`` -- order of the finite field
        - ``memory_bound`` -- maximum allowed memory to use for solving the problem (default: inf)

    """

    def __init__(self, n: int, m: int, q:int, **kwargs):
        super().__init__(**kwargs)

        theta = kwargs.get("theta", 2)
        cost_hash = kwargs.get("cost_hash", 17)
        
        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if not is_prime_power(q):
            raise ValueError("q must be a prime power")
        
        if theta < 0 and theta != -1:
            raise ValueError("theta must be greater or equal than 0 or equals to -1")

        if cost_hash < 0:
            raise ValueError("cost_hash must be greater or equals than 0")
  
        self.parameters[UOV_NUMBER_VARIABLES] = n
        self.parameters[UOV_NUMBER_POLYNOMIALS] = m
        self.parameters[UOV_FIELD_SIZE] = q
        self._theta = theta
        self._cost_hash = cost_hash

    def to_bitcomplexity_time(self, basic_operations: float, number_of_hashes=0):
        """
        Return the bit-complexity corresponding to a certain amount of basic_operations

        INPUT:

        - ``basic_operations`` -- Number of basic operations (logarithmic)
        - ``number_of_hashes`` -- Number of hashes  (logarithmic) (default: 0)

        """
        q = self.parameters[UOV_FIELD_SIZE]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta) + number_of_hashes + self._cost_hash

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """
        Return the memory bit-complexity associated to a given number of elements to store

        INPUT:

        - ``elements_to_store`` -- number of memory operations (logarithmic)

        """
        q = self.parameters[UOV_FIELD_SIZE]
        return log2(ceil(log2(q))) + elements_to_store

    def expected_number_solutions(self):
        """
        Return the logarithm of the expected number of existing solutions to the problem

        """
        raise NotImplementedError

    def get_parameters(self):
        """
        Return the optimizations parameters
        """
        return list(self.parameters.values())

    def npolynomials(self):
        """"
        Return the number of polynomials

        TESTS::

            
        """
        return self.parameters[UOV_NUMBER_POLYNOMIALS]

    def nvariables(self):
        """
        Return the number of variables

        TESTS::

            
        """
        return self.parameters[UOV_NUMBER_VARIABLES]

    def order_of_the_field(self):
        """
        Return the order of the field

        """
        return self.parameters[UOV_FIELD_SIZE]

    @property
    def theta(self):
        """
        returns the runtime of the algorithm

        """
        return self._theta

    @theta.setter
    def theta(self, value: float):
        """
        sets the runtime

        """
        self._theta = value

    @property
    def cost_hash(self):
        """
        returns the bit-complexity of computing one hash

        """
        return self._cost_hash

    @cost_hash.setter
    def cost_hash(self, value: float):
        """
        sets the bit-complexity of computing one hash

        """
        self._cost_hash = value

    def __repr__(self):
        n, m, q = self.get_problem_parameters()
        return f"UOV instance with (n, m, q) = ({n}, {m}, {q})"

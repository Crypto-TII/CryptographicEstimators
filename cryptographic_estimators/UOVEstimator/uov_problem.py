# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************


from cryptographic_estimators.base_problem import BaseProblem
from cryptographic_estimators.helper import is_prime_power, ngates
from cryptographic_estimators.UOVEstimator.uov_constants import *
from math import log2, ceil


class UOVProblem(BaseProblem):
    def __init__(self, n: int, m: int, q: int, **kwargs):
        """Construct an instance of UOVProblem.

        Args:
            n (int): Number of variables
            m (int): Number of polynomials
            q (int): Order of the finite field
            **kwargs: Additional keyword arguments
                theta (float, optional): Exponent of the conversion factor. Defaults to 2.
                    If 0 <= theta <= 2, every multiplication in GF(q) is counted as log2(q) ^ theta binary operation.
                    If theta = None, every multiplication in GF(q) is counted as 2 * log2(q) ^ 2 + log2(q) binary operation.
                cost_one_hash (int, optional): Bit complexity of computing one hash value. Defaults to 17.
                memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.
        """
        super().__init__(**kwargs)

        theta = kwargs.get("theta", 2)
        cost_one_hash = kwargs.get("cost_one_hash", 17.5)

        if n < 1:
            raise ValueError("n must be >= 1")

        if m < 1:
            raise ValueError("m must be >= 1")

        if n <= m:
            raise ValueError("n must be > m")

        if not is_prime_power(q):
            raise ValueError("q must be a prime power")

        if theta is not None and not (0 <= theta <= 2):
            raise ValueError("theta must be either None or 0 <= theta <= 2")

        if cost_one_hash < 0:
            raise ValueError("The cost of computing one hash must be >= 0")

        self.parameters[UOV_NUMBER_VARIABLES] = n
        self.parameters[UOV_NUMBER_POLYNOMIALS] = m
        self.parameters[UOV_FIELD_SIZE] = q
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
        number_of_basic_operations = (
            bit_complexity_all_hashes - bit_complexity_one_basic_operation
        )
        return number_of_basic_operations

    def to_bitcomplexity_time(self, basic_operations: float):
        """Return the bit-complexity corresponding to a certain amount of basic operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        q = self.parameters[UOV_FIELD_SIZE]
        theta = self._theta
        return ngates(q, basic_operations, theta=theta)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Return the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory operations (logarithmic)
        """
        q = self.parameters[UOV_FIELD_SIZE]
        return log2(ceil(log2(q))) + elements_to_store

    def get_parameters(self):
        """Return the optimizations parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = UOVProblem(n=14, m=8, q=4)
            >>> E.get_parameters()
            [14, 8, 4]
        """
        return list(self.parameters.values())

    def npolynomials(self):
        """Return the number of polynomials."""
        return self.parameters[UOV_NUMBER_POLYNOMIALS]

    def nvariables(self):
        """Return the number of variables."""
        return self.parameters[UOV_NUMBER_VARIABLES]

    def order_of_the_field(self):
        """Return the order of the field."""
        return self.parameters[UOV_FIELD_SIZE]

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
        n, m, q = self.get_parameters()
        return f"UOV instance with (n, m, q) = ({n}, {m}, {q})"

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


from ..base_problem import BaseProblem
from .le_constants import *
from math import log2, factorial


class LEProblem(BaseProblem):
    def __init__(self, n: int, k: int, q: int, **kwargs):
        """Construct an instance of the Linear (Code) Equivalence Problem.

        Args:
            n (int): Code length
            k (int): Code dimension
            q (int): Field size
            **kwargs: Additional keyword arguments
                nsolutions: Number of (expected) solutions of the problem in logarithmic scale
                memory_bound: Maximum allowed memory to use for solving the problem
        """
        super().__init__(**kwargs)
        self.parameters[LE_CODE_LENGTH] = n
        self.parameters[LE_CODE_DIMENSION] = k
        self.parameters[LE_FIELD_SIZE] = q
        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to basic_operations Fq additions.
    
        Args:
            basic_operations (float): Number of field additions (logarithmic)
        """
        _, _, q = self.get_parameters()
        return basic_operations + log2(log2(q))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of Fq elements to store.
    
        Args:
            elements_to_store (float): Number of elements to store (logarithmic)
        """
        _, _, q = self.get_parameters()
        return elements_to_store + log2(log2(q))

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem."""
        n, k, q = self.get_parameters()
        return log2(q) * k * k + log2(factorial(n)) - log2(q) * n * (k - 1)

    def get_parameters(self):
        """Returns n, k, q."""
        return self.parameters.values()

    def __repr__(self):
        n, k, q = self.get_parameters()
        rep = "permutation equivalence problem with (n,k,q) = " \
              + "(" + str(n) + "," + str(k) + "," + str(q) + ")"

        return rep

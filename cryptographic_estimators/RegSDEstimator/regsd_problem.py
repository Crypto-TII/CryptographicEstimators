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

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
from math import comb, log2
from .sd_constants import *


class SDProblem(BaseProblem):
    """Construct an instance of the Syndrome Decoding Problem.

    Args:
        n (int): Code length.
        k (int): Code dimension.
        w (int): Error weight.
        nsolutions (int): Number of (expected) solutions of the problem in logarithmic scale.
        memory_bound (int): Maximum allowed memory to use for solving the problem.
    """

    def __init__(self, n: int, k: int, w: int, **kwargs):
        super().__init__(**kwargs)
        if k <= 0 or n <= 0 or w <= 0:
            raise ValueError("n, k, w must be positive integers")
        if k > n:
            raise ValueError("k must be smaller or equal to n")
        if w > n - k:
            raise ValueError("w must be smaller or equal to n-k")

        self.parameters[SD_CODE_LENGTH] = n
        self.parameters[SD_CODE_DIMENSION] = k
        self.parameters[SD_ERROR_WEIGHT] = w

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))

    def to_bitcomplexity_time(self, basic_operations: float):
        """Calculates the bit-complexity corresponding to the number of field additions, which are the `basic_operations` for SDAlgorithms.

        Args:
            basic_operations (float): The number of field additions (in logarithmic scale).

        Returns:
            The bit-complexity corresponding to the given number of field additions.
        """
        pass
        n = self.parameters[SD_CODE_LENGTH]
        q = 2
        return log2(log2(q)) + log2(n) + basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated with a given number of elements to store.

        Args:
            elements_to_store (float): The number of memory operations (logarithmic).

        Returns:
            The memory bit-complexity associated with the given number of elements to store.
        """
        return self.to_bitcomplexity_time(elements_to_store)

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem."""
        n, k, w = self.get_parameters()
        return log2(comb(n, w)) - (n - k)

    def __repr__(self):
        n, k, w = self.get_parameters()
        rep = (
            "syndrome decoding problem with (n,k,w) = "
            + "("
            + str(n)
            + ","
            + str(k)
            + ","
            + str(w)
            + ") over Finite Field of size 2"
        )
        return rep

    def get_parameters(self):
        """Returns the ISD paramters n, k, w."""
        n = self.parameters[SD_CODE_LENGTH]
        k = self.parameters[SD_CODE_DIMENSION]
        w = self.parameters[SD_ERROR_WEIGHT]
        return n, k, w

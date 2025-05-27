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

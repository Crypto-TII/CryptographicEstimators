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
from .pk_constants import *
from math import log2, factorial


class PKProblem(BaseProblem):
    def __init__(self, n: int, m: int, q: int, ell=1, **kwargs):
        """Construct an instance of the Permuted Kernel Problem.

        Args:
            n (int): Columns of the matrix.
            m (int): Rows of the matrix.
            q (int): Size of the field.
            ell (int, optional): Number of rows of the matrix whose permutation should lie in the kernel. Defaults to 1.
            **kwargs: Additional keyword arguments.
                use_parity_row (bool): Enables trick of appending extra (all one) row to the matrix, i.e., m -> m+1. Defaults to False.
                nsolutions (int): Number of solutions of the problem in logarithmic scale. Defaults to expected_number_solutions.
        """
        super().__init__(**kwargs)

        self.parameters[PK_COLUMNS] = n
        self.parameters[PK_ROWS] = m
        self.parameters[PK_FIELD_SIZE] = q
        self.parameters[PK_DIMENSION] = ell

        if q ** ell < n:
            raise ValueError("q^ell should be at least n, otherwise possible number of permutations is not maximal")

        self.nsolutions = kwargs.get("nsolutions", max(self.expected_number_solutions(), 0))
        if kwargs.get("use_parity_row", False):
            self.parameters[PK_ROWS] += 1

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to basic_operations field additions.
    
        Args:
            basic_operations (float): Number of Fq additions (logarithmic)
        """
        return basic_operations + log2(log2(self.parameters[PK_FIELD_SIZE]))

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of Fq elements the algorithm needs to store (logarithmic)
        """
        return elements_to_store + log2(log2(self.parameters[PK_FIELD_SIZE]))

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem."""
        n, m, q, ell = self.get_parameters()
        return log2(factorial(n)) - log2(q) * m * ell

    def __repr__(self):
        n, m, q, ell = self.get_parameters()
        rep = "permuted kernel problem with (n,m,q,ell) = " \
              + "(" + str(n) + "," + str(m) + "," + str(q) + "," + str(ell) + ")"

        return rep

    def get_parameters(self):
        return self.parameters.values()

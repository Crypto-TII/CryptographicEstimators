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
from .bike_constants import BIKE_DIMENSION, BIKE_SK_WEIGHT, BIKE_MSG_WEIGHT
from ..base_problem import BaseProblem
from math import log2

#TODO: Fill with parameters
class BIKEProblem(BaseProblem):
    def __init__(self, r: int, w: int, t: int, **kwargs):
        """Construct an instance of BIKEProblem.

        Contains the parameters to optimize over.

        Args:
            r (int): Code dimension
            w (int): Weight of secret key polynomial
            t (int): Weight of polynomials encoding messages
            **kwargs: Additional keyword arguments
                memory_bound: Maximum allowed memory to use for solving the problem
        """
        super().__init__(**kwargs)
        self.parameters = {BIKE_DIMENSION: r, BIKE_SK_WEIGHT: w, BIKE_MSG_WEIGHT: t}

    def to_bitcomplexity_time(self, basic_operations: float):
        """Return the bit-complexity corresponding to a certain amount of basic_operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        code_length = 2 * self.parameters[BIKE_DIMENSION]
        return basic_operations + log2(code_length)

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Return the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory operations (logarithmic)
        """
        code_length = 2 * self.parameters[BIKE_DIMENSION]
        return elements_to_store + log2(code_length)

    def __repr__(self):
        r, w, t = self.get_parameters()
        rep = "BIKE instance with (r,w,t) = " + "(" + str(r) + "," + str(w) + "," + str(t) + ")"
        return rep

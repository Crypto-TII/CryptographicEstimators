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


from math import inf


class BaseProblem(object):
    def __init__(self, **kwargs):
        """Construct an instance of BaseProblem.

        Args:
            parameters (dict): Parameters of the problem.
            nsolutions (int): Number of solutions of the problem.
            memory_bound (float, optional): Maximum allowed memory to use for solving the problem. Defaults to inf.
        """
        self.parameters = {}
        self.nsolutions = None
        self.memory_bound = inf if "memory_bound" not in kwargs else kwargs["memory_bound"]

        if self.memory_bound < 0:
            raise ValueError("memory_bound must be either inf or a number >= 0")

    def expected_number_solutions(self):
        """Returns the expected number of existing solutions to the problem."""
        return NotImplementedError

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity associated to a given number of basic-operations.
    
        Args:
            basic_operations (float): Number of basic operations (logarithmic)
        """
        return NotImplementedError

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store.
    
        Args:
            elements_to_store (float): Number of memory elements (logarithmic)
        """
        return NotImplementedError

    def get_parameters(self):
        """Return the optimizations parameters."""
        return list(self.parameters.values())

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


class IFProblem(BaseProblem):
    """Construct an instance of Integer Factoring Problem. 

     Args:
        n (int): bit length of RSA integer to factored

    """

    def __init__(self, n: int, **kwargs):
        super().__init__(**kwargs)
        self.parameters["n"] = n

    def to_bitcomplexity_time(self, basic_operations: float):
        """Returns the bit-complexity corresponding to a certain amount of basic_operations

        Args:
            basic_operations (float): The number of field additions (in logarithmic scale).

        Returns:
            The bit-complexity corresponding to the given number of field additions.
        """
        return basic_operations

    def to_bitcomplexity_memory(self, elements_to_store: float):
        """Returns the memory bit-complexity associated to a given number of elements to store

        Args:
            elements_to_store (float): The number of memory operations (logarithmic).

        Returns:
            The memory bit-complexity associated with the given number of elements to store.
        """
        return elements_to_store

    def expected_number_solutions(self):
        """Returns the logarithm of the expected number of existing solutions to the problem
        """
        pass

    def get_parameters(self):
        """Returns the optimizations parameters
        """
        return list(self.parameters.values())

    def __repr__(self):
        return "Integer Factoring Problem with parameter n = " + str(self.parameters["n"])

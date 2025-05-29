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



from ..base_algorithm import BaseAlgorithm
from ..base_algorithm import BaseAlgorithm
from .mayo_problem import MAYOProblem



class MAYOAlgorithm(BaseAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Base class for MAYO algorithms complexity estimator.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w (float): Linear algebra constant (default: 2.81)
                h (int): External hybridization parameter (default: 0)
                memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
                bit_complexities (int): Determines if complexity is given in bit operations or basic operations (default 1: in bit)
        """
        super(MAYOAlgorithm, self).__init__(problem, **kwargs)

        self._h = kwargs.get("h", 0)
        self._w = kwargs.get("w", 2.81)
        self.complexity_type = 0
        self._name = "BaseMAYOAlgorithm"

        if self._w is not None and not 2 <= self._w <= 3:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if self._h < 0:
            raise ValueError("h must be >= 0")
        
    def linear_algebra_constant(self):
        """Return the linear algebra constant.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_algorithm import MAYOAlgorithm
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = MAYOAlgorithm(MAYOProblem(n=66, m=64, o=8, k=9, q=16))
            >>> E.linear_algebra_constant()
            2.81
        """
        return self._w

    def __repr__(self):
        """NOTE: self._name must be instanciated via the child class."""
        n, m, o, k, q = self.problem.get_parameters()
        return f"{self._name} estimator for the MAYO signature scheme with parameters (n, m, o, k, q) = ({n}, {m}, {o}, {k}, {q})"

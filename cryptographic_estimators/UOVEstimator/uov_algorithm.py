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


from cryptographic_estimators.base_algorithm import BaseAlgorithm
from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem


class UOVAlgorithm(BaseAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Base class for UOV algorithms complexity estimator.

        Args:
            problem (UOVProblem): UOVProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w (int): Linear algebra constant (default: 2)
                h (int): External hybridization parameter (default: 0)
                memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
                bit_complexities (int): Determines if complexity is given in bit operations or basic operations (default 1: in bit)
        """
        super(UOVAlgorithm, self).__init__(problem, **kwargs)

        self._h = kwargs.get("h", 0)
        self._w = kwargs.get("w", 2.81)
        self._name = "BaseUOVAlgorithm"

        if self._w is not None and not 2 <= self._w <= 3:
            raise ValueError("w must be in the range 2 <= w <= 3")

        if self._h < 0:
            raise ValueError("h must be >= 0")

    def linear_algebra_constant(self):
        """Return the linear algebra constant.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.uov_algorithm import UOVAlgorithm
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> UOVAlgorithm(UOVProblem(n=10, m=5, q=4), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def __repr__(self):
        n, m, q = self.problem.get_parameters()
        return f"{self._name} estimator for the UOV signature scheme with parameters (q, n, m) = ({q}, {n}, {m})"

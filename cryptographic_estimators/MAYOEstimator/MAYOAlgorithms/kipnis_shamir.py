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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from math import log2


class KipnisShamir(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of KipnisShamir estimator.

        First attack on the Oil and Vinegar problem, proposed by Kipnis and Shamir.
        The attack attempts to find vectors in the oil space O, by exploiting the fact
        that these vectors are more likely to be eigenvectors of some publicy-known matrices.

        Note:
            The linear algebra constant `w_ks` is set by default to 2.8 since this is the
            suggested choice in Section 5.4 of [BCCHK23]_

        Args:
            problem (MAYOProblem): Object including all necessary parameters
            w_ks (float, optional): Linear algebra constant (only for kipnis-shamir algorithm). Defaults to 2.8.
            h (int, optional): External hybridization parameter. Defaults to 0.
            excluded_algorithms (list, optional): A list/tuple of MQ algorithms to be excluded. Defaults to [Lokshtanov].
            memory_access (int, optional): Specifies the memory access cost model. Defaults to 0.
                Choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root
                or deploy custom function which takes as input the logarithm of the total memory usage.
            complexity_type (int, optional): Complexity type to consider. Defaults to 0 (estimate).
            bit_complexities (int, optional): Determines if complexity is given in bit operations or basic operations. Defaults to 1 (in bit).
        """
        super().__init__(problem, **kwargs)

        self._name = "KipnisShamir"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

        self._w_ks = kwargs.get("w_ks", 2.8)
        n, _, o, _, _ = self.problem.get_parameters()
        if n <= 2 * o:
            raise ValueError('n should be greater than 2 * o')

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            >>> E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            >>> E.time_complexity()
            50.007820003461546
        """
        n, _, o, _, q = self.problem.get_parameters()
        w_ks = self._w_ks
        time = (n - 2 * o) * log2(q)
        return time + log2(n) * w_ks

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.kipnis_shamir import KipnisShamir
            >>> E = KipnisShamir(MAYOProblem(n=24, m=20, o=8, k=9, q=16))
            >>> E.memory_complexity()
            14.169925001442312
        """
        n, _, o, _, _ = self.problem.get_parameters()
        return log2(o * (n ** 2))

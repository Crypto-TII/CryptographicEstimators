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
from ...MQEstimator.mq_estimator import MQEstimator
from ...MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from ...base_constants import BASE_FORGERY_ATTACK
from ...base_algorithm import optimal_parameter
from math import log2, e


class ClawFinding(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of ClawFinding estimator.

        Claw finding attack is a general attack which works against any signature which
        follows the hash-and-sign paradigm.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w: Linear algebra constant (default: obtained from MAYOAlgorithm)
                h: External hybridization parameter (default: 0)
                excluded_algorithms: A list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
                memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type: Complexity type to consider (0: estimate, default: 0)
                bit_complexities: Determines if complexity is given in bit operations or basic operations (default 1: in bit)
                hash_bit_size: Hash function output size given in bits (default: 512)
        """
        super().__init__(problem, **kwargs)

        self._name = "ClawFinding"
        self._attack_type = BASE_FORGERY_ATTACK

        # hash_bit_size can be adjusted to target a specific security level, as stated in MAYO specificactions
        # (security level 1: 256, security level 3: 384, security level 5: 512)
        self._hash_bit_size = kwargs.get("hash_bit_size", 512)

    @optimal_parameter
    def X(self):
        """Return logarithm of the optimal `X`, i.e. number of inputs (preimages).
    
        Optimal value for `X` is obtained from optimizing the bit-cost expression of the attack 
        reported in MAYO specification (see Section 5.4 in [BCCHK23]_) 36 * m * X + Y * 2 ** 17 using X * Y = q ** m

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            >>> E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            >>> E.X()
            122.962
        """
        _, m, _, _, q = self.problem.get_parameters()
        X = (1 / 2) * (17 - log2(36 * m) + m * log2(q))
        X_rounded = round(X, 3)
        return X_rounded

    @optimal_parameter
    def Y(self):
        """Return logarithm of the optimal Y.
    
        Return logarithm of the number of hashes to compute.
        Optimal value for Y is obtained from X * Y = q ** m using the optimal value of X.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            >>> E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            >>> E.Y()
            117.038
        """
        X =  self.X()
        _, m, _, _, q = self.problem.get_parameters()
        Y = max(m * log2(q) - X, 0)
        Y_rounded = round(Y, 3)
        return Y_rounded

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            >>> E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            >>> E.time_complexity()
            134.0384078561605
        """
        m = self.problem.npolynomials()
        X = self.X()
        Y = self.Y()
        cost_one_hash = self.problem.cost_one_hash
        time_in_bits = log2(36 * m * 2 ** X + 2 ** Y * 2 ** cost_one_hash)
        cost_one_field_mult = self.problem.to_bitcomplexity_time(1)
        time = time_in_bits - cost_one_field_mult
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.claw_finding import ClawFinding
            >>> E = ClawFinding(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            >>> E.memory_complexity()
            124.038
        """
        X = self.X()
        Y = self.Y()
        n, m, _, k, q = self.problem.get_parameters()
        hash_bit_size = self._hash_bit_size
        mem_evals = log2(m) + X
        mem_hashes = log2(hash_bit_size) + Y - log2(q)
        return min(mem_evals, mem_hashes)
    

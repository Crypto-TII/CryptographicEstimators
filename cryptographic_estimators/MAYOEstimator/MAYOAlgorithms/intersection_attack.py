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
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from ...MQEstimator.mq_problem import MQProblem
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from math import log2


class IntersectionAttack(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of IntersectionAttack estimator.

        The intersection attack [Beu20]_ generalizes the ideas behind the Kipnis-Shamir attack, in
        combination with a system-solving approach such as in the reconciliation attack.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            w: Linear algebra constant (default: Obtained from MAYOAlgorithm)
            h: External hybridization parameter (default: 0)
            excluded_algorithms: A list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
            memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
            complexity_type: Complexity type to consider (0: estimate, default: 0)
            bit_complexities: Determines if complexity is given in bit operations or basic operations (default 1: in bit)
        """
        super().__init__(problem, **kwargs)

        self._name = "IntersectionAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK
        n, m, o, _, q = self.problem.get_parameters()
        self._boolean_solve = BooleanSolveFXL(MQProblem(n=n, m=3*m-2, q=q), bit_complexities=False)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_attack import IntersectionAttack
            >>> E = IntersectionAttack(MAYOProblem(n=80, m=60, o=18, k=9, q=16))
            >>> E.time_complexity()
            217.30764571185566
        """
        n, m, o, _, q = self.problem.get_parameters()
        E = self._boolean_solve
        time = E.time_complexity()
        time += (n - (3 * o) + 1) * log2(q)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_attack import IntersectionAttack
            >>> E = IntersectionAttack(MAYOProblem(n=80, m=60, o=18, k=9, q=16))
            >>> E.memory_complexity()
            48.427678101094735
        """
        E = self._boolean_solve
        return E.memory_complexity()
    

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        E = self._boolean_solve
        return E.get_optimal_parameters_dict()      

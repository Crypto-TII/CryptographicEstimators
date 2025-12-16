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


from ..bike_algorithm import BIKEAlgorithm
from ..bike_problem import BIKEProblem
from ...base_constants import BASE_ATTACK_TYPE_MSG_RECOVERY
from ...base_algorithm import BaseAlgorithm
from ...SDEstimator import SDEstimator
from math import log2


class SDMsgAttack(BIKEAlgorithm):
    def __init__(self, problem: BIKEProblem, **kwargs):
        """Construct an instance of SDMsgAttack estimator.

        Estimates complexity of solving syndrome decoding problem corresponding to recovering a BIKE message from a ciphertext.

        Args:
            problem (BIKEProblem): An instance of the BIKEProblem class.
        """
        super().__init__(problem, **kwargs)
        self._name = "SDMsgAttack"
        self._attack_type = BASE_ATTACK_TYPE_MSG_RECOVERY
        r, _, t = self.problem.get_parameters()
        self._SDEstimator = SDEstimator(n=2 * r, k=r, w=t, nsolutions=0, memory_bound=self.problem.memory_bound,
                                        bit_complexities=0, **kwargs)

    @BaseAlgorithm.complexity_type.setter
    def complexity_type(self, input_type):
        BaseAlgorithm.complexity_type.fset(self, input_type)
        self._SDEstimator.complexity_type = input_type

    def get_fastest_sd_algorithm(self):
        return self._SDEstimator.fastest_algorithm()

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters (empty dictionary in this specific case).
        """
        r, _, _ = self.problem.get_parameters()
        return max(self.get_fastest_sd_algorithm().time_complexity() - log2(r)/2, self._compute_memory_complexity(parameters))

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters (empty dictionary in this specific case)
        """
        return self.get_fastest_sd_algorithm().memory_complexity()

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the tilde-O time complexity of the algorithm.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self.get_fastest_sd_algorithm().time_complexity()

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the tilde-O memory complexity of the algorithm.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self.get_fastest_sd_algorithm().memory_complexity()

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters of the internally used sd algorithm."""
        parameters_sd = self.get_fastest_sd_algorithm().get_optimal_parameters_dict()
        parameters_sd["SD-algorithm"] = self.get_fastest_sd_algorithm()._name
        return parameters_sd

    def reset(self):
        """Reset to the initial state of the estimation object."""
        super().reset()
        self._SDEstimator.reset()

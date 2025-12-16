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
from ...base_constants import BASE_ATTACK_TYPE_KEY_RECOVERY
from ...base_algorithm import BaseAlgorithm
from ...SDEstimator import SDEstimator
from math import log2

class SDKeyAttack(BIKEAlgorithm):
    def __init__(self, problem: BIKEProblem, **kwargs):
        """Construct an instance of SDKeyAttack estimator.

        Estimates complexity of solving syndrome decoding problem corresponding to recovering the BIKE secret key from its public key.

        Args:
            problem (BIKEProblem): An instance of the BIKEProblem class.
        """
        super(SDKeyAttack, self).__init__(problem, **kwargs)
        self._name = "SDKeyAttack"
        self._attack_type = BASE_ATTACK_TYPE_KEY_RECOVERY
        r, w, _ = self.problem.get_parameters()
        self._SDEstimator = SDEstimator(n=2 * r, k=r, w=w, nsolutions=log2(r), memory_bound=self.problem.memory_bound,
                                        bit_complexities=0, **kwargs)

    def get_fastest_sd_algorithm(self):
        """Fastest algorithm returned by the SDEstimator object."""
        return self._SDEstimator.fastest_algorithm()

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self.get_fastest_sd_algorithm().time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
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
        """Return the optimal parameters of the internally used sd algorithm."""
        parameters_sd = self.get_fastest_sd_algorithm().get_optimal_parameters_dict()
        parameters_sd["SD-algorithm"] = self.get_fastest_sd_algorithm()._name
        return parameters_sd

    def reset(self):
        """Reset to the initial state of the estimation object."""
        super().reset()
        self._SDEstimator.reset()

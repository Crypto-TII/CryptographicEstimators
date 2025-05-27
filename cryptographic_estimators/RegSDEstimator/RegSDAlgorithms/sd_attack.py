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


from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from ...SDEstimator import SDEstimator
from ...SDEstimator.SDAlgorithms import BJMMdw, BJMMpdw, BJMMplus, MayOzerov, BothMay, Stern, Dumer


#FIX: Performance
class SDAttack(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of SDEstimator to solve the RegSDProblem.

        (for performance reasons for now only BJMM is estimated)

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class.
        """
        super(SDAttack, self).__init__(problem, **kwargs)
        self._name = "SD-Attack"
        n, k, w = self.problem.get_parameters()

        _ = kwargs.pop("bit_complexities", None)
        _ = kwargs.pop("nsolutions", None)
        _ = kwargs.pop("excluded_algorithms", None)
        self.SDEstimator = SDEstimator(n, k, w, bit_complexities=0
                                       , nsolutions=self.problem.nsolutions
                                       , excluded_algorithms=[BJMMdw, BJMMpdw, BJMMplus, MayOzerov, BothMay, Stern, Dumer]
                                       , **kwargs)

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        SD = self.SDEstimator.fastest_algorithm()
        return SD.time_complexity(), SD.memory_complexity()

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        SD = self.SDEstimator.fastest_algorithm()
        d = SD.get_optimal_parameters_dict()
        d["variant"] = SD._name
        return d

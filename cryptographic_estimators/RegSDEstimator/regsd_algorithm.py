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
from .regsd_problem import RegSDProblem


class RegSDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Base class for RegSD algorithms complexity estimator.

        Args:
            problem (RegSDProblem): RegSDProblem object including all necessary parameters
        """
        super(RegSDAlgorithm, self).__init__(problem, **kwargs)
        self._name = "sample_name"

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Returns the time and memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self._compute_time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return self._compute_time_and_memory_complexity(parameters)[1]

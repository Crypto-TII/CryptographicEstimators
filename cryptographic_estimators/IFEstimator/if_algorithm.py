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
from .if_problem import IFProblem


class IFAlgorithm(BaseAlgorithm):
    def __init__(self, problem: IFProblem, **kwargs):
        """Base class for Integer Factoring Estimator algorithms complexity estimator

        Args:
            problem (IFProblem) -- IFProblem object including all necessary parameters

        """
        super(IFAlgorithm, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        """
        Args:
            parameters (dict): Dictionary of parameters used for time complexity computation
        """
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        """Compute and return the memory complexity of the algorithm for the given parameter set.

        Args:
            parameters (dict): A dictionary of parameters used for the memory complexity computation.
        """
        return self._time_and_memory_complexity(parameters)[1]

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Compute and return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): A dictionary containing the parameters.
        """
        return self._tilde_o_time_and_memory_complexity(parameters)[0]

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Compute and return the memory complexity of the algorithm for the given parameter set.

        Args:
            parameters (dict): A dictionary of parameters used for the memory complexity computation.
        """
        return self._tilde_o_time_and_memory_complexity(parameters)[1]

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError

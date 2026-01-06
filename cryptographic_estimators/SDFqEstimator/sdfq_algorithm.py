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
from .sdfq_problem import SDFqProblem


class SDFqAlgorithm(BaseAlgorithm):
    """Base class for Syndrome Decoding over FQ algorithms complexity estimator.

    Args:
        problem (SDFqProblem): An SDFqProblem object including all necessary parameters.
        hmp (bool, optional): Indicates if a hashmap is used for list matching. If False, sorting is used instead. Defaults to True.
    """

    def __init__(self, problem: SDFqProblem, **kwargs):
        super(SDFqAlgorithm, self).__init__(problem, **kwargs)
        self._hmap = kwargs.get("hmap", 1)
        self._adjust_radius = kwargs.get("adjust_radius", 10)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Computes time and memory complexity for given parameters."""
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        return self._time_and_memory_complexity(parameters)[1]

    def _get_verbose_information(self):
        """Returns a dictionary containing information about the object.
    
        Returns:
            dict: A dictionary with the following keys:
                - CONSTRAINTS
                - PERMUTATIONS
                - TREE
                - GAUSS
                - REPRESENTATIONS
                - LISTS
        """
        verb = {}
        _ = self._time_and_memory_complexity(self.optimal_parameters(), verbose_information=verb)
        return verb


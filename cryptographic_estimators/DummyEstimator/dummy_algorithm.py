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
from .dummy_problem import DummyProblem


class DummyAlgorithm(BaseAlgorithm):
    def __init__(self, problem: DummyProblem, **kwargs):
        """Base class for Dummy algorithms complexity estimator.

        Args:
            problem (DummyProblem): DummyProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                memory_access: Specifies the memory access cost model
                    (default: 0, choices: 0 - constant, 1 - logarithmic,
                    2 - square-root, 3 - cube-root or deploy custom function
                    which takes as input the logarithm of the total memory usage)
                complexity_type: Complexity type to consider
                    (0: estimate, 1: tilde O complexity, default: 0)
        """
        super(DummyAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        NOTE: self._name must be instanciated via the child class
        """
        par1, par2 = self.problem.get_parameters()
        return f"{self._name} estimator for the dummy problem with parameters {par1} and {par2} "

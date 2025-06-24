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
from math import log2


class RegularISDPerm(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of RegularISD-Perm estimator from [ES23]_.

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDPerm
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDPerm(RegSDProblem(n=100,k=50,w=10))
            >>> A
            RegularISD-Perm estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(RegularISDPerm, self).__init__(problem, **kwargs)

        self._name = "RegularISD-Perm"
    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()

        # add parity-checks
        k_prime = k - w

        # success pr
        p_iter = log2(1 - k_prime / n) * w

        # cost of one iteration
        T_iter = log2(n - k_prime) * 2

        return T_iter - p_iter

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()
        return log2(n - k + w)

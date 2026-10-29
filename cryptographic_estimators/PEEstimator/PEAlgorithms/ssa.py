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

from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from math import log, log2


class SSA(PEAlgorithm):
    def __init__(self, problem: PEProblem, **kwargs):
        """Complexity estimate of Support Splitting Algorithm [Sen06]_

        Rough Estimate according to [BBPS20]_

        Args:
            problem (PEProblem): PEProblem object including all necessary parameters

        Examples:
            >>> from cryptographic_estimators.PEEstimator.PEAlgorithms import SSA
            >>> from cryptographic_estimators.PEEstimator import PEProblem
            >>> SSA(PEProblem(n=100,k=50,q=3))
            Support Splitting Algorithm estimator for permutation equivalence problem with (n,k,q) = (100,50,3)
        """

        super().__init__(problem, **kwargs)
        self._name = "SSA"

    def _compute_time_complexity(self, parameters: dict):
        n, _, q, h = self.problem.get_parameters()
        return log2(n ** 3 + n ** 2 * q ** h * log(max(h, 1)))

    def _compute_memory_complexity(self, parameters: dict):
        n, k, _, h = self.problem.get_parameters()
        return log2(n * h + n * k + n * (n - k))

    def __repr__(self):
        rep = "Support Splitting Algorithm estimator for " + str(self.problem)
        return rep

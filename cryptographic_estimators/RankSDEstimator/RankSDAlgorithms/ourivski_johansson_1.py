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


from math import log2, ceil
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_problem import RankSDProblem


class OJ1(RankSDAlgorithm):
    """Construct an instance of OJ strategy 1  estimator.

       This algorithm tries to solve a given instance by guessing the coefficient matrix of x
       associated with an F_q basis of Suppx and solving a linearized quadratic system [OJ02]_

       Args:
            problem (RankSDProblem): An instance of the RankSDProblem class.
            **kwargs: Additional keyword arguments.
                w (int): Linear algebra constant (default: 3).
                theta (int): Exponent of the conversion factor (default: 2).

       Examples:
            >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.ourivski_johansson_1 import OJ1
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
            >>> OJ = OJ1(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> OJ
            OJ strategy 1 estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(OJ1, self).__init__(problem, **kwargs)
        self.on_base_field = True
        self._name = "OJ strategy 1"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.ourivski_johansson_1 import OJ1
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> OJ = OJ1(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> OJ.time_complexity()
               323.3881188264893
        """

        q, m, _, k, r = self.problem.get_parameters()
        self.problem.set_operations_on_base_field(self.on_base_field)
        time_complexity = self._w * log2(m * r) + (r - 1) * (k + 1) * log2(q)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.ourivski_johansson_1 import OJ1
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> OJ = OJ1(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
              >>> OJ.memory_complexity()
              19.47199664177152
        """

        _, m, _, k, r = self.problem.get_parameters()
        nn = ceil(((r - 1) * m + k + 1) / (m - 1))
        n_rows = nn * m
        n_columns = (r - 1) * m + k + nn + 1
        return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)

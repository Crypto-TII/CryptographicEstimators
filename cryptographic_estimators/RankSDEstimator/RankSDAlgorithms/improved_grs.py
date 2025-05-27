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


from math import log2, ceil, inf
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_problem import RankSDProblem


class ImprovedGRS(RankSDAlgorithm):
    """Construct an instance of ImprovedGRS estimator.

       This algorithm tries to solve a given instance by searching for a linear subspace E'
       of dimension r' ≥ r such that e*Suppx ⊆ E' for a nonzero e in Fq^m and then
       solving the linear system given by the parity-check equations [AGHT18]_

       Args:
           problem (RankSDProblem): An instance of the RankSDProblem class.
           **kwargs: Additional keyword arguments.
               w (int): Linear algebra constant (default: 3).
               theta (int): Exponent of the conversion factor (default: 2).

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.improved_grs import ImprovedGRS
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
           >>> IGRS = ImprovedGRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> IGRS
           Improved GRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(ImprovedGRS, self).__init__(problem, **kwargs)
        self.on_base_field = True
        self._name = "Improved GRS"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.improved_grs import ImprovedGRS
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> IGRS = ImprovedGRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
              >>> IGRS.time_complexity()
              283.3539031111514
        """

        q, m, n, k, r = self.problem.get_parameters()

        r1 = m - ceil((k + 1) * m / n)
        if r1 > 0:
            self.problem.set_operations_on_base_field(self.on_base_field)
            t1 = self._w * log2((n - k) * m)
            mu1 = r * (m - r1) - m
            time_complexity = t1 + max(0, mu1 * log2(q))
            return time_complexity
        else:
            return inf

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.improved_grs import ImprovedGRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> IGRS = ImprovedGRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> IGRS.memory_complexity()
               26.189305558541125
        """
        _, m, n, k, _ = self.problem.get_parameters()
        r1 = m - ceil((k + 1) * m / n)
        if r1 > 0:
            n_columns = r1 * n
            n_rows = (n - k - 1) * m
            return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)
        else:
            return inf

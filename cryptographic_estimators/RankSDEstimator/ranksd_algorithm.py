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


from math import log2
from .ranksd_helper import compute_nb, compute_mb
from .ranksd_problem import RankSDProblem
from ..base_algorithm import BaseAlgorithm


class RankSDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: RankSDProblem, **kwargs):
        """Base class for RankSD algorithms complexity estimator.

           Args:
                problem (RankSDProblem): RankSDProblem object including all necessary parameters.
                **kwargs: Additional keyword arguments.
                    w (int, optional): linear algebra constant. Defaults to 3.

           Examples:
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_algorithm import RankSDAlgorithm
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> A = RankSDAlgorithm(RankSDProblem(q=2, m=31, n=33, k=15, r=10))
               >>> A
               BaseRankSDAlgorithm estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
        """
        super(RankSDAlgorithm, self).__init__(problem, **kwargs)
        w = kwargs.get("w", 3)
        self._w = w
        self.on_base_field = True
        self._name = "BaseRankSDAlgorithm"

        if w < 2 or 3 < w:
            raise ValueError("w must be in the range 2 <= w <= 3")

    def linear_algebra_constant(self):
        """Return the linear algebra constant.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_algorithm import RankSDAlgorithm
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> RankSDAlgorithm(RankSDProblem(q=2, m=31, n=33, k=15, r=10), w=2).linear_algebra_constant()
               2
        """
        return self._w

    def get_reduced_instance_parameters(self, a, p):
        """Return the problem parameters of the reduced instance, i.e., after puncturing the code on ``p`` positions
           and specializing ``a`` columns in X.

           Args:
             a (int): Number of columns to guess in X.
             p (int): Number of positions to puncture in the code.
        """
        q, m, n, k, r = self.problem.get_parameters()
        q_reduced = q
        m_reduced = m
        n_reduced = n - a - p
        k_reduced = k - a
        r_reduced = r
        return q_reduced, m_reduced, n_reduced, k_reduced, r_reduced

    def compute_time_complexity_helper(self, a, b, p, op_on_base_field):
        """Return the time complexity of the reduced instance, i.e.,
           after puncturing the code on ``p`` positions and specializing ``a`` columns in X.

           Args:
               a (int): Number of columns to guess in X.
               b (int): Degree of linear variables.
               p (int): Number of positions to puncture in the code.
               op_on_base_field (boolean): True if operations are performed on Fq. False if performed on Fq^m.
        """
        self.problem.set_operations_on_base_field(op_on_base_field)

        q, m, n_red, k_red, r = self.get_reduced_instance_parameters(a, p)
        w = self._w
        n_rows = compute_nb(m, n_red, k_red, r, b)
        n_columns = compute_mb(m, n_red, k_red, r, b)
        time_complexity = (a * r) * log2(q) + log2(n_rows) + (w - 1) * log2(n_columns)

        return time_complexity

    def compute_memory_complexity_helper(self, a, b, p, op_on_base_field):
        """Return the time complexity of the reduced instance, i.e.,
           after puncturing the code on ``p`` positions and specializing ``a`` columns in X.

           Args:
               a (int): Number of columns to guess in X.
               b (int): Degree of linear variables.
               p (int): Number of positions to puncture in the code.
               op_on_base_field (boolean): True if operations are performed on Fq. False if performed on Fq^m.
        """

        _, m, n_red, k_red, r = self.get_reduced_instance_parameters(a, p)
        n_rows = compute_nb(m, n_red, k_red, r, b)
        n_columns = compute_mb(m, n_red, k_red, r, b)
        return self.__compute_memory_complexity_helper__(n_rows, n_columns, op_on_base_field)

    def __compute_memory_complexity_helper__(self, n_rows, n_columns, op_on_base_field):
        """Return the log of the number of field elements to store an n_rows x n_columns matrix.

            Args:
                n_rows (int): Number of columns to guess in X.
                n_columns (int): Degree of linear variables.
                op_on_base_field (boolean): True if operations are performed on Fq. False if performed on Fq^m.
        """

        memory_complexity = 0
        self.problem.set_operations_on_base_field(op_on_base_field)
        if n_columns > 0 and n_rows > 0:
            memory_complexity += log2(n_rows * n_columns)

        return memory_complexity

    def __repr__(self):
        q, m, n, k, r = self.problem.get_parameters()
        return f"{self._name} estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = ({q}, {m}, {n}, {k}, {r})"

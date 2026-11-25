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
from .mr_problem import MRProblem
from math import log2, inf


class MRAlgorithm(BaseAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Base class for MR algorithms complexity estimator.

        Args:
            problem (MRProblem): MRProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                w (int, optional): linear algebra constant. Defaults to 3.

        Examples:
            >>> from cryptographic_estimators.MREstimator.mr_algorithm import MRAlgorithm
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> E = MRAlgorithm(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> E
            BaseMRAlgorithm estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """
        super(MRAlgorithm, self).__init__(problem, **kwargs)
        w = kwargs.get("w", 3)
        self._w = w
        self._name = "BaseMRAlgorithm"

        if w < 2 or 3 < w:
            raise ValueError("w must be in the range 2 <= w <= 3")

    def linear_algebra_constant(self):
        """Return the linear algebra constant.

        Tests:
            >>> from cryptographic_estimators.MREstimator.mr_algorithm import MRAlgorithm
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> MRAlgorithm(MRProblem(q=7, m=9, n=10, k=15, r=4), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def get_problem_parameters_reduced(self, a, lv):
        """Return the problem parameters of the reduced instance.
    
        Returns the problem parameters after guessing `a` kernel vectors
        and `lv` entries in the solution vector.

        Args:
        - ``a`` -- no. of vectors to guess in the kernel of the low-rank matrix
        - ``lv`` -- no. of entries to guess in the solution vector
        """
        q, m, n, k, r = self.problem.get_parameters()
        q_reduced = q
        m_reduced = m
        n_reduced = n - a
        k_reduced = k - a * m - lv
        r_reduced = r
        return q_reduced, m_reduced, n_reduced, k_reduced, r_reduced

    @staticmethod
    def _log2_sum(*log_terms):
        """Sum logarithmic costs without constructing large powers of two."""
        largest = max(log_terms)
        if largest == inf:
            return inf
        return largest + log2(sum(2 ** (term - largest) for term in log_terms))

    def _are_hybrid_parameters_invalid(self, a, lv):
        """Check the domain of the hybrid reduction."""
        _, m, n, k, r = self.problem.get_parameters()
        return a < 0 or lv < 0 or lv >= min(r, k) or a > n - r or a * m >= k - lv

    def hybrid_reduction_cost(self, a, lv):
        """Return the logarithmic cost of ProcessGuess.

        The linear-variable substitution is amortized over the kernel guesses.
        The internal solver requires k - lv - am > 0.
        """
        if self._are_hybrid_parameters_invalid(a, lv):
            return inf
        _, m, n, k, r = self.problem.get_parameters()
        k_p = k - lv
        comp_step_2 = a * (k_p + 1) * r * m
        comp_step_3 = (k_p + 1) * (a * m) ** (self._w - 1)
        comp_step_12 = a * m * (k_p - a * m + 1) * m * (n - a)
        cost = comp_step_2 + comp_step_3 + comp_step_12
        return log2(cost) if cost > 0 else -inf

    def hybridization_factor(self, a, lv):
        """Return the logarithm of the number of reduced instances to be solved.
    
        Args:
            a: No. of vectors to guess in the kernel of the low-rank matrix.
            lv: No. of entries to guess in the solution vector.
        """
        q, _, _, _, r = self.problem.get_parameters()
        return (r * a + lv) * log2(q)

    def __repr__(self):
        q, m, n, k, r = self.problem.get_parameters()
        return f"{self._name} estimator for the MinRank problem with (q, m, n, k, r) = ({q}, {m}, {n}, {k}, {r})"

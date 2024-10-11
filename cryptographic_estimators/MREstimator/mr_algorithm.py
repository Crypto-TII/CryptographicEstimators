# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from ..base_algorithm import BaseAlgorithm
from .mr_problem import MRProblem
from math import log2


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

    def cost_reduction(self, a, lv):
        """Return the cost of computing the reduced instance.
    
        The reduced instance is obtained after one guess of `a` kernel vectors.
    
        Args:
            a: Number of vectors to guess in the kernel of the low-rank matrix
        """
        cost_guess_kernel_vectors = 0
        cost_guess_entries = 0
        _, m, n, k, _ = self.problem.get_parameters()
        if lv > 0:
            cost_guess_entries = log2(lv * m * n)

        if a > 0 and lv != k:
            w = self.linear_algebra_constant()
            cost_guess_kernel_vectors = w * log2(min(k - lv, a * m))

        reduction_cost = max(cost_guess_kernel_vectors, cost_guess_entries)

        return reduction_cost

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

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
from .rsd_problem import RSDProblem


class RSDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: RSDProblem, **kwargs):
        """Base class for MR algorithms complexity estimator.
            Args:
                problem (MRProblem): MRProblem object including all necessary parameters
                **kwargs: Additional keyword arguments
                w (int, optional): linear algebra constant. Defaults to 3.

            Examples:
              >>> from cryptographic_estimators.RSDEstimator.rsd_algorithm import RSDAlgorithm
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> E = RSDAlgorithm(RSDProblem(q=2, m=31, n=33, k=15, r=10))
              >>> E
              BaseRSDAlgorithm estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)

        """
        super(RSDAlgorithm, self).__init__(problem, **kwargs)
        w = kwargs.get("w", 3)
        self._w = w
        self._name = "BaseRSDAlgorithm"

        if w < 2 or 3 < w:
            raise ValueError("w must be in the range 2 <= w <= 3")

    def linear_algebra_constant(self):
        """Return the linear algebra constant.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.rsd_algorithm import RSDAlgorithm
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> RSDAlgorithm(RSDProblem(q=2, m=31, n=33, k=15, r=10), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def get_problem_parameters_reduced(self, a, p):
        """Return the problem parameters of the reduced instance, i.e., after puncturing the code on ``p`` positions and specializing ``a`` columns in X

        Args:
           a (int): Number of columns to guess in X
           p (int): Number of positions to puncture in the code
        """
        q, m, n, k, r = self.problem.get_parameters()
        q_reduced = q
        m_reduced = m
        n_reduced = n - a - p
        k_reduced = k - a
        r_reduced = r
        return q_reduced, m_reduced, n_reduced, k_reduced, r_reduced

    def __repr__(self):
        q, m, n, k, r = self.problem.get_parameters()
        return f"{self._name} estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = ({q}, {m}, {n}, {k}, {r})"

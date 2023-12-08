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
        """
        Base class for MR algorithms complexity estimator

        INPUT:

        - ``problem`` -- MRProblem object including all necessary parameters
        - ``w`` -- linear algebra constant (default: 3)

        """
        super(MRAlgorithm, self).__init__(problem, **kwargs)
        w = kwargs.get("w", 3)
        self._w = w
        self._name = "BaseMRAlgorithm"

        if  w < 2 or 3 < w:
            raise ValueError("w must be in the range 2 <= w <= 3")

    def linear_algebra_constant(self):
        """
        Return the linear algebra constant

        TESTS::

            sage: from cryptographic_estimators.MREstimator.mr_algorithm import MRAlgorithm
            sage: from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            sage: MRAlgorithm(MRProblem(q=7, m=9, n=10, k=15, r=4), w=2).linear_algebra_constant()
            2
        """
        return self._w

    def get_problem_parameters_reduced(self, a, lv):
        """
        Return the problem parameters of the reduced instance, i.e., after guessing `a` kernel vectors
        and `lv` entries in the solution vector

        INPUT:

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

    def cost_reduction(self, a):
        """
        Return the cost of computing the reduced instance, i.e., the obtained instance after one guess of
        `a` kernel vectors.

        INPUT:

        - ``a`` -- no. of vectors to guess in the kernel of the low-rank matrix

        """
        if a == 0:
            return 0
        _, m, _, k, _ = self.problem.get_parameters()
        w = self.linear_algebra_constant()
        return w * log2(min(k, a * m))

    def hybridization_factor(self, a, lv):
        """
        Return the logarithm of the number of reduced instances to be solved

        INPUT:

        - ``a`` -- no. of vectors to guess in the kernel of the low-rank matrix
        - ``lv``no. of entries to guess in the solution vector
        """
        q, _, _, _, r = self.problem.get_parameters()
        return (r * a + lv)  *  log2(q)
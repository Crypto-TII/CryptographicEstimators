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
        """
        Base class for RSD algorithms complexity estimator

        INPUT:

        - ``problem`` -- RSDProblem object including all necessary parameters
        - ``w`` -- linear algebra constant (default: 3)

        """
        super(RSDAlgorithm, self).__init__(problem, **kwargs)
        self._name = "RSDAlgorithm"
        self.w = kwargs.get("w", 3)

    def get_problem_parameters_reduced(self, a, p):
        """
        Return the problem parameters of the reduced instance, i.e., after pucturing the code on p positions
        and especializing `a` columns in X

        INPUT:

        - ``a`` -- no. of columns to guess in in X
        - ``p`` -- no. of positions to puncture in the code
        """
        q, m, n, k, r = self.problem.get_parameters()
        q_reduced = q
        m_reduced = m
        n_reduced = n - a - p
        k_reduced = k - a
        r_reduced = r
        return q_reduced, m_reduced, n_reduced, k_reduced, r_reduced

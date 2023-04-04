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

from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from math import log, log2


class SSA(PEAlgorithm):

    def __init__(self, problem: PEProblem, **kwargs):
        """
        Complexity estimate of Support Splitting Algorithm [Sen06]_
        Rough Estimate according to [BBPS20]_

        INPUT:

        - ``problem`` -- PEProblem object including all necessary parameters

        EXAMPLES::

            sage: from cryptographic_estimators.PEEstimator.PEAlgorithms import SSA
            sage: from cryptographic_estimators.PEEstimator import PEProblem
            sage: SSA(PEProblem(n=100,k=50,q=3))
            Support Splitting Algorithm estimator for permutation equivalence problem with (n,k,q) = (100,50,3)

        """

        super().__init__(problem, **kwargs)
        self._name = "SSA"

    def _compute_time_complexity(self, parameters: dict):
        n, _, q, h = self.problem.get_parameters()
        return log2(n ** 3 + n ** 2 * q ** h * log(h))

    def _compute_memory_complexity(self, parameters: dict):
        n, k, q, h = self.problem.get_parameters()
        return log2(n * h + n * k + n * (n - k))

    def __repr__(self):
        rep = "Support Splitting Algorithm estimator for " + str(self.problem)
        return rep

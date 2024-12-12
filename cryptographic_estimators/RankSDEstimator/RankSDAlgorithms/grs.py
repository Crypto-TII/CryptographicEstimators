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


from math import log2, ceil, inf
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_problem import RankSDProblem


class GRS(RankSDAlgorithm):
    """Construct an instance of GRS estimator.

       This algorithm tries to solve a given instance by searching a linear subspace E'
       of dimension r' ≥ r such that Suppx ⊆ E', and solving the linear system
       given by the parity-check equations [GRS16]_

       Args:
            problem (RankSDProblem): An instance of the RankSDProblem class.
            **kwargs: Additional keyword arguments.
               w (int): Linear algebra constant (default: 3).
               theta (int): Exponent of the conversion factor (default: 2).

       Examples:
            >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.grs import GRS
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
            >>> GRSA = GRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> GRSA
            GRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(GRS, self).__init__(problem, **kwargs)
        self.on_base_field = True
        self._name = "GRS"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.grs import GRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> GRSA = GRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> GRSA.time_complexity()
               357.3539031111514
        """

        q, m, n, k, r = self.problem.get_parameters()
        self.problem.set_operations_on_base_field(self.on_base_field)

        r1 = m - ceil(k * m / n)
        t1 = self._w * log2((n - k) * m)
        time_complexity_1 = inf
        if r1 > 0:
            mu1 = r * (m - r1)
            time_complexity_1 = t1 + mu1 * log2(q)

        r1 = m - ceil((k + 1) * m / n)
        time_complexity_2 = inf
        if r1 > 0:
            mu2 = (r - 1) * (m - r1)
            time_complexity_2 = t1 + mu2 * log2(q)

        return min(time_complexity_1, time_complexity_2)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.grs import GRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> GRSA = GRS(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> GRSA.memory_complexity()
               26.229429443574855
        """

        _, m, n, k, _ = self.problem.get_parameters()
        r1 = m - ceil(k * m / n)
        if r1 > 0:
            n_columns = r1 * n
            n_rows = (n - k) * m
            return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)
        else:
            return inf

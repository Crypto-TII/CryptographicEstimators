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


from math import log2
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_problem import RankSDProblem


class BasisEnumeration(RankSDAlgorithm):
    """Construct an instance of Basis Enumeration estimator.

       This algorithm tries to solve a given instance by enumerating
       the possible supports for the vector x, and solving the linear system
       given by the parity-check equations [CS96]_

       Args:
            problem (RankSDProblem): An instance of the RankSDProblem class.
            **kwargs: Additional keyword arguments.
                w (int): Linear algebra constant (default: 3).
                theta (int): Exponent of the conversion factor (default: 2).

       Examples:
            >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.basis_enumeration import BasisEnumeration
            >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
            >>> BE = BasisEnumeration(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> BE
            BasisEnumeration estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(BasisEnumeration, self).__init__(problem, **kwargs)
        self.on_base_field = True
        self._name = "BasisEnumeration"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.basis_enumeration import BasisEnumeration
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> BE = BasisEnumeration(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> BE.time_complexity()
               749.6889972117298
        """
        q, m, n, _, r = self.problem.get_parameters()
        self.problem.set_operations_on_base_field(self.on_base_field)
        time_complexity = self._w * log2(n * r + m) + (m - r) * (r - 1) * log2(q)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.basis_enumeration import BasisEnumeration
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> BE = BasisEnumeration(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> BE.memory_complexity()
               23.014300107627076
        """
        _, m, n, k, r = self.problem.get_parameters()
        n_rows = (n - k) * m
        n_columns = n * r + m
        return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)

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


from ..rsd_algorithm import RSDAlgorithm
from ..rsd_problem import RSDProblem
from math import log2


class BasisEnumeration(RSDAlgorithm):
    """Construct an instance of Basis Enumerator estimator

      This algorithm enumerates the possible supports for the vector x and is introduced in
      Florent Chabaud and Jacques Stern,
      "The Cryptographic Security of the Syndrome Decoding Problem for Rank Distance Codes", ASIACRYPT, 1996.


       Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
            w (int): Linear algebra constant (default: 3).
            theta (int): Exponent of the conversion factor (default: 2).

       Examples:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.basis_enumeration import BasisEnumeration
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> BE = BasisEnumeration(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> BE
            BasisEnumeration estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(BasisEnumeration, self).__init__(problem, **kwargs)
        self._name = "BasisEnumeration"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.basis_enumeration import BasisEnumeration
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> BE = BasisEnumeration(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> BE.time_complexity()
            749.6889972117298
        """
        q, m, n, _, r = self.problem.get_parameters()
        time_complexity = self._w * log2(n * r + m) + (m - r) * (r - 1) * log2(q)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.basis_enumeration import BasisEnumeration
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> BE = BasisEnumeration(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> BE.memory_complexity()
            23.014300107627076
        """
        _, m, n, k, r = self.problem.get_parameters()
        n_rows = (n - k) * m
        n_columns = n * r + m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

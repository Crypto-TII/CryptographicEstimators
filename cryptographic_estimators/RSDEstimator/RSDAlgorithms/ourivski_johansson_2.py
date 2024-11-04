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
from math import log2, ceil


class OJ2(RSDAlgorithm):
    """
     Construct an instance of OJ strategy 2  estimator

     This algorithm is introduced in
     V. Ourivski and T. Johansson,
    “New technique for decoding codes in the rank metric and its cryptography applications,”
    in Problems of Information Transmission, 2002.

     Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
            w (int): Linear algebra constant (default: 3).
            theta (int): Exponent of the conversion factor (default: 2).

     Examples:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_2 import OJ2
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> OJ = OJ2(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> OJ
            OJ strategy 2 estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
     """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(OJ2, self).__init__(problem, **kwargs)
        self._name = "OJ strategy 2"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

               Args:
                   parameters (dict): Dictionary including the parameters.

               Tests:
                   >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_2 import OJ2
                   >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                   >>> OJ = OJ2(RSDProblem(q=2,m=127,n=118,k=48,r=7))
                   >>> OJ.time_complexity()
                   745.7661439067468
        """

        q, m, _, k, r = self.problem.get_parameters()
        time_complexity = self._w * (log2(k + r) + log2(r)) + (r - 1) * (m - r) * log2(q)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
           parameters (dict): Dictionary including the parameters.

        Tests:
           >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_2 import OJ2
           >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
           >>> OJ = OJ2(RSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> OJ.memory_complexity()
           17.081441827692018
        """
        q, m, _, k, r = self.problem.get_parameters()
        N = ceil(((k + 1) * r) / (m - r))
        n_rows = N * m
        n_columns = (k + 1 + N) * r
        memory_complexity = log2(n_rows * n_columns)
        return memory_complexity

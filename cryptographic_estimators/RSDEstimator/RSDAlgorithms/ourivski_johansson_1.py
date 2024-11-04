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


class OJ1(RSDAlgorithm):
    """
    Construct an instance of OJ strategy 1  estimator

    V. Ourivski and T. Johansson,
    “New technique for decoding codes in the rank metric and its cryptography applications,”

    Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
            w (int): Linear algebra constant (default: 3).
            theta (int): Exponent of the conversion factor (default: 2).

    Examples:
           >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_1 import OJ1
           >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
           >>> OJ = OJ1(RSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> OJ
           OJ strategy 1 estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(OJ1, self).__init__(problem, **kwargs)
        self._name = "OJ strategy 1"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

               Args:
                   parameters (dict): Dictionary including the parameters.

               Tests:
                   >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_1 import OJ1
                   >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                   >>> OJ = OJ1(RSDProblem(q=2,m=127,n=118,k=48,r=7))
                   >>> OJ.time_complexity()
                   323.3881188264893
        """

        q, m, n, k, r = self.problem.get_parameters()
        time_complexity = self._w * log2(m * r) + (r - 1) * (k + 1) * log2(q)

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
           parameters (dict): Dictionary including the parameters.

        Tests:
           >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.ourivski_johansson_1 import OJ1
           >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
           >>> OJ = OJ1(RSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> OJ.memory_complexity()
               19.47199664177152
        """

        q, m, n, k, r = self.problem.get_parameters()
        N = ceil(((r - 1) * m + k + 1) / (m - 1))
        n_rows = N * m
        n_columns = (r - 1) * m + k + N + 1
        memory_complexity = log2(n_rows * n_columns)
        return memory_complexity

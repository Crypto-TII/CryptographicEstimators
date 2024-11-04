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
from math import log2, ceil, floor


class ImprovedGRS(RSDAlgorithm):
    """Construct an instance of ImprovedGRS estimator

    This algorithm is introduced in
    N. Aragon, P. Gaborit, A. Hauteville, and J. Tillich,
    “A new algorithm for solving the rank syndrome decoding problem,” ISIT, 2018.

    Args:
        problem (MRProblem): An instance of the MRProblem class.
        **kwargs: Additional keyword arguments.
        w (int): Linear algebra constant (default: 3).
        theta (int): Exponent of the conversion factor (default: 2).

    Examples:
        >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.improved_grs import ImprovedGRS
        >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
        >>> IGRS = ImprovedGRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
        >>> IGRS
        Improved GRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(ImprovedGRS, self).__init__(problem, **kwargs)
        self._name = "Improved GRS"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.improved_grs import ImprovedGRS
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> IGRS = ImprovedGRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
              >>> IGRS.time_complexity()
              283.3539031111514
        """

        q, m, n, k, r = self.problem.get_parameters()

        t1 = self._w * log2((n - k) * m)

        mu1 = r * ceil(((k + 1) * m) / n) - m
        time_complexity = t1 + max(0, mu1 * log2(q))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.improved_grs import ImprovedGRS
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> IGRS = ImprovedGRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> IGRS.memory_complexity()
            26.002220005940632
        """
        _, m, n, k, _ = self.problem.get_parameters()
        r1 = floor((n - (k + 1) * m / n))
        n_columns = r1 * n
        n_rows = (n - k - 1) * m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

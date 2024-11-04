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
from math import log2, floor


class GRS(RSDAlgorithm):
    """
    Construct an instance of GRS estimator

    P. Gaborit, O. Ruatta, and J. Schrek, “On the complexity of the rank syndrome decoding problem,”

    Args:
        problem (MRProblem): An instance of the MRProblem class.
        **kwargs: Additional keyword arguments.
        w (int): Linear algebra constant (default: 3).
        theta (int): Exponent of the conversion factor (default: 2).

    Examples:
         >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.grs import GRS
         >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
         >>> GRSA = GRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
         >>> GRSA
         GRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)

    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(GRS, self).__init__(problem, **kwargs)
        self._name = "GRS"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

                Args:
                    parameters (dict): Dictionary including the parameters.

                Tests:
                    >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.grs import GRS
                    >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                    >>> GRSA = GRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
                    >>> GRSA.time_complexity()
                    351.3539031111514
        """

        q, m, n, k, r = self.problem.get_parameters()
        t1 = self._w * log2(n - k) + self._w * log2(m)
        mu1 = r * floor(k * m / n)
        mu2 = (r - 1) * floor((k + 1) * m / n)
        time_complexity_1 = t1 + mu1 * log2(q)
        time_complexity_2 = t1 + mu2 * log2(q)
        return min(time_complexity_1, time_complexity_2)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.grs import GRS
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> GRSA = GRS(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> GRSA.memory_complexity()
            26.229429443574855
        """

        q, m, n, k, r = self.problem.get_parameters()
        r_1 = floor((n - k) * m / n)
        n_columns = r_1 * n
        n_rows = (n - k) * m
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

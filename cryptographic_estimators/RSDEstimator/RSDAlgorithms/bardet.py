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
from math import comb as binomial


class Bardet(RSDAlgorithm):
    """
    Construct an instance of Bardet estimator

    This algorithm is introduced in
    M. Bardet, P. Briaud, M. Bros, P. Gaborit, V. Neiger, O. Ruatta, and J.P. Tillich,
    “An algebraic attack on rank metric code-based cryptosystems", EUROCRYPT, 2020.

    Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
            w (int): Linear algebra constant (default: 3).
            theta (int): Exponent of the conversion factor (default: 2).

    Examples:
            >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.bardet import Bardet
            >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
            >>> BD = Bardet(RSDProblem(q=2,m=127,n=118,k=48,r=7))
            >>> BD
            Bardet estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(Bardet, self).__init__(problem, **kwargs)
        self._name = "Bardet"

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.bardet import Bardet
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> BD=Bardet(RSDProblem(q=2,m=127,n=118,k=48,r=7), w=2.807)
              >>> BD.time_complexity()
              176.58483881935828
        """

        q, m, n, k, r = self.problem.get_parameters()

        bin1 = m * binomial(n - k - 1, r)
        bin2 = binomial(n, r)
        if bin1 < bin2:
            a = r + 1
        else:
            a = r
        time_complexity = self._w * (a * (log2(m + n) + log2(r)) - sum([log2(i) for i in range(1, a + 1)]))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """

        return 0

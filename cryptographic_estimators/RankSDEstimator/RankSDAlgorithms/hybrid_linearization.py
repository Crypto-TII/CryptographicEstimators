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
from ..ranksd_constants import RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS
from ..ranksd_problem import RankSDProblem
from ...base_algorithm import optimal_parameter


class HybridLinearization(RankSDAlgorithm):
    """Construct an instance of HybridLinearization estimator.

       This algorithm tries to solve a given instance by randomly generating new equations from
       the orginal equations and attempting to solve them by linearization [GRS16]_

       Args:
           problem (RankSDProblem): An instance of the RankSDProblem class.
           **kwargs: Additional keyword arguments.
               w (int): Linear algebra constant (default: 3).
               theta (int): Exponent of the conversion factor (default: 2).

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.hybrid_linearization import HybridLinearization
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
           >>> HL = HybridLinearization(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> HL
           Hybrid Linearization estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(HybridLinearization, self).__init__(problem, **kwargs)
        _, _, _, k, _ = self.problem.get_parameters()

        self.set_parameter_ranges(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS, 1, k)
        self.on_base_field = False
        self._name = "Hybrid Linearization"

    @optimal_parameter
    def t(self):
        """Return the optimal `t`, i.e. the number of zero entries expected to have a random element of the support.

           Examples:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.hybrid_linearization import HybridLinearization
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> HL = HybridLinearization(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
               >>> HL.t()
               15

          Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.hybrid_linearization import HybridLinearization
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> HL = HybridLinearization(RankSDProblem(q=2,m=37,n=41,k=18,r=13))
               >>> HL.t()
               18
        """
        return self._get_optimal_parameter(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.hybrid_linearization import HybridLinearization
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> HL = HybridLinearization(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
              >>> HL.time_complexity()
              312.1543216418806
        """

        q, _, _, k, r = self.problem.get_parameters()
        self.problem.set_operations_on_base_field(self.on_base_field)
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        time_complexity = self._w * (log2(r) + log2(k)) + r * t * log2(q)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.hybrid_linearization import HybridLinearization
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> HL = HybridLinearization(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> HL.memory_complexity()
               19.59624618312637
        """
        _, _, n, k, r = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        n_rows = n - t
        n_columns = ((r + 1) * (k + 1 - t) - 1)
        return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)

    def _are_parameters_invalid(self, parameters: dict):
        """Specifies constraints on the parameters.
        """
        _, _, n, k, r = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        b = (n - t) < ((r + 1) * (k + 1 - t) - 1)
        return b

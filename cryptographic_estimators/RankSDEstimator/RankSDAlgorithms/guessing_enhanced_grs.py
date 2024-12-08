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


from math import log2, floor, inf
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_constants import RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS
from ..ranksd_problem import RankSDProblem
from ...base_algorithm import optimal_parameter


class GuessingEnhancedGRS(RankSDAlgorithm):
    """Construct an instance of GuessingEnhancedGRS estimator.

       This algorithm tries to solve a given instance by guessing t Fq-elements in X and
       then applying the Improved GRS to the instance with the guessed values.

       Args:
           problem (RankSDProblem): An instance of the RankSDProblem class.
           **kwargs: Additional keyword arguments.
               w (int): Linear algebra constant (default: 3).
               theta (int): Exponent of the conversion factor (default: 2).

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
           >>> GEGRS = GuessingEnhancedGRS(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
           >>> GEGRS
           GuessingEnhancedGRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(GuessingEnhancedGRS, self).__init__(problem, **kwargs)
        _, m, n, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS, 0, n * m)
        self.on_base_field = True
        self._name = "GuessingEnhancedGRS"

    @optimal_parameter
    def t(self):
        """Return the optimal `t`, i.e. the number of Fq-elements guessed in X.

           Examples:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> GEGRS = GuessingEnhancedGRS(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
               >>> GEGRS.t()
               1

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> GEGRS = GuessingEnhancedGRS(RankSDProblem(q=2,m=37,n=41,k=18,r=13))
               >>> GEGRS.t()
               6
        """
        return self._get_optimal_parameter(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> GEGRS = GuessingEnhancedGRS(RankSDProblem(q=2,m=31,n=33,k=15,r=10),w=2)
               >>> GEGRS.time_complexity()
               138.25340894568637
        """

        q, m, n, k, r = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]

        r1 = floor(((n - k - 1) * m + t) / n)
        if r1 > 0:
            self.problem.set_operations_on_base_field(self.on_base_field)
            t1 = self._w * log2((n - k) * m + t)
            mu1 = r * (m - r1) - m + t
            time_complexity = t1 + max(0, mu1 * log2(q))
            return time_complexity
        else:
            return inf

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> GEGRS = GuessingEnhancedGRS(RankSDProblem(q=2,m=31,n=33,k=15,r=10),w=2)
              >>> GEGRS.memory_complexity()
              18.08878823871691
        """

        _, m, n, k, _ = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        r1 = floor(((n - k - 1) * m + t) / n)
        if r1 > 0:
            n_columns = r1 * n
            n_rows = (n - k - 1) * m + t
            return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)
        else:
            return inf

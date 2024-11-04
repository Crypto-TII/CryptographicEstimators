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
from ...base_algorithm import optimal_parameter
from math import log2, ceil, floor


class GuessingEnhancedGRS(RSDAlgorithm):
    """
    Construct an instance of GuessingEnhancedGRS estimator

    This algorithm is introduced in
    G. D’Alconzo2, A. Esser, A. Gangemi, and C. Sanna,
    “Ryde with mira: Partial key exposure attacks on rank-based schemes”, 2024.

    Args:
        problem (MRProblem): An instance of the MRProblem class.
        **kwargs: Additional keyword arguments.
        w (int): Linear algebra constant (default: 3).
        theta (int): Exponent of the conversion factor (default: 2).

    Examples:
        >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
        >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
        >>> GEGRS = GuessingEnhancedGRS(RSDProblem(q=2,m=31,n=33,k=15,r=10))
        >>> GEGRS
        GuessingEnhancedGRS estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(GuessingEnhancedGRS, self).__init__(problem, **kwargs)
        _, m, n, _, _ = self.problem.get_parameters()
        self.set_parameter_ranges('t', 0, n * m)
        self._name = "GuessingEnhancedGRS"

    @optimal_parameter
    def t(self):
        """Return the optimal `t`, i.e. the number of Fq-elements guessed in X.

          Examples:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> GEGRS = GuessingEnhancedGRS(RSDProblem(q=2,m=31,n=33,k=15,r=10))
              >>> GEGRS.t()
              1

          Tests:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> GEGRS = GuessingEnhancedGRS(RSDProblem(q=2,m=37,n=41,k=18,r=13))
              >>> GEGRS.t()
              6
          """
        return self._get_optimal_parameter("t")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
               >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
               >>> GEGRS = GuessingEnhancedGRS(RSDProblem(q=2,m=31,n=33,k=15,r=10),w=2)
               >>> GEGRS.time_complexity()
               138.25340894568637
        """

        q, m, n, k, r = self.problem.get_parameters()
        t = parameters['t']
        t1 = self._w * log2((n - k) * m + t)
        mu1 = r * ceil(((k + 1) * m - t) / n) - m + t
        time_complexity = t1 + max(0, mu1 * log2(q))

        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        Args:
           parameters (dict): Dictionary including the parameters.

        Tests:
           >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.guessing_enhanced_grs import GuessingEnhancedGRS
           >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
           >>> GEGRS = GuessingEnhancedGRS(RSDProblem(q=2,m=31,n=33,k=15,r=10),w=2)
           >>> GEGRS.memory_complexity()
           18.08878823871691
        """

        _, m, n, k, _ = self.problem.get_parameters()
        t = parameters['t']
        r_1 = floor(((n - k - 1) * m + t) / n)
        n_columns = r_1 * n
        n_rows = (n - k - 1) * m + t
        memory_complexity = log2(n_rows * n_columns)

        return memory_complexity

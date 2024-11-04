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
from math import log2
from math import comb as binomial


class MaxMinors(RSDAlgorithm):
    """
    Construct an instance of MaxMinors estimator

    M. Bardet, P. Briaud, M. Bros, P. Gaborit, and J.-P. Tillich,
    “Revisiting algebraic attacks on MinRank and on the rank decoding problem.

    Args:
            problem (MRProblem): An instance of the MRProblem class.
            **kwargs: Additional keyword arguments.
            w (int): Linear algebra constant (default: 3).
            theta (int): Exponent of the conversion factor (default: 2).

    Examples:
         >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
         >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
         >>> MM = MaxMinors(RSDProblem(q=2,m=31,n=33,k=15,r=10))
         >>> MM
         MaxMinors estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 31, 33, 15, 10)
    """

    def __init__(self, problem: RSDProblem, **kwargs):
        super(MaxMinors, self).__init__(problem, **kwargs)
        _, _, n, k, _ = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, k)
        self.set_parameter_ranges('p', 0, n)
        self._name = "MaxMinors"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. the number of columns specialized in X.

           Examples:
                >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
                >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                >>> MM = MaxMinors(RSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> MM.a()
                12

           Tests:
                >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
                >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                >>> MM = MaxMinors(RSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> MM.a()
                15
        """
        return self._get_optimal_parameter("a")

    @optimal_parameter
    def p(self):
        """Return the optimal `p`, i.e. the number of positions to puncture the code.

           Examples:
                >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
                >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                >>> MM = MaxMinors(RSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
                >>> MM.p()
                2

           Tests:
                >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
                >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
                >>> MM = MaxMinors(RSDProblem(q=2,m=37,n=41,k=18,r=13), w=2)
                >>> MM.p()
                2
        """
        return self._get_optimal_parameter("p")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> MM = MaxMinors(RSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
              >>> MM.time_complexity()
              152.99052338294462
        """

        a = parameters['a']
        p = parameters['p']
        q, _, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)
        w = self._w
        bin2 = binomial(n_red, r)
        time_complexity = a * r * log2(q) + w * log2(bin2)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters
           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RSDEstimator.RSDAlgorithms.max_minors import MaxMinors
              >>> from cryptographic_estimators.RSDEstimator.rsd_problem import RSDProblem
              >>> MM = MaxMinors(RSDProblem(q=2,m=31,n=33,k=15,r=10), w=2)
              >>> MM.memory_complexity()
              33.00164676141634
        """

        a = parameters['a']
        p = parameters['p']
        _, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)

        n_rows = m * binomial(n_red - k_red - 1, r)
        n_columns = binomial(n_red, r)
        memory_complexity = log2(n_rows * n_columns)
        return memory_complexity

    def _are_parameters_invalid(self, parameters: dict):
        """
        Specifies constraints on the parameters
        """
        a = parameters['a']
        p = parameters['p']
        _, m, n_red, k_red, r = self.get_problem_parameters_reduced(a, p)

        if (n_red - k_red - 1) >= r and n_red >= r:
            bin1 = m * binomial(n_red - k_red - 1, r)
            bin2 = binomial(n_red, r) - 1
            return bin1 < bin2

        return True

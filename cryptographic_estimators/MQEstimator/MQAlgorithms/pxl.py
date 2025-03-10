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


from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries
from cryptographic_estimators.base_algorithm import optimal_parameter
from math import log2, ceil, comb as binomial


class PXL(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of DummyAlgorithm1 estimator.

        ---------------------

        Args:
            

        Examples:

        """
        super().__init__(problem, **kwargs)
        self._name = "PXL"

        n, _, _ = problem.get_problem_parameters()

        self.set_parameter_ranges("k", 1, n//2)

    @optimal_parameter
    def k(self):
        """Return the optimal k

        Examples:
            
        """
        return self._get_optimal_parameter("k")
    
    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, m, q = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        k = parameters["k"]
        H = HilbertSeries(n=n - k, degrees=[2] * m)
        
        D = H.first_nonpositive_coefficient_up_to_degree()
        alpha = sum(
            [
                max(H.coefficient_of_degree(i), 0)
                for i in range(D+1)
            ]
        )
        
        time_1 = log2(k ** 2 * alpha) + log2(binomial(n - k + D, D) * binomial(n + D, D))
        time_2 = k * log2(q) + log2(alpha ** 2 * binomial(k + D, D) + alpha ** w)

        return max(time_1, time_2)

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return 0

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        n, m, _ = self.problem.get_problem_parameters()
        k = self.k()
        H = HilbertSeries(n=n - k, degrees=[2] * m)
        D = H.first_nonpositive_coefficient_up_to_degree()
        alpha = sum(
            [
                max(H.coefficient_of_degree(i), 0)
                for i in range(D+1)
            ]
        )

        d = {"k": k, "alpha": ceil(log2(alpha)), "D": D}
        return d

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
from math import log2, ceil, inf, comb as binomial


class PXL(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of PXL estimator.

        The XL algorithm is a major approach to solving the MQ problem with linearization
        over a coefficient field. The hybrid approach (h-XL) is a variant of the XL algorithm.
        The PXL algorithm is a variant of the h-XL algorithm that reduces the number of operations
        for each of the k guessed variables [FK21]_.

        Args:
            problem (MQProblem): MQProblem object including all necessary parameters.
                w (float): Linear algebra constant (2 <= w <= 3). Default is 2.81
                h (Optional[float]): External hybridization parameter (default: 0).
                memory_access (int): Specifies the memory access cost model.
                    0 - constant (default)
                    1 - logarithmic
                    2 - square-root
                    3 - cube-root
                    Alternatively, deploy a custom function which takes as input the logarithm of the total memory usage and returns the logarithm of the memory access cost.
                complexity_type (int): Complexity type to consider.
                    0 - estimate (default)
                    1 - tilde O complexity

        Examples:
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.pxl import PXL
            >>> E = PXL(MQProblem(n=15, m=15, q=2), bit_complexities=0)
            >>> E
            PXL estimator for the MQ problem with 15 variables and 15 polynomials

        """
        super().__init__(problem, **kwargs)
        self._name = "PXL"

        n = self.problem.nvariables()

        self.set_parameter_ranges("k", 1, n)

    @optimal_parameter
    def k(self):
        """Return the optimal k

        Examples:
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.pxl import PXL
            >>> E = PXL(MQProblem(n=20, m=20, q=256), bit_complexities=0)
            >>> E.k()
            3
        """
        return self._get_optimal_parameter("k")
    
    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.pxl import PXL
            >>> E = PXL(MQProblem(n=20, m=20, q=31), bit_complexities=0)
            >>> E.time_complexity()
            57.36008539315609

        Tests:
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.pxl import PXL
            >>> E = PXL(MQProblem(n=20, m=20, q=256), bit_complexities=0)
            >>> E.time_complexity()
            63.23886285441314
        """
        n, m, q = self.problem.get_problem_parameters()
        w = self.linear_algebra_constant()
        k = parameters["k"]
        H = HilbertSeries(n=n - k, degrees=[2] * m)

        try: 
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
        
        except ValueError:
            return inf

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
        >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
        >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.pxl import PXL
        >>> E = PXL(MQProblem(n=20, m=20, q=256), bit_complexities=0)
        >>> E.memory_complexity()
        50.93179370563208
        """
        n, m, _ = self.problem.get_problem_parameters()
        k = parameters["k"]
        H = HilbertSeries(n=n - k, degrees=[2] * m)
        
        try:
            D = H.first_nonpositive_coefficient_up_to_degree()

            return log2(binomial(k + D, D)) + 2 * log2(binomial(n - k + D, D))
        
        except ValueError:
            return inf

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

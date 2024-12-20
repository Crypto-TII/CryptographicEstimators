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


from cryptographic_estimators.base_algorithm import optimal_parameter
from cryptographic_estimators.MQEstimator.mq_algorithm import MQAlgorithm
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from cryptographic_estimators.MQEstimator.MQAlgorithms.f5 import F5
from math import log2


class HybridF5(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of HybridF5.

        HybridF5 is an algorithm to solve systems of polynomials over a finite field proposed in [BFP09]_, [BFP12]_. The
        algorithm is a tradeoff between exhaustive search and Groebner bases computation. The idea is to fix the value of,
        say, $k$ variables and compute the Groebner bases of $q^{k}$ subsystems, where $q$ is the order of the finite
        field. The Grobner bases computation is done using F5 algorithm.

        Notes:
            See also: mpkc.algorithms.f5.F5, class to compute the complexity of F5 algorithm.

        Args:
            problem (MQProblem): The MQProblem object including all necessary parameters.
            h (int, optional): The external hybridization parameter (default: 0).
            w (float, optional): The linear algebra constant (2 <= w <= 3) (default: 2.81).
            degrees (list, optional): A list/tuple of degree of the polynomials (default: [2]*m, i.e. quadratic system).

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=256, n=5, m=10))
            >>> H
            HybridF5 estimator for the MQ problem with 5 variables and 10 polynomials
        """
        q = problem.order_of_the_field()
        m = problem.npolynomials()
        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        degrees = kwargs.get("degrees", [2] * m)

        if len(degrees) != m:
            raise ValueError(f"len(degrees) must be equal to {m}")

        super().__init__(problem, **kwargs)
        if degrees == [2] * m:
            self._degrees = [2] * self.npolynomials_reduced()
        else:
            self._degrees = degrees
        self._name = "HybridF5"

        n = self.nvariables_reduced()
        self.set_parameter_ranges("k", 0, n - 1)

    def degree_of_polynomials(self):
        """Return a list of degree of the polynomials.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=31, n=5, m=5), degrees=[3]*5)
            >>> H.degree_of_polynomials()
            [3, 3, 3, 3, 3]
        """
        return self._degrees

    @optimal_parameter
    def k(self):
        """Return the optimal k.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=31, n=23, m=23))
            >>> H.k()
            5

        Tests:
            >>> H = HybridF5(MQProblem(q=256, n=10, m=10))
            >>> H.k()
            1
            >>> H = HybridF5(MQProblem(q=256, n=20, m=10))
            >>> H.k()
            1
        """
        return self._get_optimal_parameter("k")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=256, n=10, m=10), bit_complexities=False)
            >>> H.time_complexity(k=2)
            46.38042019731107
        """
        k = parameters["k"]
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(
            MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, bit_complexities=False
        )
        h = self._h
        return log2(q) * k + E.time_complexity() + h * log2(q)

    def _compute_memory_complexity(self, parameters: dict):
        """Compute the memory complexity with respect to k.
    
        Args:
            parameters (dict): A dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=7, n=10, m=12), bit_complexities=False)
            >>> H.memory_complexity(k=1)
            20.659592676441402
        """
        k = parameters["k"]
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(
            MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, bit_complexities=False
        )
        return max(E.memory_complexity(), log2(m * n**2))

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            >>> H.time_complexity(k=3)
            26.38447672418113
        """
        k = parameters["k"]
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, complexity_type=1)
        h = self._h
        return log2(q) * k + E.time_complexity() + h * log2(q)

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Compute the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary containing the required parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> H = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            >>> H.memory_complexity(k = 3)
            12.784634845557521
        """
        k = parameters["k"]
        n, m, q = self.get_reduced_parameters()
        w = self.linear_algebra_constant()
        degrees = self.degree_of_polynomials()
        E = F5(MQProblem(n=n - k, m=m, q=q), w=w, degrees=degrees, complexity_type=1)
        return max(E.memory_complexity(), log2(m * n**2))

    def _find_optimal_tilde_o_parameters(self):
        """Return the optimal parameters to achive the optimal Ō time complexity.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hybrid_f5 import HybridF5
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = HybridF5(MQProblem(q=7, n=10, m=12), complexity_type=1)
            >>> E.optimal_parameters()
            {'k': 9}
        """
        self._find_optimal_parameters()

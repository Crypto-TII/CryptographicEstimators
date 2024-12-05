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
from ...MQEstimator.mq_algorithm import MQAlgorithm
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from math import log2, inf

from cryptographic_estimators.MQEstimator.series.hilbert import HilbertSeries


class Hashimoto(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Hashimoto estimator.

        There are several algorithms for solving systems of quadratic equations, especially 
        when the number of variables is significantly larger than the number of equations. 
        This algorithm reduces the number of variables required compared to previous strategies [Has21]_.

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
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=924, m=67))
            >>> E
            Hashimoto estimator for the MQ problem with 924 variables and 67 polynomials
        """
        super().__init__(problem, **kwargs)
        self._name = "Hashimoto"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

        m = self.problem.npolynomials()               
        self.set_parameter_ranges("a", 3, (m // 2) - 1)   
        self.set_parameter_ranges("k", 1, (m // 2) - 1 )

    @optimal_parameter
    def k(self):
        """
        Return the optimal value of k.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=924, m=67))
            >>> E.k()
            8
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def a(self):
        """
        Return the optimal value of alpha.
        
        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=924, m=67))
            >>> E.a()
            26
        """
        return self._get_optimal_parameter("a")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
    
        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=924, m=67), bit_complexities=False)
            >>> E.time_complexity()
            110.7538907435183
        """
        n, m, q = self.problem.get_problem_parameters()
        a = parameters["a"]
        k = parameters["k"]

        if (a * (m - k) - (a-1)**2 + k) <= n:
            E_1 = BooleanSolveFXL(MQProblem(q=q, n=a, m=a), bit_complexities=0)
            E_2 = BooleanSolveFXL(MQProblem(q=q, n=a-1, m=a-1), bit_complexities=0)
            E_3 = BooleanSolveFXL(MQProblem(q=q, n=m-a-k, m=m-a), bit_complexities=0)

            com1 = log2(m - a - k + 1) + E_1.time_complexity()
            com2 = k * log2(q) + E_2.time_complexity()
            com3 = k * log2(q) + E_3.time_complexity()
            return max(com1, com2, com3)

        return inf
    
    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        return 0













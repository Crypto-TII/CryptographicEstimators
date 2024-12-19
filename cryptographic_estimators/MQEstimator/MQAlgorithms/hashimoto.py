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
from ..mq_constants import MQ_LAS_VEGAS
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from math import log2, inf
import pytest


class Hashimoto(MQAlgorithm):
    def __init__(self, problem: MQProblem, **kwargs):
        """Construct an instance of Hashimoto estimator.

        There are several algorithms for solving systems of quadratic equations, especially 
        when the number of variables is significantly larger than the number of equations. 
        This algorithm ([Has21]_) reduces the number of variables required compared to previous strategies 
        such as those presented in [FNT21]_ and [TW12].  

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
        n, m, q = problem.get_problem_parameters()

        if not isinstance(q, int):
            raise TypeError("q must be an integer")

        if not problem.is_underdefined_system():
            raise ValueError("The MQ problem should be underdefined, i.e., m must be <= n")

        super().__init__(problem, **kwargs)
        self._name = "Hashimoto"

        self.set_parameter_ranges("a", 3, (m // 2) - 1)   
        self.set_parameter_ranges("k", 1, (m // 2) - 1)

    @optimal_parameter
    def k(self):
        """Return the optimal value of k.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.k()
            2
        """
        return self._get_optimal_parameter("k")

    @optimal_parameter
    def a(self):
        """Return the optimal value of alpha.
        
        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.a()
            4
        """
        return self._get_optimal_parameter("a")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.time_complexity()
            29.75041913021961
    
        Tests:
            >>> if skip_long_doctests:
            ...     pytest.skip()
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=924, m=67), bit_complexities=False)
            >>> E.time_complexity()
            111.55965470245576
        """
        n, m, q = self.problem.get_problem_parameters()
        a = parameters["a"]
        k = parameters["k"]

        if (a * (m - k) - (a-1)**2 + k) <= n:
            E_1 = BooleanSolveFXL(MQProblem(q=q, n=a, m=a), bit_complexities=0)
            E_1.set_parameter_ranges('k', 1, a-1);
            E_2 = BooleanSolveFXL(MQProblem(q=q, n=a-1, m=a-1), bit_complexities=0)
            E_2.set_parameter_ranges('k', 1, a - 2);
            E_3 = BooleanSolveFXL(MQProblem(q=q, n=m-a-k, m=m-a), bit_complexities=0)

            com1 = log2(m - a - k + 1) + E_1.time_complexity()
            com2 = k * log2(q) + E_2.time_complexity()
            com3 = k * log2(q) + E_3.time_complexity(k=0, variant=MQ_LAS_VEGAS)
            return max(com1, com2, com3)

        return inf
    
    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MQEstimator.MQAlgorithms.hashimoto import Hashimoto
            >>> from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
            >>> E = Hashimoto(MQProblem(q=16, n=45, m=10))
            >>> E.memory_complexity()
            9.129283016944967
        """
        n, m, q = self.problem.get_problem_parameters()
        a = parameters["a"]
        k = parameters["k"]

        if (a * (m - k) - (a-1)**2 + k) <= n:
            E_1 = BooleanSolveFXL(MQProblem(q=q, n=a, m=a), bit_complexities=0)
            E_1.set_parameter_ranges('k', 1, a-1);
            E_2 = BooleanSolveFXL(MQProblem(q=q, n=a-1, m=a-1), bit_complexities=0)
            E_2.set_parameter_ranges('k', 1, a - 2);
            E_3 = BooleanSolveFXL(MQProblem(q=q, n=m-a-k, m=m-a), bit_complexities=0)

            com1 = E_1.memory_complexity()
            com2 = E_2.memory_complexity()
            com3 = E_3.memory_complexity(k=0, variant=MQ_LAS_VEGAS)
            return max(com1, com2, com3)
        
        return inf













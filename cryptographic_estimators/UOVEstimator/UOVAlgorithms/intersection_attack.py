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


from ..uov_algorithm import UOVAlgorithm
from ..uov_problem import UOVProblem
from ...base_algorithm import optimal_parameter
from math import log2, inf, comb as binomial
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from cryptographic_estimators.base_constants import BASE_KEY_RECOVERY_ATTACK

class IntersectionAttack(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of IntersectionAttack estimator.

        The intersection attack [Beu20]_ generalizes the ideas behind the Kipnis-Shamir attack, in
        combination with a system-solving approach such as in the reconciliation attack.

        Args:
            problem (UOVProblem): An instance of the UOVProblem class.
            **kwargs: Additional keyword arguments.
                memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
                complexity_type: Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).
        """
        super().__init__(problem, **kwargs)

        n, m, _ = self.problem.get_parameters()
        self.set_parameter_ranges('k', 2, 3)
        self._name = "IntersectionAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK

        if n >= 3 * m:
            raise ValueError('n should be less than 3 * m')

    @optimal_parameter
    def k(self):
        """Return the optimal parameter k used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_attack import IntersectionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.k()
            2
        """
        return self._get_optimal_parameter("k")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_attack import IntersectionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.time_complexity()
            23.339850002884624
        """
        n, m, q = self.problem.get_parameters()
        k = parameters["k"]
        N = k * n - (2 * k - 1) * m
        temp = (k - 1) * n - (2 * k - 1) * m
        if N <= 0 or not  temp <= 0: # Second condition is to guarantee that the attack works
            return inf
        M = binomial(k + 1, 2) * m - 2 * binomial(k, 2)
        E = BooleanSolveFXL(MQProblem(n=N, m=M, q=q), bit_complexities=0)
        time = E.time_complexity()
        if temp == 0:
            time += log2((q - 1))
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_attack import IntersectionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = IntersectionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.memory_complexity()     
            13.147204924942228
        """
        n, m, q = self.problem.get_parameters()
        k = parameters["k"]
        N = k * n - (2 * k - 1) * m
        temp = (k - 1) * n - (2 * k - 1) * m
        if N <= 0 or not temp <= 0:
            return inf
        M = binomial(k + 1, 2) * m - 2 * binomial(k, 2)
        E = BooleanSolveFXL(MQProblem(n=N, m=M, q=q), bit_complexities=0)
        return E.memory_complexity()
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        raise NotImplementedError

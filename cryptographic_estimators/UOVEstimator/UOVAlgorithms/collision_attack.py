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
from math import log2, e
from cryptographic_estimators.base_constants import BASE_FORGERY_ATTACK



class CollisionAttack(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of CollisionAttack estimator.

        Collision attack is a general attack which works against any signature which 
        follows the hash-and-sign paradigm. 

        Args:
            problem (UOVProblem): An instance of the UOVProblem class
            **kwargs: Additional keyword arguments
                gray_code_eval_cost (float): Logarithm of the cost to evaluate one polynomial in one vector using Gray-code enumeration (default: log(q))
                X (int): Number of preimages
                Y (int): Number of variables in the salt space
                memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
                complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
        """
        super().__init__(problem, **kwargs)

        self._name = "CollisionAttack"
        self._attack_type = BASE_FORGERY_ATTACK
        self._alpha = 1.25
        self._log2_of_alpha = log2(self._alpha)
        q = problem.order_of_the_field()
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(q))


    @optimal_parameter
    def X(self):
        """Return the optimal `X`, i.e. number of inputs (preimages).

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.X()
            11.958
        """
        _, m, q = self.problem.get_parameters()
        log2_of_alpha = self._log2_of_alpha
        r = self._gray_code_eval_cost
        X = 9.25  +  (1 / 2) * (-log2(3 * m * r)  + log2_of_alpha + m * log2(q))
        X_rounded = round(X, 3)
        return X_rounded
    
    @optimal_parameter
    def Y(self):
        """Return logarithm of the optimal `Y`, i.e. logarithm of number of hashes to compute.

        Examples:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.Y()
            0
        """
        X =  self.X()
        log2_of_alpha = self._log2_of_alpha
        _, m, q = self.problem.get_parameters()
        Y = max(log2(log2_of_alpha) + m * log2(q) - X, 0)
        Y_rounded = round(Y, 3)
        return Y_rounded

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.time_complexity()
            17.38968211094338
        """
        _, m, q = self.problem.get_parameters()
        X = self.X()
        Y = self.Y()
        alpha = self._alpha
        r = self._gray_code_eval_cost
        cost_one_hash = self.problem.cost_one_hash
        time_temp = int((3 / 2) * m * r * 2 ** X) + int(2 ** cost_one_hash * 2 ** Y)
        time_in_bits = log2(time_temp)
        time_in_bits += log2(1/(1 - e ** (-alpha)))
        cost_one_field_mult = self.problem.to_bitcomplexity_time(1)
        time = time_in_bits - cost_one_field_mult
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            >>> E.memory_complexity()
            8.0
        """
        X = self.X()
        Y = self.Y()
        _, m, q = self.problem.get_parameters()
        mem_evals = log2(log2(q)) + log2(m) + X
        mem_hashes = log2(256) + Y
        return min(mem_evals, mem_hashes)
    
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

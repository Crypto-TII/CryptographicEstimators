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
from ...MQEstimator.mq_estimator import MQEstimator
from ...base_algorithm import optimal_parameter
from ...helper import round_or_truncate
from ...base_constants import BASE_MEMORY_BOUND, BASE_NSOLUTIONS, BASE_BIT_COMPLEXITIES, BASE_EXCLUDED_ALGORITHMS
from math import log2, e


class CollisionAttack(UOVAlgorithm):
    """
    Construct an instance of CollisionAttack estimator

    Collision attack is a general attack which works against any signature which 
    follows the hash-and-sign paradigm. 

    INPUT:

    - ``problem`` -- an instance of the UOVProblem class
    - ``gray_code_eval_cost`` -- logarithm of the cost to evaluate one polynomial in one vector using Gray-code enumeration (default: log(n))
    - ``X`` -- Number of preimages
    - ``Y`` -- Number of variables in the salt space
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    """

    def __init__(self, problem: UOVProblem, **kwargs):
        super().__init__(problem, **kwargs)

        self._name = "CollisionAttack"
        self._attack_type = "forgery"
        self._alpha = 1.25
        q = problem.order_of_the_field()
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(q))


    @optimal_parameter
    def X(self):
        """
        Return the optimal `X`, i.e. no. of inputs (preimages)

        EXAMPLES::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.X()
            11.95

        """
        _, m, q = self.problem.get_parameters()
        alpha = self._alpha
        r = self._gray_code_eval_cost
        X = 9.25  +  (1 / 2) * (-log2(3 * m * r)  + log2(alpha) + m * log2(q))
        precision = 2
        X_truncated = float(int(X * 10 ** precision) / 10 ** precision)
        return X_truncated
    
    @optimal_parameter
    def Y(self):
        """
        Return logarithm of the optimal `Y`, i.e. logarithm of no. of hashes to compute

        EXAMPLES::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.Y()
            0.0

        """
        X =  self.X()
        alpha = self._alpha
        _, m, q = self.problem.get_parameters()
        Y = max(log2(alpha) + m * log2(q) - X, 0)
        precision = 2
        Y_truncated = float(int(Y * 10 ** precision) / 10 ** precision)
        return Y_truncated

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.time_complexity()
            17.387737896811494

        """
        _, m, q = self.problem.get_parameters()
        X = self.X()
        Y = self.Y()
        alpha = self._alpha
        r = self._gray_code_eval_cost
        time_temp = int((3 / 2) * m * r * 2 ** X) + int(2 ** 17.5 * 2 ** Y)
        time_in_bits = log2(time_temp)
        time_in_bits += log2(1/(1 - e ** (-alpha)))
        cost_one_field_mult = self.problem.to_bitcomplexity_time(1)
        time = time_in_bits - cost_one_field_mult
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.memory_complexity()
            12.491853096329674

        """
        X = self.X()
        Y = self.Y()
        _, m, q = self.problem.get_parameters()
        mem_evals = log2(log2(q)) + log2(m) + X
        mem_hashes = log2(256) + Y
        return min(mem_evals, mem_hashes)
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        raise NotImplementedError
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        raise NotImplementedError
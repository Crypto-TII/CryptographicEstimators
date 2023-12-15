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
        n = problem.nvariables()
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(n))
        self.set_parameter_ranges('X', 1, n)
        self.set_parameter_ranges('Y', 1, n)

    @optimal_parameter
    def X(self):
        """
        Return the optimal `X`, i.e. no. of inputs (preimages)

        EXAMPLES::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.X()
            1

        """
        return self._get_optimal_parameter('X')
    
    @optimal_parameter
    def Y(self):
        """
        Return the optimal `Y`, i.e. no. of variables in the salt space

        EXAMPLES::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.Y()
            1

        """
        return self._get_optimal_parameter('Y')

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.collision_attack import CollisionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = CollisionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.time_complexity())
            7.759419014654298

        """
        _, m, q = self.problem.get_parameters()
        X = parameters['X']
        Y = parameters['Y']
        r = self._gray_code_eval_cost
        time = log2(((q ** m) * m * r) ** (1/2))
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
            sage: E.memory_complexity())
            12.491853096329674

        """
        n, m, _ = self.problem.get_parameters()
        return log2(m * (n ** 2))
    
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
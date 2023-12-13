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
from ...MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from ...base_constants import BASE_MEMORY_BOUND, BASE_NSOLUTIONS, BASE_BIT_COMPLEXITIES, BASE_EXCLUDED_ALGORITHMS
from math import log2, e

class CollisionAttack(UOVAlgorithm):
    """
    Construct an instance of CollisionAttack estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the UOVProblem class
    - ``gray_code_eval_cost`` -- logarithm of the cost to evaluate one polynomial in one vector using Gray-code enumeration (default: log(n))
    - ``X`` -- Number of inputs
    - ``Y`` -- Number of salts
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    """

    def __init__(self, problem: UOVProblem, **kwargs):
        super().__init__(problem, **kwargs)

        self._name = "CollisionAttack"
        self._attack_type = "forgery"
        self._alpha = 1.25
        n = problem.npolynomials()
        self._gray_code_eval_cost = kwargs.get("gray_code_eval_cost", log2(n))
        self._X = kwargs.get("X")
        self._Y = kwargs.get("Y")

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

           

        """
        n, m, _ = self.problem.get_parameters()

        time = log2(3 * m * self._gray_code_eval_cost * self._X + (2 ** 18.5) *  self._Y)
        time -= log2(1 - (e ** - self._alpha))
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            

        """
        
    
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
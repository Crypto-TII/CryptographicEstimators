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


from ..mayo_algorithm import MAYOAlgorithm
from ..mayo_problem import MAYOProblem
from ...MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from ...MQEstimator.mq_problem import MQProblem
from ...base_constants import BASE_KEY_RECOVERY_ATTACK
from math import log2


class IntersectionAttack(MAYOAlgorithm):
    """
    Construct an instance of IntersectionAttack estimator

    The intersection attack [Beu20]_ generalizes the ideas behind the Kipnis-Shamir attack, in
    combination with a system-solving approach such as in the reconciliation attack.

    INPUT:

    - ``problem`` -- MAYOProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (default: Obtained from MAYOAlgorithm)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``excluded_algorithms`` -- a list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """

    def __init__(self, problem: MAYOProblem, **kwargs):
        super().__init__(problem, **kwargs)

        self._name = "IntersectionAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK
        n, m, o, _, q = self.problem.get_parameters()
        self._boolean_solve = BooleanSolveFXL(MQProblem(n=n, m=3*m-2, q=q), bit_complexities=False)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_attack import IntersectionAttack
            sage: E = IntersectionAttack(MAYOProblem(n=80, m=60, o=18, k=9, q=16))
            sage: E.time_complexity()
            217.30764571185566

        """
        n, m, o, _, q = self.problem.get_parameters()
        E = self._boolean_solve
        time = E.time_complexity()
        time += (n - (3 * o) + 1) * log2(q)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.intersection_attack import IntersectionAttack
            sage: E = IntersectionAttack(MAYOProblem(n=80, m=60, o=18, k=9, q=16))
            sage: E.memory_complexity()
            48.427678101094735

        """
        E = self._boolean_solve
        return E.memory_complexity()
    

    def get_optimal_parameters_dict(self):
        """
        Returns the optimal parameters dictionary

        """
        E = self._boolean_solve
        return E.get_optimal_parameters_dict()      
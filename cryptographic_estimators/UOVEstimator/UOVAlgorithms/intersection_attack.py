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
from math import log2, comb as binomial
from ...MQEstimator.mq_estimator import MQEstimator


class IntersectionAttack(UOVAlgorithm):
    """
    Construct an instance of Kipnis-Shamir estimator

    The intersection attack [Beu20]_ generalizes the ideas behind the Kipnis-Shamir attack, in
    combination with a system-solving approach such as in the reconciliation attack.

    INPUT:

    - ``problem`` -- an instance of the UOVProblem class
    - ``k`` -- Number of vectors in the oil space (default: 2)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)

    """

    def __init__(self, problem: UOVProblem, **kwargs):
        super().__init__(problem, **kwargs)

        n, m, _ = self.problem.get_parameters()

        self._name = "IntersectionAttack"
        self._attack_type = "forgery"
        self._k = kwargs.get("k", 2)

        if n >= ((2 *self._k - 1)/(self._k - 1)) * m:
            raise ValueError('n should be less than (2*k-1)/(k-1)*m')

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_attack import IntersectionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = IntersectionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.time_complexity()
            21.060021436183064

        """
        n, m, q = self.problem.get_parameters()
        k = self._k
        N = k * n - (2 * k - 1) * m
        M = binomial(k + 1, 2) * m - 2 * binomial(k, 2)
        E = MQEstimator(n=N, m=M, q=q).fastest_algorithm()
        return E.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.intersection_attack import IntersectionAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: E = IntersectionAttack(UOVProblem(n=24, m=10, q=2))
            sage: E.memory_complexity()     
            13.147204924942228       

        """
        n, m, q = self.problem.get_parameters()
        k = self._k
        N = k * n - (2 * k - 1) * m
        M = binomial(k + 1, 2) * m - 2 * binomial(k, 2)
        E = MQEstimator(n=N, m=M, q=q).fastest_algorithm()
        return max(E.memory_complexity(), log2(m * n ** 2))
    
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

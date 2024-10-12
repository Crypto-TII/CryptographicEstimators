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


class ReconciliationAttack(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of ReconciliationAttack estimator.

        Reconciliation attack attempts to find vectors in the oils space O by using the fact
        that P(o) = 0 for all o in O.

        Args:
            problem (MAYOProblem): MAYOProblem object including all necessary parameters
            w: Linear algebra constant (default: obtained from MAYOAlgorithm)
            h: External hybridization parameter (default: 0)
            excluded_algorithms: A list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
            memory_access: Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
            complexity_type: Complexity type to consider (0: estimate, default: 0)
            bit_complexities: Determines if complexity is given in bit operations or basic operations (default 1: in bit)
        """
        super().__init__(problem, **kwargs)

        self._name = "ReconciliationAttack"
        self._attack_type = BASE_KEY_RECOVERY_ATTACK
        n, m, o, _, q = self.problem.get_parameters()
        self._boolean_solve = BooleanSolveFXL(MQProblem(n=n-o, m=m, q=q), bit_complexities=False)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_attack import ReconciliationAttack
            >>> E = ReconciliationAttack(MAYOProblem(n=32, m=30, o=12, k=9, q=16))
            >>> E.time_complexity()
            53.33754239288287
        """
        E = self._boolean_solve
        return E.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_attack import ReconciliationAttack
            >>> E = ReconciliationAttack(MAYOProblem(n=32, m=30, o=12, k=9, q=16))
            >>> E.memory_complexity()
            20.434204686526638
        """
        E = self._boolean_solve
        return E.memory_complexity()
    

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        E = self._boolean_solve
        return E.get_optimal_parameters_dict()      

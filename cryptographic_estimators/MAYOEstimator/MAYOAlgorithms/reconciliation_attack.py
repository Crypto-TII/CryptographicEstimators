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
from ...MQEstimator.mq_estimator import MQEstimator
from ...MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from ...base_constants import BASE_EXCLUDED_ALGORITHMS
from math import log2
from sage.functions.other import floor


from ...base_algorithm import optimal_parameter
from cryptographic_estimators.MQEstimator.MQAlgorithms.booleansolve_fxl import BooleanSolveFXL
from cryptographic_estimators.MQEstimator.mq_problem import MQProblem




class ReconciliationAttack(MAYOAlgorithm):
    """
    Construct an instance of ReconciliationAttack estimator

    Reconciliation attack attempts to find vectors in the oils space O by using the fact
    that P(o) = 0 for all o in O. 

    INPUT:

    - ``problem`` -- DummyProblem object including all necessary parameters
    - ``w`` -- linear algebra constant (default: Obtained from MAYOAlgorithm)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``nsolutions`` -- number of solutions in logarithmic scale (default: expected_number_solutions))
    - ``excluded_algorithms`` -- a list/tuple of MQ algorithms to be excluded (default: [Lokshtanov])
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """

    def __init__(self, problem: MAYOProblem, **kwargs):
        super().__init__(problem, **kwargs)

        self._name = "ReconciliationAttack"
        self._attack_type = "key-recovery"
        n, m, o, _, q = self.problem.get_parameters()
        self._boolean_solve = BooleanSolveFXL(MQProblem(n=n-o, m=m, q=q), bit_complexities=False)

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_attack import ReconciliationAttack
            sage: E = ReconciliationAttack(MAYOProblem(n=32, m=30, o=12, k=9, q=16))
            sage: E.time_complexity()
            53.33754239288287

        """
        E = self._boolean_solve
        return E.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.reconciliation_attack import ReconciliationAttack
            sage: E = ReconciliationAttack(MAYOProblem(n=32, m=30, o=12, k=9, q=16))
            sage: E.memory_complexity()
            20.434204686526638

        """
        E = self._boolean_solve
        return E.memory_complexity()
    

    def get_optimal_parameters_dict(self):
        """
        Returns the optimal parameters dictionary

        """
        E = self._boolean_solve
        return E.get_optimal_parameters_dict()      
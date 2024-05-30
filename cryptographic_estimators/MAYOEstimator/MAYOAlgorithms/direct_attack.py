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
from ...base_algorithm import optimal_parameter
from ...helper import ComplexityType
from ..mayo_helper import _optimize_k
from ...base_constants import BASE_EXCLUDED_ALGORITHMS
from math import log2
from sage.functions.other import floor


class DirectAttack(MAYOAlgorithm):
    """
    Construct an instance of DirectAttack estimator

    The most straightforward attack against MAYO is the direct attack, in which the attacker 
    aims to solve an instance of the MQ problem associated with the public map P^* [BCCHK23]_.

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

        self._name = "DirectAttack"
        self._attack_type = "forgery"

        n, m, _, k, q = self.problem.get_parameters()
        self._K = self.K()
        K = self._K
        m_tilde = m - floor(((k*n)-K)/(m-K)) + 1
        n_tilde = m_tilde - K
        w = self.linear_algebra_constant()
        h = self._h
        nsolutions = self.problem.expected_number_solutions()
        excluded_algorithms = kwargs.get(BASE_EXCLUDED_ALGORITHMS, [Lokshtanov])
        complexity_type = self.complexity_type

        if n_tilde <= 0:
            raise ValueError("n_tilde must be > 0")
        if m_tilde <= 0:
            raise ValueError("m_tilde must be > 0")

        self._MQEstimator = MQEstimator(n=n_tilde, m=m_tilde, q=q,
                                        w=w,
                                        h=h,
                                        nsolutions=nsolutions,
                                        excluded_algorithms=excluded_algorithms,
                                        memory_access=0,
                                        complexity_type=complexity_type,
                                        bit_complexities=0)
        
        self._fastest_algorithm = None

    @optimal_parameter
    def K(self):
        """
        Return the optimal parameter `K` from Furue, Nakamura, and Takagi strategy

        EXAMPLES::

            sage: from cryptographic_estimators.MAYOEstimator.mayo_algorithm import MAYOAlgorithm
            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: E = DirectAttack(MAYOProblem(n=80, m=60, o=18, k=12, q=16))
            sage: E.K()
            15
                
        """
        if self._optimal_parameters.get("K") is None:
            n, m, _, k, q = self.problem.get_parameters()
            if self.complexity_type == ComplexityType.ESTIMATE.value:
                return _optimize_k(n=k*n, m=m, k=k, q=q)
            elif self.complexity_type == ComplexityType.TILDEO.value:
                return 0

        return self._optimal_parameters.get("K")

    def get_fastest_mq_algorithm(self):
        """
        Return the fastest algorithm for solving the MQ instance associated with the attack
        """
        if self._fastest_algorithm is None:
            self._fastest_algorithm = self._MQEstimator.fastest_algorithm()
        return self._fastest_algorithm

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: E = DirectAttack(MAYOProblem(n=66, m=64, o=8, k=9, q=16))
            sage: E.time_complexity()
            144.82775006902293

        """
        q = self.problem.order_of_the_field()
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.time_complexity() + self._K * log2(q)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            sage: E = DirectAttack(MAYOProblem(n=66, m=64, o=8, k=9, q=16))
            sage: E.memory_complexity()
            99.2697664172768

        """
        q = self.problem.order_of_the_field()
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.memory_complexity() + self._K * log2(q)
    

    
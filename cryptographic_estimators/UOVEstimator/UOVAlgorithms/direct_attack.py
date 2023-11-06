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


class DirectAttack(UOVAlgorithm):
    """
    Construct an instance of DirectAttack estimator

    The most straightforward attack against UOV, (and even against most of the MPKC 
    cryptosystems) is the direct attack, where the attacker aims to solve an instance of the 
    MQ problem associated with the public key [TW12]_.

    INPUT:

    - ``problem`` -- an instance of the UOVProblem class
    - ``w`` -- linear algebra constant (default: 2)
    - ``h`` -- external hybridization parameter (default: 0)
    - ``memory_access`` -- specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage)
    - ``complexity_type`` -- complexity type to consider (0: estimate, 1: tilde O complexity, default: 0)
    - ``bit_complexities`` -- determines if complexity is given in bit operations or basic operations (default 1: in bit)

    """

    def __init__(self, problem: UOVProblem, **kwargs):
        super(DirectAttack, self).__init__(problem, **kwargs)

        self._name = "DirectAttack"
        n, m, q = self.problem.get_parameters()

        complexity_type = self.complexity_type()
        h = self._h
        nsolutions = self.problem.nsolutions()
        self._MQEstimator = MQEstimator(n, m, q,
                                        bit_complexities=0,
                                        memory_access=0,
                                        h = h,
                                        complexity_type=mq_complexity_type)
        self._fastest_algorithm = None

    def get_fastest_mq_algorithm(self):
        if self._fastest_algorithm is None:
            self._fastest_algorithm = self._MQEstimator.fastest_algorithm()
        return self._fastest_algorithm

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: A = DirectAttack(UOVProblem(n=10, m=12, q=5))
            sage: A.time_complexity()
            22.000568934770925
        """
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type()
        fastest_algorithm.bit_complexities = self.complexity_type()
        return self._fastest_algorithm.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: A = DirectAttack(UOVProblem(n=10, m=12, q=5))
            sage: A.memory_complexity()
            20.965093767318066
        """
        self._MQEstimator.complexity_type = 0
        return self._fastest_algorithm.memory_complexity()
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the Ō time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: A = DirectAttack(UOVProblem(n=10, m=12, q=5), complexity_type=1)
            sage: A.time_complexity()
            19.39681379895914
        """
        self._MQEstimator.complexity_type = 1
        return self._fastest_algorithm.time_complexity()
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the Ō memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

         TESTS::

            sage: from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            sage: from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            sage: A = DirectAttack(UOVProblem(n=10, m=12, q=5), complexity_type=1)
            sage: A.memory_complexity()
            19.38013126659691
        """

        self._MQEstimator.complexity_type = 1
        return self._fastest_algorithm.memory_complexity()
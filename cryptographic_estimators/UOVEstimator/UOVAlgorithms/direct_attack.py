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
from ...base_constants import BASE_EXCLUDED_ALGORITHMS
from cryptographic_estimators.base_constants import BASE_FORGERY_ATTACK

class DirectAttack(UOVAlgorithm):
    def __init__(self, problem: UOVProblem, **kwargs):
        """Construct an instance of DirectAttack estimator.

        The most straightforward attack against UOV, (and even against most of the MPKC 
        cryptosystems) is the direct attack, where the attacker aims to solve an instance of the 
        MQ problem associated with the public key [TW12]_.

        Args:
            problem (UOVProblem): An instance of the UOVProblem class.
            **kwargs: Additional keyword arguments.
                w (int): Linear algebra constant (default: 2).
                h (int): External hybridization parameter (default: 0).
                excluded_algorithms (list): A list/tuple of MQ algorithms to be excluded (default: [Lokshtanov]).
                memory_access (int): Specifies the memory access cost model (default: 0, choices: 0 - constant, 1 - logarithmic, 2 - square-root, 3 - cube-root or deploy custom function which takes as input the logarithm of the total memory usage).
                complexity_type (int): Complexity type to consider (0: estimate, 1: tilde O complexity, default: 0).
                bit_complexities (int): Determines if complexity is given in bit operations or basic operations (default 1: in bit).
        """
        super(DirectAttack, self).__init__(problem, **kwargs)

        self._name = "DirectAttack"
        n, m, q = self.problem.get_parameters()

        w = self.linear_algebra_constant()
        h = self._h
        excluded_algorithms = kwargs.get(BASE_EXCLUDED_ALGORITHMS, [Lokshtanov])
        complexity_type = self.complexity_type
        self._MQEstimator = MQEstimator(n=n, m=m, q=q,
                                        w=w,
                                        h=h,
                                        excluded_algorithms=excluded_algorithms,
                                        memory_access=0,
                                        complexity_type=complexity_type,
                                        bit_complexities=0)
        self._fastest_algorithm = None
        self._attack_type = BASE_FORGERY_ATTACK

    def get_fastest_mq_algorithm(self):
        if self._fastest_algorithm is None:
            self._fastest_algorithm = self._MQEstimator.fastest_algorithm()
        return self._fastest_algorithm

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> A = DirectAttack(UOVProblem(n=14, m=12, q=5))
            >>> A.time_complexity()
            29.92041846257129
        """
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> A = DirectAttack(UOVProblem(n=14, m=12, q=5))
            >>> A.memory_complexity()
            12.339850002884624
        """
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.memory_complexity()
    
    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """Return the Ō time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> A = DirectAttack(UOVProblem(n=14, m=12, q=5), complexity_type=1)
            >>> A.time_complexity()
            23.609416039920553
        """
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.time_complexity()
    
    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """Return the Ō memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

         Tests:
            >>> from cryptographic_estimators.UOVEstimator.UOVAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.UOVEstimator.uov_problem import UOVProblem
            >>> A = DirectAttack(UOVProblem(n=14, m=12, q=5), complexity_type=1)
            >>> A.memory_complexity()
            19.595388618985982
        """
        fastest_algorithm = self.get_fastest_mq_algorithm()
        fastest_algorithm.complexity_type = self.complexity_type
        return self._fastest_algorithm.memory_complexity()
    
    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        fastest_algorithm = self.get_fastest_mq_algorithm()
        d = fastest_algorithm.get_optimal_parameters_dict()
        d["variant"] = fastest_algorithm._name
        return d

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
from ...MQEstimator.mq_problem import MQProblem
from ...MQEstimator.MQAlgorithms.hashimoto import Hashimoto
from ...MQEstimator.MQAlgorithms.lokshtanov import Lokshtanov
from ...base_algorithm import optimal_parameter
from ...helper import ComplexityType
from ..mayo_helper import _optimize_k
from ...base_constants import BASE_EXCLUDED_ALGORITHMS, BASE_FORGERY_ATTACK
from math import log2, floor


class DirectAttack(MAYOAlgorithm):
    def __init__(self, problem: MAYOProblem, **kwargs):
        """Construct an instance of DirectAttack estimator.

        The most straightforward attack against MAYO is the direct attack, in which the attacker 
        aims to solve an instance of the MQ problem associated with the public map P^* [BCCHK23]_.

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

        self._name = "DirectAttack"
        self._attack_type = BASE_FORGERY_ATTACK

        n, m, _, k, q = self.problem.get_parameters()
        self._hashimoto = Hashimoto(MQProblem(n=n*k, m=m, q=q), bit_complexities=0)

    @optimal_parameter
    def k(self):
        """Return the optimal value of k.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = DirectAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16))
            >>> E.k()
            2
        """
        E = self._hashimoto
        return E._get_optimal_parameter("k")

    @optimal_parameter
    def a(self):
        """Return the optimal value of alpha.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = DirectAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16))
            >>> E.a()
            9
        """
        E = self._hashimoto
        return E._get_optimal_parameter("a")

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = DirectAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16))
            >>> E.time_complexity()
            45.114555923134844

        """
        E = self._hashimoto
        return E.time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Examples:
            >>> from cryptographic_estimators.MAYOEstimator.MAYOAlgorithms.direct_attack import DirectAttack
            >>> from cryptographic_estimators.MAYOEstimator.mayo_problem import MAYOProblem
            >>> E = DirectAttack(MAYOProblem(n=22, m=20, o=4, k=5, q=16))
            >>> E.memory_complexity()
            15.289154353723356

        """
        E = self._hashimoto
        return E.memory_complexity()
    
    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        E = self._hashimoto
        d = E.get_optimal_parameters_dict()
        d["variant"] = E._name
        return d
    

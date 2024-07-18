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


from ..bike_algorithm import BIKEAlgorithm
from ..bike_problem import BIKEProblem
from ...base_constants import BASE_ATTACK_TYPE_KEY_RECOVERY
from ...base_algorithm import BaseAlgorithm
from ...SDEstimator import SDEstimator
from math import log2

class SDKeyAttack(BIKEAlgorithm):
    """
    Construct an instance of SDKeyAttack estimator
    (estimates complexity of solving syndrome decoding problem corresponding to recovering the BIKE secret key from its public key)

    INPUT:

    - ``problem`` -- an instance of the BIKEProblem class
    """

    def __init__(self, problem: BIKEProblem, **kwargs):
        self._name = "SDKeyAttack"
        super(SDKeyAttack, self).__init__(problem, **kwargs)
        self._attack_type = BASE_ATTACK_TYPE_KEY_RECOVERY
        r, w, _ = self.problem.get_parameters()
        self._SDEstimator = SDEstimator(n=2 * r, k=r, w=w, nsolutions=log2(r), memory_bound=self.problem.memory_bound,
                                        bit_complexities=0, **kwargs)

    @BaseAlgorithm.complexity_type.setter
    def complexity_type(self, input_type):
        """
        sets complexity type of algorithm and included SDEstimator object
        """
        BaseAlgorithm.complexity_type.fset(self, input_type)
        self._SDEstimator.complexity_type = input_type

    def get_fastest_sd_algorithm(self):
        """
        Fastest algorithm returned by the SDEstimator object
        """
        return self._SDEstimator.fastest_algorithm()

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return self.get_fastest_sd_algorithm().time_complexity()

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return self.get_fastest_sd_algorithm().memory_complexity()

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return self.get_fastest_sd_algorithm().time_complexity()

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        return self.get_fastest_sd_algorithm().memory_complexity()

    def get_optimal_parameters_dict(self):
        """
        return the optimal parameters of the internally used sd algorithm
        """
        parameters_sd = self.get_fastest_sd_algorithm().get_optimal_parameters_dict()
        parameters_sd["SD-algorithm"] = self.get_fastest_sd_algorithm()._name
        return parameters_sd

    def reset(self):
        """
        reset to the initial state of the estimation object
        """
        super().reset()
        self._SDEstimator.reset()

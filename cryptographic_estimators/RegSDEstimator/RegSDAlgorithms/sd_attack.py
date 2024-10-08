# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from ...SDEstimator import SDEstimator
from ...SDEstimator.SDAlgorithms import BJMMdw, BJMMpdw, BJMMplus, MayOzerov, BothMay, Stern, Dumer


#FIX: Performance
class SDAttack(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of SDEstimator to solve the RegSDProblem.

        (for performance reasons for now only BJMM is estimated)

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class.
        """
        super(SDAttack, self).__init__(problem, **kwargs)
        self._name = "SD-Attack"
        n, k, w = self.problem.get_parameters()

        _ = kwargs.pop("bit_complexities", None)
        _ = kwargs.pop("nsolutions", None)
        _ = kwargs.pop("excluded_algorithms", None)
        self.SDEstimator = SDEstimator(n, k, w, bit_complexities=0
                                       , nsolutions=self.problem.nsolutions
                                       , excluded_algorithms=[BJMMdw, BJMMpdw, BJMMplus, MayOzerov, BothMay, Stern, Dumer]
                                       , **kwargs)

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        SD = self.SDEstimator.fastest_algorithm()
        return SD.time_complexity(), SD.memory_complexity()

    def get_optimal_parameters_dict(self):
        """Returns the optimal parameters dictionary."""
        SD = self.SDEstimator.fastest_algorithm()
        d = SD.get_optimal_parameters_dict()
        d["variant"] = SD._name
        return d

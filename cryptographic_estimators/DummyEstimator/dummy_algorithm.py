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


from ..base_algorithm import BaseAlgorithm
from .dummy_problem import DummyProblem


class DummyAlgorithm(BaseAlgorithm):
    def __init__(self, problem: DummyProblem, **kwargs):
        """Base class for Dummy algorithms complexity estimator.

        Args:
            problem (DummyProblem): DummyProblem object including all necessary parameters
            **kwargs: Additional keyword arguments
                memory_access: Specifies the memory access cost model
                    (default: 0, choices: 0 - constant, 1 - logarithmic,
                    2 - square-root, 3 - cube-root or deploy custom function
                    which takes as input the logarithm of the total memory usage)
                complexity_type: Complexity type to consider
                    (0: estimate, 1: tilde O complexity, default: 0)
        """
        super(DummyAlgorithm, self).__init__(problem, **kwargs)

    def __repr__(self):
        """
        NOTE: self._name must be instanciated via the child class
        """
        par1, par2 = self.problem.get_parameters()
        return f"{self._name} estimator for the dummy problem with parameters {par1} and {par2} "

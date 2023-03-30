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
from .pk_problem import PKProblem


class PKAlgorithm(BaseAlgorithm):
    def __init__(self, problem: PKProblem, **kwargs):
        """
        Base class for Permuted Kernel algorithms

        INPUT:

        - ``problem`` -- LEProblem object including all necessary parameters
        - ``cost_for_list_operation`` -- cost in Fq additions for one list operation in the SBC and KMP algorithms (default: n-m)
        - ``memory_for_list_element`` -- memory in Fq elements for one list element in the SBC and KMP algorithms (default: n-m)
        """
        super(PKAlgorithm, self).__init__(problem, **kwargs)
        n, m, _, _ = self.problem.get_parameters()
        self.cost_for_list_operation = kwargs.get("cost_for_list_operation", n - m)
        self.memory_for_list_element = kwargs.get("memory_for_list_element", n - m)

        if self.memory_for_list_element > self.cost_for_list_operation:
            raise ValueError("Cost per list element must be at least as high as its memory usage")

    def __repr__(self):
        return f"{self._name} estimator for the " + str(self.problem)

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


from ...base_algorithm import optimal_parameter
from ..dummy_algorithm import DUMMYAlgorithm
from ..dummy_problem import DUMMYProblem
from types import SimpleNamespace


class DUMMYAlgorithm1(DUMMYAlgorithm):
    """
    Construct an instance of DUMMYAlgorithm1 estimator

    Add reference to correponding paper here.

    INPUT:

    - ``problem`` -- an instance of the DUMMYProblem class
    """

    def __init__(self, problem: DUMMYProblem, **kwargs):
        self._name = "DUMMYAlgorithm1"
        super(DUMMYAlgorithm1, self).__init__(problem, **kwargs)
        n = self.problem.get_parameters()[0]
        self.set_parameter_ranges("h", 0, n)

    @optimal_parameter
    def h(self):
        return self._get_optimal_parameter("h")

    def _valid_choices(self):
        new_ranges = self._fix_ranges_for_already_set_parameters()
        for h in range(new_ranges["h"]["min"], new_ranges["h"]["max"], 2):
            yield {"h": h} 

    def _compute_time_complexity(self, parameters: dict):
        """
        Return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        par = SimpleNamespace(**parameters)
        n = self.problem.get_parameters()[0]
        return max(par.h, n - par.h)

    def _compute_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters

        """
        par = SimpleNamespace(**parameters)
        return par.h

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Return time complexity of DUMMYAlgorithm1's  for given set of parameters

        INPUT:
        -  ``parameters`` -- dictionary including parameters
        -  ``verbose_information`` -- if set to a dictionary `permutations` and `gauß` will be returned.
        """
        n = self.problem.get_parameters()[0]
        verbose_information["Lists Sizes"] = par.h
        return n, 0


    def __repr__(self):
        return "DUMMYAlgorithm1 estimator for " + str(self.problem)

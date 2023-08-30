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


import collections
from .scipy_model import ScipyModel
from ..sd_problem import SDProblem
from .workfactor_helper import representations_asymptotic, binomial_approximation, may_ozerov_near_neighbor_time


class BallCollisionScipyModel(ScipyModel):
    def __init__(self, par_names: list, problem: SDProblem, iterations, accuracy):
        """
        Optimization model for workfactor computation of Ball-Collision algorithm
        """
        super().__init__(par_names, problem, iterations, accuracy)

    def _build_model_and_set_constraints(self):
        self.L1 = lambda x: binomial_approximation(
            self.rate(x) / 2, x.p / 2) + binomial_approximation(x.l / 2, x.pl / 2)

        self.constraints = [
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p)},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: x.l - x.pl)},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: (
                1. - self.rate(x) - x.l) - (self.w(x) - x.p - x.pl))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.w(x) - x.p - x.pl)},
        ]

    def _memory(self, x):
        return self.L1(x)

    def _time_lists(self, x):
        return [max(self.L1(x), 2 * self.L1(x) - x.l)]

    def _time_perms(self, x):
        return max(0,
                   binomial_approximation(1., self.w(x))
                   - binomial_approximation(self.rate(x), x.p)
                   - binomial_approximation(x.l, x.pl)
                   - binomial_approximation(1 - self.rate(x) -
                                            x.l, self.w(x) - x.p - x.pl)
                   - self.nsolutions
                   )

    def _time(self, x):
        x = self.set_vars(*x)
        return self._time_perms(x) + max(self._time_lists(x))

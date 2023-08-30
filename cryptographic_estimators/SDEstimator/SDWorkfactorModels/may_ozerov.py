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


class MayOzerovScipyModel(ScipyModel):
    def __init__(self, par_names: list, problem: SDProblem, iterations, accuracy):
        """
        Optimization model for workfactor computation of May-Ozerov algorithm in depth 3 using May-Ozerov nearest neighbor search
        """
        super().__init__(par_names, problem, iterations, accuracy)

    def _build_model_and_set_constraints(self):
        self.r1 = lambda x: representations_asymptotic(
            x.p2, x.p1 - x.p2 / 2, self.rate(x) + x.l)
        self.r2 = lambda x: representations_asymptotic(
            x.p, x.p2 - x.p / 2, self.rate(x) + x.l)

        self.D1 = lambda x: binomial_approximation(self.rate(x) + x.l, x.p1)
        self.D2 = lambda x: binomial_approximation(self.rate(x) + x.l, x.p2)

        self.q2 = lambda x: self.D2(x) + self.r1(x) - 2 * self.D1(x)
        self.q3 = lambda x: self.D3(x) + self.r2(x) - 2 * self.D2(x)

        self.L1 = lambda x: binomial_approximation(
            (self.rate(x) + x.l) / 2, x.p1 / 2)
        self.L2 = lambda x: 2 * self.L1(x) - self.r1(x)
        self.L3 = lambda x: 2 * self.L2(x) - (x.l - self.r1(x)) + self.q2(x)

        self.constraints = [
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.r2(x) - self.r1(x))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.r2(x) - x.l)},

            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p - (x.p2 - x.p / 2))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p2 - (x.p1 - x.p2 / 2))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p1)},

            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: (1. - self.rate(x) - x.l) - (self.w(x) - x.p))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.w(x) - x.p)},
        ]

    def _memory(self, x):
        return max(self.L1(x), self.L2(x), self.L3(x))

    def _time_lists(self, x):
        time_list1 = max(self.L1(x), 2 * self.L1(x) - self.r1(x))
        time_list2 = max(self.L2(x), 2 * self.L2(x) - (x.l - self.r1(x)))
        time_list3 = may_ozerov_near_neighbor_time(
            self.L3(x), 1 - self.rate(x) - x.l, self.w(x) - x.p)

        return time_list1, time_list2, time_list3

    def _time_perms(self, x):
        return max(0,
                   binomial_approximation(1., self.w(x))
                   - binomial_approximation(self.rate(x) + x.l, x.p)
                   - binomial_approximation(1 -
                                            self.rate(x) - x.l, self.w(x) - x.p)
                   - self.nsolutions
                   )

    def _time(self, x):
        x = self.set_vars(*x)
        return self._time_perms(x) + max(self._time_lists(x))

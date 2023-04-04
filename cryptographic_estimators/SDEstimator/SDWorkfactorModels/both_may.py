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


class BothMayScipyModel(ScipyModel):
    def __init__(self, par_names: list, problem: SDProblem, iterations, accuracy):
        """
        Optimization model for workfactor computation of Both-May algorithm in depth 2 using May-Ozerov nearest neighbor search
        """
        super().__init__(par_names, problem, iterations, accuracy)

    def _build_model_and_set_constraints(self):
        self.r1 = lambda x: representations_asymptotic(
            x.p, x.p1 - x.p / 2, self.rate(x))
        self.c1 = lambda x: x.l - \
            representations_asymptotic(x.w2, x.w1 - x.w2 / 2, x.l)

        self.L1 = lambda x: binomial_approximation(
            (self.rate(x)) / 2, x.p1 / 2.0)
        self.L2 = lambda x: binomial_approximation(
            self.rate(x), x.p1) - x.l + binomial_approximation(x.l, x.w1)

        self.constraints = [
            {'type': 'eq', 'fun': self._inject_vars(
                lambda x: self.r1(x) - self.c1(x))},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: (
                1 - self.rate(x) - x.l) - (self.w(x) - x.p - x.w2))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: 1 - self.rate(x) - x.l)},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.w(x) - x.p - x.w2)},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: x.l - x.w2 - (x.w1 - x.w2 / 2))},
            {'type': 'ineq', 'fun': self._inject_vars(lambda x: x.l - x.w1)},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p - (x.p1 - x.p / 2))},
            {'type': 'ineq', 'fun': self._inject_vars(
                lambda x: self.rate(x) - x.p1)},

        ]

    def _memory(self, x):
        return max(self.L1(x), self.L2(x))

    def _time_lists(self, x):
        time_list1 = may_ozerov_near_neighbor_time(self.L1(x), x.l, x.w1)
        time_list2 = may_ozerov_near_neighbor_time(
            self.L2(x), 1 - self.rate(x) - x.l, self.w(x) - x.p - x.w2)

        return time_list1, time_list2

    def _time_perms(self, x):
        return max(0,
                   binomial_approximation(1, self.w(x))
                   - binomial_approximation(1 - self.rate(x) -
                                            x.l, self.w(x) - x.p - x.w2)
                   - binomial_approximation(self.rate(x), x.p)
                   - binomial_approximation(x.l, x.w2)
                   - self.nsolutions
                   )

    def _time(self, x):
        x = self.set_vars(*x)
        perms = self._time_perms(x)
        time_list1, time_list2 = self._time_lists(x)

        return perms + max(time_list1, time_list2)

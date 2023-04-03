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
from ..sd_estimator import SDProblem
from .workfactor_helper import list_of_random_tuples, wrap, binomial_approximation
import scipy.optimize as opt
from math import log2, inf


class ScipyModel:
    def __init__(self, var_names: list, problem: SDProblem, iterations, accuracy):
        self.parameters_names = [i for i in var_names if i != 'r']
        self.number_of_variables = len(self.parameters_names)
        self.accuracy = accuracy
        self.iterations = iterations

        n, k, w = problem.get_parameters()
        self.rate = lambda x: k / n
        self.w = lambda x: w / n

        self.set_vars = collections.namedtuple(
            'SciOptModel', ' '.join(self.parameters_names))

        if problem.nsolutions == max(0, problem.expected_number_solutions()):
            self.nsolutions = max(
                0, binomial_approximation(1, w / n) - (1 - k / n))
        else:
            self.nsolutions = log2(problem.nsolutions) / n

    def _inject_vars(self, f):
        return wrap(f, self.set_vars)

    def _set_bounds(self, parameters):
        if parameters is None:
            return [(0, 1)] * self.num_vars
        else:
            bounds = []
            for i in self.parameters_names:
                if i in parameters:
                    bounds += [(max(parameters[i] - self.accuracy, 0),
                                parameters[i] + self.accuracy)]
                else:
                    bounds += [(0, 1)]
            return bounds

    def _time(self, x):
        raise NotImplementedError

    def _memory(self, x):
        raise NotImplementedError

    def _optimize(self, parameters):
        start = list_of_random_tuples(0.001, 0.01, self.number_of_variables)
        bounds = self._set_bounds(parameters)

        result = opt.minimize(
            self._time,
            start,
            bounds=bounds,
            tol=self.accuracy,
            constraints=self.constraints,
            options={"maxiter": 150},
        )
        return result

    def _get_parameters(self, x):
        par = {}
        par_index = 0
        for par_name in self.parameters_names:
            par[par_name] = x[par_index]
            par_index += 1
        return par

    def get_time_memory_and_parameters(self, parameters=None):
        self._build_model_and_set_constraints()

        result = self._optimize(parameters)

        for _ in range(self.iterations - 1):
            tmp = self._optimize(parameters)
            if tmp.success and (tmp.fun < result.fun or not result.success):
                result = tmp

        x = self.set_vars(*result.x)
        if not result.success:
            return inf, inf, {}

        return self._time(x), self._memory(x), self._get_parameters(x)

    def _build_model_and_set_constraints(self):
        raise NotImplementedError

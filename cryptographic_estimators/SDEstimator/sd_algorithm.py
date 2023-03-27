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


from ..helper import ComplexityType
from ..base_algorithm import BaseAlgorithm, optimal_parameter
from ..SDEstimator.sd_helper import _optimize_m4ri
from .sd_problem import SDProblem
from math import log2, inf


class SDAlgorithm(BaseAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """
        Base class for Syndrome Decoding algorithms complexity estimator

        INPUT:

        - ``problem`` -- SDProblem object including all necessary parameters
        - ``var_ranges`` -- allow parameter optimization to adapt ranges if necessary (default: true)
        - ``hmap`` -- indicates if hashmap is being used for linear time sorting (default: true)

        """
        super(SDAlgorithm, self).__init__(problem, **kwargs)
        self._variable_parameter_ranges = kwargs.get("var_ranges", 1)
        self._hmap = kwargs.get("hmap", 1)
        self._adjust_radius = kwargs.get("adjust_radius", 10)
        self.workfactor_accuracy = kwargs.get("workfactor_accuracy", 1)
        self.scipy_model = None
        self.full_domain = kwargs.get("full_domain", False)
        self._current_minimum_for_early_abort = inf
        n, k, _  = self.problem.get_parameters()
        self.set_parameter_ranges("r", 0, n - k)

    @optimal_parameter
    def r(self):
        """
        Return the optimal parameter $r$ used in the optimization of the M4RI Gaussian elimination

        """

        if self._optimal_parameters.get("r") is None:
            n = self.problem.parameters["code length"]
            k = self.problem.parameters["code dimension"]
            if self.complexity_type == ComplexityType.ESTIMATE.value:
                return _optimize_m4ri(n, k, self.problem.memory_bound - log2(n - k))
            elif self.complexity_type == ComplexityType.TILDEO.value:
                return 0

        return self._optimal_parameters.get("r")

    def _are_parameters_invalid(self, parameters: dict):
        """
        returns `true` if `parameters` is an invalid parameter set
        """
        raise NotImplementedError

    def _find_optimal_parameters(self):
        """
        Enumerates over all valid parameter configurations withing the ranges
        of the optimization and saves the best result in `self._optimal_parameter`
        """
        _ = self.r()
        time = inf
        while True:
            stop = True
            for params in self._valid_choices():
                if self._are_parameters_invalid(params):
                    continue
                tmp_time, tmp_memory = self._time_and_memory_complexity(params)

                if self.bit_complexities:
                    tmp_memory = self.problem.to_bitcomplexity_memory(
                        tmp_memory)

                tmp_time += self.memory_access_cost(tmp_memory)

                if tmp_time < time and tmp_memory < self.problem.memory_bound:
                    time, memory = tmp_time, tmp_memory
                    self._current_minimum_for_early_abort = tmp_time

                    for i in params:
                        self._optimal_parameters[i] = params[i]

            if self._variable_parameter_ranges and len(self._optimal_parameters) > 1:
                stop = self._adjust_parameter_ranges()

            if stop:
                break
        self._current_minimum_for_early_abort = inf

    def _find_optimal_tilde_o_parameters(self):
        """
        Enumerates all valid parameter within the given ranges to find the optimal one asymptotically.
        Calls the C interface.
        """
        self._tilde_o_time_and_memory_complexity(self._optimal_parameters)

    def _adjust_parameter_ranges(self):
        """
        Readjust the boundaries of the `ESTIMATE` optimization routine if the
        optimization detects that it runs into one or more of the boundaries,
        these boundaries will be increased/decreased by `self._adjust_radius`.
        """
        kept_old_ranges = True
        r = self._adjust_radius

        for i in self._optimal_parameters_methods:
            ranges = self._parameter_ranges[i.__name__]
            current_min = ranges["min"]
            current_max = ranges["max"]
            val = i()
            if val > ranges["max"] - r:
                ranges["max"] += r
                ranges["min"] = max(0, min(val - r, ranges["min"] + r))
                kept_old_ranges = False

            if i() < ranges["min"] + r:
                ranges["min"] -= r
                ranges["min"] = max(0, ranges["min"])
                ranges["max"] = max(val + r, ranges["max"] - r)
                kept_old_ranges = False

            if current_min == ranges["min"] and current_max == ranges["max"]:
                kept_old_ranges = True
        return kept_old_ranges

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """
        Computes time and memory complexity for given parameters
        """
        raise NotImplementedError

    def _compute_time_complexity(self, parameters: dict):
        """
        Compute and return the time complexity either in the asymptotic case or for
        real parameters.

        INPUT:
        - ``parameters`` -- dictionary of parameters used for time complexity computation

        """
        return self._time_and_memory_complexity(parameters)[0]

    def _compute_tilde_o_time_complexity(self, parameters: dict):
        """
        Compute and return the time complexity of the algorithm for a given set of parameters

        INPUT:

        - ``parameters`` -- dictionary including the parameters
        """
        return self._tilde_o_time_and_memory_complexity(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        """
        Compute and return time complexity of the algorithm for given parameter set

        INPUT:
        - ``parameters`` -- dictionary of parameters used for time complexity computation

        """
        return self._time_and_memory_complexity(parameters)[1]

    def _compute_tilde_o_memory_complexity(self, parameters: dict):
        """
        Compute and return time complexity the algorithm for given parameter set

        INPUT:
        - ``parameters`` -- dictionary of parameters used for time complexity computation

        """
        return self._tilde_o_time_and_memory_complexity(parameters)[1]

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        Computes and returns time and memory complexity of the algorithm for given parameter set

        INPUT:
        - ``parameters`` -- dictionary of parameters used for time complexity computation

        """
        if self.scipy_model is None:
            raise NotImplementedError(
                "For " + self._name + " TildeO complexity is not yet implemented")
        model = self.scipy_model(self.parameter_names(
        ), self.problem, iterations=self.workfactor_accuracy*10, accuracy=1e-7)
        wf_time, wf_memory, par = model.get_time_memory_and_parameters(
            parameters=parameters)
        self._optimal_parameters.update(par)
        n, _, _ = self.problem.get_parameters()
        return wf_time*n, wf_memory*n

    def _get_verbose_information(self):
        """
        returns a dictionary containing
            {
                CONSTRAINTS,
                PERMUTATIONS,
                TREE,
                GAUSS,
                REPRESENTATIONS,
                LISTS
            }
        """
        verb = dict()
        _ = self._time_and_memory_complexity(
            self.optimal_parameters(), verbose_information=verb)
        return verb

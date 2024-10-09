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

from ...base_algorithm import optimal_parameter
from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from ..regsd_helper import r_int
from math import log2, ceil, inf


class CCJ(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of CCJ estimator from [CCJ23]_.

        (concrete formulas taken from [ES23]_)

        Args:
            problem (RegSDProblem): an instance of the RegSDProblem class

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import CCJ
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = CCJ(RegSDProblem(n=100,k=50,w=10))
            >>> A
            CCJ estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(CCJ, self).__init__(problem, **kwargs)
        n, k, w = self.problem.get_parameters()
        self._name = "CCJ"
        self.set_parameter_ranges("ell", 0, min(k + w, n))

    @optimal_parameter
    def ell(self):
        """Return the optimal parameter ell used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import CCJ
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = CCJ(RegSDProblem(n=100,k=50,w=10))
            >>> A.ell()
            10
        """
        return self._get_optimal_parameter("ell")

    def _valid_choices(self):
        """Generator yielding new sets of valid parameters.
    
        Yields new sets of valid parameters based on the `_parameter_ranges` and
        already set parameters in `_optimal_parameters`.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        n, k, w = self.problem.get_parameters()

        # we first find a suitable range for the optimal value of ell
        k_tilde_approx = k - (1 - k / n) / (1 - w / n) * w
        L1_approx = log2(n / w) * (w * k_tilde_approx / (2 * n))
        ell_approx = L1_approx
        ell_min = ceil(ell_approx * 0.75)
        ell_max = min(r_int(ell_approx * 1.5), n - k)
        for ell in range(max(new_ranges["ell"]["min"], ell_min), min(ell_max, new_ranges["ell"]["max"] + 1)):
            indices = {"ell": ell}
            if self._are_parameters_invalid(indices):
                continue
            yield indices

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()
        ell = parameters["ell"]
        k_tilde = k - (1 - (ell + k) / n) / (1 - w / n) * w
        if ell > (n - k_tilde):
            return inf, inf

        # cost of one iteration
        L = (n / w) ** (w * (k_tilde + ell) / (2 * n))
        num_coll = L ** 2 * 2 ** -ell

        # overall cost
        time = log2((n - k_tilde) ** 2 + (2 * L + num_coll))

        return time, log2(L)


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
from math import log2, comb as binomial, ceil, floor, inf
from types import SimpleNamespace


class RegularISDRep(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of RegularISD-Enum estimator in depth 3 from [ES23]_.

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class

        Examples:
        >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDRep
        >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
        >>> A = RegularISDRep(RegSDProblem(n=100,k=50,w=10))
        >>> A
        RegularISD-Rep estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(RegularISDRep, self).__init__(problem, **kwargs)
        self._name = "RegularISD-Rep"
        n, k, w = self.problem.get_parameters()

        self.set_parameter_ranges("p", 0, 40)
        self.set_parameter_ranges("ell", 0, n - k)
        self.set_parameter_ranges("eps_x", 0, 32)
        self.set_parameter_ranges("eps_y", 0, 20)

    @optimal_parameter
    def p(self):
        """Return the optimal parameter p used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDRep
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDRep(RegSDProblem(n=300,k=150,w=30))
            >>> A.p()
            8
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def ell(self):
        """Return the optimal parameter ell used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDRep
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDRep(RegSDProblem(n=300,k=150,w=30))
            >>> A.ell()
            22
        """
        return self._get_optimal_parameter("ell")

    @optimal_parameter
    def eps_x(self):
        """Return the optimal parameter eps_x used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDRep
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDRep(RegSDProblem(n=300,k=150,w=30))
            >>> A.eps_x()
            0
        """
        return self._get_optimal_parameter("eps_x")

    @optimal_parameter
    def eps_y(self):
        """Return the optimal parameter eps_y used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDRep
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDRep(RegSDProblem(n=300,k=150,w=30))
            >>> A.eps_y()
            0
        """
        return self._get_optimal_parameter("eps_y")

    def _are_parameters_invalid(self, parameters: dict):
        """Return if the parameter set `parameters` is invalid."""
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k_prime = k - w
        v = (k_prime + par.ell) / w
        b = n / w
        if w / 2 - par.p / 2 < par.eps_x / 2 or w / 2 - par.p / 4 - par.eps_x / 2 < par.eps_y / 2 \
                or w / 2 < par.p / 2 or v == 0 or v >= b:
            return True
        return False

    def _valid_choices(self):
        """Generator yielding new sets of valid parameters.
    
        Based on the `_parameter_ranges` and already set parameters in `_optimal_parameters`.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        n, k, w = self.problem.get_parameters()
        k_prime = k - w
        for p in range(new_ranges["p"]["min"], min(w // 2, new_ranges["p"]["max"])+1, 8):
            for eps_x in range(new_ranges["eps_x"]["min"], new_ranges["eps_x"]["max"]+1, 4):
                p_x = p/2 + eps_x
                for eps_y in range(new_ranges["eps_y"]["min"], new_ranges["eps_y"]["max"] + 1):
                    p_y = p_x / 2 + eps_y
                    L1 = log2(max(binomial(r_int(w / 2), int(p_y / 2)) * k_prime ** (p_y // 2), 1))
                    ell_approx = r_int(2 * L1)
                    ell_min = r_int(ell_approx * 0.5)
                    ell_max = r_int(ell_approx * 1.5)
                    for ell in range(max(new_ranges["ell"]["min"], ell_min), min(ell_max, new_ranges["ell"]["max"])):
                        indices = {"p": p, "ell": ell, "eps_x": eps_x, "eps_y": eps_y}
                        if self._are_parameters_invalid(indices):
                            continue
                        yield indices

    def _compute_time_and_memory_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.
        """
        n, k, w = self.problem.get_parameters()
        p, ell, eps_x, eps_y= list(parameters.values())
        
        k_prime = k-w
        v = (k_prime + ell) / w
        b=n//w

        p_x = p//2 + eps_x
        p_y = p_x//2 + eps_y
        # Num reps
        R_x = (log2(binomial(int(p / 2), int(p / 4))) + log2(binomial(int((w-p)/ 2), int(eps_x / 2))) + log2(v) * (eps_x / 2)) * 2
        R_y = (log2(binomial(int(p_x / 2), int(p_x / 4))) + log2(binomial(int((w- p_x)/2), int(eps_y // 2))) + log2(v) * (
                    eps_y // 2)) * 2

        ell_x = floor(R_x)
        ell_y = floor(R_y)

        if ell_y > ell_x:
            return inf, inf

        # success probability
        p_iter = log2(binomial(floor(w / 2), r_int(p / 2))) + log2(binomial(ceil(w / 2), r_int(p / 2))) + log2(
            v / b) * p + log2(1 - v / b) * (w - p)

        L1 = log2(binomial(r_int(w / 2), int(p_y / 2))) + log2(v) * (p_y / 2)  # list size, first level (initial lists)

        L_y1 = L1 * 2 - ell_y
        N_y = L_y1 * 2 - (ell_x - ell_y)

        L_x1 = log2(binomial(r_int(w / 2), p_x // 2)) * 2 + log2(v) * p_x - ell_x
        N_x = L_x1 * 2 - (ell - ell_x)

        # cost of one iteration
        T_gauss = log2(n - k_prime) * 2
        T_iter = max(T_gauss, 3 + L1, 2 + L_y1, 1 + N_y, 1 + L_x1, N_x)

        # overall cost
        time = T_iter - p_iter
        memory = max(L1, L_y1,L_x1)
        return time, memory


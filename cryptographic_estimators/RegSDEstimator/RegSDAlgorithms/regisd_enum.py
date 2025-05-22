# ****************************************************************************
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# ****************************************************************************


from ...base_algorithm import optimal_parameter
from ..regsd_algorithm import RegSDAlgorithm
from ..regsd_problem import RegSDProblem
from ..regsd_helper import r_int
from math import log2, comb as binomial, ceil, floor
from types import SimpleNamespace

class RegularISDEnum(RegSDAlgorithm):
    def __init__(self, problem: RegSDProblem, **kwargs):
        """Construct an instance of RegularISD-Enum estimator from [ES23]_.

        Args:
            problem (RegSDProblem): An instance of the RegSDProblem class

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDEnum
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDEnum(RegSDProblem(n=100,k=50,w=10))
            >>> A
            RegularISD-Enum estimator for the RegSDProblem with parameters (n, k, w) = (100, 50, 10)
        """
        super(RegularISDEnum, self).__init__(problem, **kwargs)
        n, k, w = self.problem.get_parameters()
        self._name = "RegularISD-Enum"
        self.set_parameter_ranges("p", 0, 30)
        self.set_parameter_ranges("ell", 0, n-k)

    @optimal_parameter
    def p(self):
        """Return the optimal parameter p used in the algorithm optimization.
    
        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDEnum
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDEnum(RegSDProblem(n=100,k=50,w=10))
            >>> A.p()
            4
        """
        return self._get_optimal_parameter("p")

    @optimal_parameter
    def ell(self):
        """Return the optimal parameter p used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.RegSDEstimator.RegSDAlgorithms import RegularISDEnum
            >>> from cryptographic_estimators.RegSDEstimator import RegSDProblem
            >>> A = RegularISDEnum(RegSDProblem(n=100,k=50,w=10))
            >>> A.ell()
            4
        """
        return self._get_optimal_parameter("ell")

    def _are_parameters_invalid(self, parameters: dict):
        """Return if the parameter set `parameters` is invalid."""
        n, k, w = self.problem.get_parameters()
        par = SimpleNamespace(**parameters)
        k_prime = k - w
        v = (k_prime + par.ell) / w
        b = n/w
        if w / 2 < par.p / 2 or v / b >= 1:
            return True
        return False
    def _valid_choices(self):
        """Generator yielding new sets of valid parameters.
    
        Based on the `_parameter_ranges` and already set parameters in `_optimal_parameters`.
        """
        new_ranges = self._fix_ranges_for_already_set_parameters()

        n, k, w = self.problem.get_parameters()
        k_prime = k - w
        for p in range(new_ranges["p"]["min"], min(w // 2, new_ranges["p"]["max"]+1), 2):
            ell_approx = max(1, log2(binomial(r_int(w / 2), p // 2)) +log2(k_prime / w) * (p / 2))
            ell_min = r_int(ell_approx * 0.5)
            ell_max = min(r_int(ell_approx * 1.5), n - k_prime)

            for ell in range(max(new_ranges["ell"]["min"],ell_min), min(ell_max, new_ranges["ell"]["max"]+1)):
                indices = {"p": p, "ell": ell}
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
        p = parameters["p"]
        b = n//w

        # add parity-checks
        k_prime = k - w

        v = (k_prime + ell) / w  # number of coordinates per block

        # success probability
        p_iter = log2(binomial(floor(w / 2), r_int(p / 2))) + log2(binomial(ceil(w / 2), r_int(p / 2))) + log2(
            v / b) * p + log2(1 - v / b) * (w - p)

        # cost of one iteration
        L = log2(binomial(r_int(w / 2), p // 2)) + log2(v) * (p / 2)
        T_iter = max(log2(n - k_prime) * 2, 1 + L, L * 2 - ell)

        # overall cost
        time = T_iter - p_iter
        return time, L

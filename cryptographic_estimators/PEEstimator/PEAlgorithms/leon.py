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

from ...PEEstimator.pe_algorithm import PEAlgorithm
from ...PEEstimator.pe_problem import PEProblem
from ...base_algorithm import optimal_parameter
from ..pe_helper import gv_distance, number_of_weight_d_codewords
from ...SDFqEstimator.sdfq_estimator import SDFqEstimator
from math import log, ceil, log2


class Leon(PEAlgorithm):
    def __init__(self, problem: PEProblem, **kwargs):
        """Complexity estimate of Leon's algorithm [Leo82]_.

        Estimates are adapted versions of the scripts derived in [Beu20]_ with the code accessible at
        https://github.com/WardBeullens/LESS_Attack

        Args:
            problem (PEProblem): PEProblem object including all necessary parameters
            codewords_needed_for_success: Number of low word codewords needed for success (default = 100)
            sd_parameters: Dictionary of parameters for SDFqEstimator used as a subroutine (default: {})

        Examples:
            >>> from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            >>> from cryptographic_estimators.PEEstimator import PEProblem
            >>> Leon(PEProblem(n=100,k=50,q=3))
            Leon estimator for permutation equivalence problem with (n,k,q) = (100,50,3)
        """
        super().__init__(problem, **kwargs)
        self._name = "Leon"
        n, k, q, _ = self.problem.get_parameters()
        self._codewords_needed_for_success = kwargs.get("codewords_needed_for_success",
                                                        min(100, int(number_of_weight_d_codewords(n, k, q,
                                                                                                  gv_distance(n, k,
                                                                                                              q) + 3))))
        self.set_parameter_ranges('w', 0, n)

        self.SDFqEstimator = None

        self._SDFqEstimator_parameters = kwargs.get("sd_parameters", {})
        self._SDFqEstimator_parameters.pop("bit_complexities", None)
        self._SDFqEstimator_parameters.pop("nsolutions", None)
        self._SDFqEstimator_parameters.pop("memory_bound", None)

    @optimal_parameter
    def w(self):
        """Return the optimal parameter w used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.PEEstimator.PEAlgorithms import Leon
            >>> from cryptographic_estimators.PEEstimator import PEProblem
            >>> A = Leon(PEProblem(n=100,k=50,q=3))
            >>> A.w()
            20
        """
        n, k, q, _ = self.problem.get_parameters()
        d = gv_distance(n, k, q)

        while number_of_weight_d_codewords(n, k, q, d) < self._codewords_needed_for_success and d < n - k:
            d += 1
        return d

    def _compute_time_complexity(self, parameters: dict):
        n, k, q, _ = self.problem.get_parameters()
        w = parameters["w"]
        N = number_of_weight_d_codewords(n, k, q, w)
        self.SDFqEstimator = SDFqEstimator(n=n, k=k, w=w, q=q, nsolutions=0, memory_bound=self.problem.memory_bound,
                                           bit_complexities=0, **self._SDFqEstimator_parameters)
        c_isd = self.SDFqEstimator.fastest_algorithm().time_complexity()
        return c_isd + log2(ceil(2 * (0.57 + log2(max(N, 1)))))

    def _compute_memory_complexity(self, parameters: dict):
        return self.SDFqEstimator.fastest_algorithm().memory_complexity()

    def __repr__(self):
        rep = "Leon estimator for " + str(self.problem)
        return rep

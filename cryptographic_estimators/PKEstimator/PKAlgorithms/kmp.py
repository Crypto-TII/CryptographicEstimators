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

from ..pk_algorithm import PKAlgorithm
from ..pk_problem import PKProblem
from ..pk_constants import *
from ...base_algorithm import optimal_parameter
from math import log2, factorial


class KMP(PKAlgorithm):
    def __init__(self, problem: PKProblem, **kwargs):
        """Complexity estimate of the KMP algorithm.

        Originally proposed in [KMP19]_. The estimates are adapted versions of the code accompanying [SBC22]_, original
        code is accessible at https://github.com/secomms/pkpattack

        Examples:
            >>> from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP
            >>> from cryptographic_estimators.PKEstimator import PKProblem
            >>> KMP(PKProblem(n=100,m=50,q=31,ell=2))
            KMP estimator for the permuted kernel problem with (n,m,q,ell) = (100,50,31,2)
        """
        super().__init__(problem, **kwargs)
        self._name = "KMP"
        _, m, _, _ = self.problem.get_parameters()

        self.set_parameter_ranges("u", 0, m)

    @optimal_parameter
    def u(self):
        """Return the optimal parameter u used in the algorithm optimization.

        Examples:
            >>> from cryptographic_estimators.PKEstimator.PKAlgorithms import KMP
            >>> from cryptographic_estimators.PKEstimator import PKProblem
            >>> A = KMP(PKProblem(n=100,m=50,q=31,ell=2))
            >>> A.u()
            24
        """
        return self._get_optimal_parameter("u")

    def _compute_time_and_memory(self, parameters: dict, verbose_information=None):
        """Computes the time and memory complexity of the KMP algorithm.
    
        Calculates the number of Fq additions and Fq elements for time and memory complexity respectively.
    
        Args:
            parameters (dict): Dictionary including parameters.
            verbose_information: If set to a dictionary, L1, L1, and final_list will be returned.
        """
        u = parameters["u"]
        n, m, q, ell = self.problem.get_parameters()
        u1 = int((n - m + u) / 2)
        u2 = n - m + u - u1

        L1 = factorial(n) // factorial(n - u1)
        L2 = factorial(n) // factorial(n - u2)
        num_coll = factorial(n) * factorial(n) // factorial(n - u1) \
                   // factorial(n - u2) * q ** (ell * (n - m - u1 - u2))

        time = log2(max(L1 + L2 + num_coll, 1)) + log2(max(self.cost_for_list_operation, 1))
        memory = log2(max(L1 + L2, 1)) + log2(max(self.memory_for_list_element, 1))

        if verbose_information is not None:
            verbose_information[VerboseInformation.KMP_L1.value] = log2(max(L1, 1))
            verbose_information[VerboseInformation.KMP_L2.value] = log2(max(L2, 1))
            verbose_information[VerboseInformation.KMP_FINAL_LIST.value] = log2(max(num_coll, 1))

        return time, memory

    def _compute_time_complexity(self, parameters: dict):
        return self._compute_time_and_memory(parameters)[0]

    def _compute_memory_complexity(self, parameters: dict):
        return self._compute_time_and_memory(parameters)[1]

    def _get_verbose_information(self):
        """Returns a dictionary containing additional algorithm information."""
        verb = {}
        _ = self._compute_time_and_memory(self.optimal_parameters(), verbose_information=verb)
        return verb

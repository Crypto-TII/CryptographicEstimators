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

from ..mr_constants import MR_SERIES_PRECISION
from math import log2, ceil, inf
from math import comb as binomial
from ..mr_constants import MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS, \
    MR_NUMBER_OF_COEFFICIENTS_TO_GUESS, \
    MR_REDUCED_NUMBER_OF_COLUMNS, \
    MR_LINEAR_VARIABLES_DEGREE
from ...MREstimator.mr_algorithm import MRAlgorithm
from ...MREstimator.mr_problem import MRProblem
from ...MREstimator.mr_helper import _bw_complexity_, determinantal_series
from ...MREstimator.mr_helper import predict_solving_degree, linear_monomial_series
from ...base_algorithm import optimal_parameter


def support_minors_series(q, m, n, k, r, precision=None):
    """Return the Support-Minors series with field equations."""
    return determinantal_series(q, m, n, k, r, dc=1, precision=precision)


class SupportMinors(MRAlgorithm):
    def __init__(self, problem: MRProblem, **kwargs):
        """Construct an instance of SupportMinors estimator with affine field equations [ABCPSV]_.

        Args:
            problem (MRProblem): An instance of the MRProblem class
            **kwargs: Additional keyword arguments
                w (int): Linear algebra constant for hybrid reduction (default: 3)
                theta (int): Exponent of the conversion factor (default: 2)

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> SM
            SupportMinors estimator for the MinRank problem with (q, m, n, k, r) = (7, 9, 10, 15, 4)
        """
        super(SupportMinors, self).__init__(problem, **kwargs)

        q, m, n, k, r = self.problem.get_parameters()
        self.set_parameter_ranges('a', 0, min(n - r, ceil(k / m) - 1))
        self.set_parameter_ranges('lv', 0, min(r, k) - 1)
        self.set_parameter_ranges('b', 1, min(n, m))
        self.set_parameter_ranges('nprime', r + 1, n)
        self._name = "SupportMinors"

    @optimal_parameter
    def a(self):
        """Return the optimal `a`, i.e. number of vectors to guess in the kernel of the low-rank matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> SM.a()
            1

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.a()
            5
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS)

    @optimal_parameter
    def lv(self):
        """Return the optimal `lv`, i.e. number of entries to guess in the solution.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> SM.lv()
            0

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.lv()
            0
        """
        return self._get_optimal_parameter(MR_NUMBER_OF_COEFFICIENTS_TO_GUESS)

    @optimal_parameter
    def b(self):
        """Return the optimal `b`, i.e. the degree of the linear variables in the Macaulay matrix.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> SM.b()
            1

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.b()
            1
        """
        return self._get_optimal_parameter(MR_LINEAR_VARIABLES_DEGREE)

    @optimal_parameter
    def nprime(self):
        """Return the optimal `nprime`, i.e. the number of columns to be selected.

        Examples:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=7, m=9, n=10, k=15, r=4))
            >>> SM.nprime()
            8

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.nprime()
            8
        """
        return self._get_optimal_parameter(MR_REDUCED_NUMBER_OF_COLUMNS)

    def _dimension(self, q, n, K, r, b):
        """Return the number of columns after applying the affine field equations."""
        return binomial(n, r) * linear_monomial_series(q, K - 1, b)

    def _solving_degree(self, q, m, n, k, r):
        series = support_minors_series(q, m, n, k, r)
        max_b = self.parameter_ranges['b']['max']
        # A positive series through max_b rules out every allowed degree.
        if max_b < MR_SERIES_PRECISION and all(series[b] > 0 for b in range(max_b + 1)):
            return inf
        return predict_solving_degree(series, MR_SERIES_PRECISION)

    def _valid_choices(self):
        """Enumerate hybrid guesses and columns, using the predicted solving degree."""
        ranges = self._fix_ranges_for_already_set_parameters()
        q, m, _, _, r = self.problem.get_parameters()
        for a in range(ranges['a']['min'], ranges['a']['max'] + 1):
            for lv in range(ranges['lv']['min'], ranges['lv']['max'] + 1):
                if self._are_hybrid_parameters_invalid(a, lv):
                    continue
                _, _, n_reduced, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
                for nprime in range(ranges['nprime']['min'], min(n_reduced, ranges['nprime']['max']) + 1):
                    b = self._solving_degree(q, m, nprime, k_reduced, r)
                    if not ranges['b']['min'] <= b <= ranges['b']['max']:
                        continue
                    yield {'a': a, 'lv': lv, 'b': b, 'nprime': nprime}

    def _are_parameters_invalid(self, parameters):
        """Check the hybrid domain and the predicted solving degree."""
        a, lv = parameters['a'], parameters['lv']
        if self._are_hybrid_parameters_invalid(a, lv):
            return True
        q, m, n_reduced, k_reduced, r = self.get_problem_parameters_reduced(a, lv)
        nprime = parameters['nprime']
        if not r < nprime <= n_reduced:
            return True
        b = self._solving_degree(q, m, nprime, k_reduced, r)
        return parameters['b'] != b or not self.parameter_ranges['b']['min'] <= b <= self.parameter_ranges['b']['max']

    def _sm_time_complexity_helper_(self, q: int, K: int, r: int, nprime: int, b: int):
        """Return the Wiedemann cost with affine field equations."""
        ncols = self._dimension(q, nprime, K, r, b)
        return _bw_complexity_(row_density=K * (r + 1), ncols=ncols)

    def _sm_memory_complexity_helper_(self, q: int, K: int, r: int, nprime: int, b: int):
        """Return the memory needed for two Wiedemann vectors."""
        return log2(2 * self._dimension(q, nprime, K, r, b))

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.time_complexity()
            144.5902334156004

            >>> SM = SupportMinors(MRProblem(q=2, m=10, n=10, k=70, r=4))
            >>> SM.time_complexity()
            66.38320555241827
        """
        if self._are_parameters_invalid(parameters):
            return inf
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]

        q, m, n, k, r = self.problem.get_parameters()
        time = self.hybridization_factor(a, lv)
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        reduction_cost = self.hybrid_reduction_cost(a, lv)
        time_complexity = self._sm_time_complexity_helper_(q, k_reduced + 1, r, nprime, b)
        time += self._log2_sum(time_complexity, reduction_cost)
        return time

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.
    
        Args:
            parameters (dict): Dictionary including the parameters.

        Tests:
            >>> from cryptographic_estimators.MREstimator.MRAlgorithms.support_minors import SupportMinors
            >>> from cryptographic_estimators.MREstimator.mr_problem import MRProblem
            >>> SM = SupportMinors(MRProblem(q=16, m=15, n=15, k=78, r=6))
            >>> SM.memory_complexity()
            16.11756193939414
        """

        if self._are_parameters_invalid(parameters):
            return inf
        a = parameters[MR_NUMBER_OF_KERNEL_VECTORS_TO_GUESS]
        lv = parameters[MR_NUMBER_OF_COEFFICIENTS_TO_GUESS]
        nprime = parameters[MR_REDUCED_NUMBER_OF_COLUMNS]
        b = parameters[MR_LINEAR_VARIABLES_DEGREE]

        q, m, n, k, r = self.problem.get_parameters()
        _, _, _, k_reduced, _ = self.get_problem_parameters_reduced(a, lv)
        memory_store_matrices = log2((k + 1) * m * n)
        memory_attack = self._sm_memory_complexity_helper_(q, k_reduced + 1, r, nprime, b)
        memory = max(memory_store_matrices, memory_attack)
        return memory

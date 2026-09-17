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


from math import log2
from ..ranksd_algorithm import RankSDAlgorithm
from ..ranksd_constants import RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS
from ..ranksd_problem import RankSDProblem
from ...base_algorithm import optimal_parameter


class AnnulatorPolynomial(RankSDAlgorithm):
    """Construct an instance of HybridLinearization estimator.

       This algorithm tries to solve a given instance by randomly generating new equations from
       the orginal equations and attempting to solve them by linearization [GRS16]_

       Args:
           problem (RankSDProblem): An instance of the RankSDProblem class.
           **kwargs: Additional keyword arguments.
               w (int): Linear algebra constant (default: 3).
               theta (int): Exponent of the conversion factor (default: 2).

       Examples:
           >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.annulator_polynomial import AnnulatorPolynomial
           >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
           >>> HL = AnnulatorPolynomial(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
           >>> HL
           AnnulatorPolynomial estimator for the Rank Syndrome Decoding problem with (q, m, n, k, r) = (2, 127, 118, 48, 7)
    """

    def __init__(self, problem: RankSDProblem, **kwargs):
        super(AnnulatorPolynomial, self).__init__(problem, **kwargs)
        _, _, _, k, _ = self.problem.get_parameters()

        self.set_parameter_ranges(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS, 1, k)
        self.on_base_field = False
        self._name = "AnnulatorPolynomial"

    @optimal_parameter
    def t(self):
        """Return the optimal `t`, i.e. the number of zero entries expected to have a random element of the support.

           Examples:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.annulator_polynomial import AnnulatorPolynomial
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> AP = AnnulatorPolynomial(RankSDProblem(q=2,m=31,n=33,k=15,r=10))
               >>> AP.t()
               15

          Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.annulator_polynomial import AnnulatorPolynomial
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> AP = AnnulatorPolynomial(RankSDProblem(q=2,m=37,n=41,k=18,r=13))
               >>> AP.t()
               18
        """
        return self._get_optimal_parameter(RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS)

    def _compute_time_complexity(self, parameters: dict):
        """Return the time complexity of the algorithm for a given set of parameters.

           Args:
              parameters (dict): Dictionary including the parameters.

           Tests:
              >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.annulator_polynomial import AnnulatorPolynomial
              >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
              >>> AP = AnnulatorPolynomial(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
              >>> AP.time_complexity()
              312.1543216418806
        """

        q, _, _, k, r = self.problem.get_parameters()
        self.problem.set_operations_on_base_field(self.on_base_field)
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        time_complexity = self._w * (log2(r) + log2(k)) + r * t * log2(q)
        return time_complexity

    def _compute_memory_complexity(self, parameters: dict):
        """Return the memory complexity of the algorithm for a given set of parameters.

           Args:
               parameters (dict): Dictionary including the parameters.

           Tests:
               >>> from cryptographic_estimators.RankSDEstimator.RankSDAlgorithms.annulator_polynomial import AnnulatorPolynomial
               >>> from cryptographic_estimators.RankSDEstimator.ranksd_problem import RankSDProblem
               >>> AP = AnnulatorPolynomial(RankSDProblem(q=2,m=127,n=118,k=48,r=7))
               >>> AP.memory_complexity()
               19.59624618312637
        """
        _, _, n, k, r = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        n_rows = n - t
        n_columns = ((r + 1) * (k + 1 - t) - 1)
        return self.__compute_memory_complexity_helper__(n_rows, n_columns, self.on_base_field)

    def _are_parameters_invalid(self, parameters: dict):
        """Specifies constraints on the parameters.
        """
        _, _, n, k, r = self.problem.get_parameters()
        t = parameters[RANKSD_NUMBER_OF_ENTRIES_X_TO_GUESS]
        b = (n - t) < ((r + 1) * (k + 1 - t) - 1)
        return b

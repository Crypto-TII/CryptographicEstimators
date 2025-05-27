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

from ...SDFqEstimator.sdfq_algorithm import SDFqAlgorithm
from ...SDFqEstimator.sdfq_problem import SDFqProblem
from ...SDFqEstimator.sdfq_helper import _mem_matrix, binom, log2
from ..sdfq_constants import *


class Prange(SDFqAlgorithm):
    def __init__(self, problem: SDFqProblem, **kwargs):
        """Construct an instance of Prange's estimator [Pra62]_.

        Expected weight distribution:

            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |                w               |              0                |
            +--------------------------------+-------------------------------+

        Args:
            problem (SDFqProblem): SDProblem object including all necessary parameters.

        Examples:
            >>> from cryptographic_estimators.SDFqEstimator.SDFqAlgorithms import Prange
            >>> from cryptographic_estimators.SDFqEstimator import SDFqProblem
            >>> Prange(SDFqProblem(n=100,k=50,w=10,q=3))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 3
        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Returns the time complexity of Prange's algorithm for the given set of parameters.
    
        Args:
            parameters (dict): A dictionary including the parameters.
            verbose_information (dict, optional): If set, 'permutations' and 'gauß' will be returned.
        """

        n, k, w, _ = self.problem.get_parameters()
        solutions = self.problem.nsolutions

        memory = log2(_mem_matrix(n, k, 0)) + log2(n)

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(k*k)
        time = Tp + Tg + log2(n)

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg
        
        return time, memory

    def __repr__(self):
        rep = "Prange estimator for " + str(self.problem)
        return rep

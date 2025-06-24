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


from ...SDEstimator.sd_algorithm import SDAlgorithm
from ...SDEstimator.sd_problem import SDProblem
from ...SDEstimator.sd_helper import (
    _gaussian_elimination_complexity,
    _mem_matrix,
    binom,
    log2,
)
from ..sd_constants import *
from ..SDWorkfactorModels.prange import PrangeScipyModel


class Prange(SDAlgorithm):
    def __init__(self, problem: SDProblem, **kwargs):
        """Construct an instance of Prange's estimator [Pra62]_.

        Expected weight distribution::

            +--------------------------------+-------------------------------+
            | <----------+ n - k +---------> | <----------+ k +------------> |
            |                w               |              0                |
            +--------------------------------+-------------------------------+

        Args:
            problem (SDProblem): An SDProblem object including all necessary parameters.

        Examples:
            >>> from cryptographic_estimators.SDEstimator.SDAlgorithms import Prange
            >>> from cryptographic_estimators.SDEstimator import SDProblem
            >>> Prange(SDProblem(n=100, k=50, w=10))
            Prange estimator for syndrome decoding problem with (n,k,w) = (100,50,10) over Finite Field of size 2
        """
        self._name = "Prange"
        super(Prange, self).__init__(problem, **kwargs)
        self.scipy_model = PrangeScipyModel

    def _time_and_memory_complexity(self, parameters: dict, verbose_information=None):
        """Return time complexity of Prange's algorithm for given set of parameters.

        Args:
            parameters (dict): Dictionary including parameters.
            verbose_information (dict, optional): If set, `permutations` and `gauß` will be returned.

        Returns:
            The time complexity of Prange's algorithm.
        """
        n, k, w = self.problem.get_parameters()

        solutions = self.problem.nsolutions

        r = parameters["r"]
        memory = log2(_mem_matrix(n, k, r))

        Tp = max(log2(binom(n, w)) - log2(binom(n - k, w)) - solutions, 0)
        Tg = log2(_gaussian_elimination_complexity(n, k, r))
        time = Tp + Tg

        if verbose_information is not None:
            verbose_information[VerboseInformation.PERMUTATIONS.value] = Tp
            verbose_information[VerboseInformation.GAUSS.value] = Tg

        return time, memory

    def __repr__(self):
        rep = "Prange estimator for " + str(self.problem)
        return rep

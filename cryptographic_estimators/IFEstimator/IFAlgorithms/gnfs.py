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


from ..if_algorithm import IFAlgorithm
from ..if_problem import IFProblem
from ..if_constants import *
from ..if_helper import *
from math import exp, log


class GNFS(IFAlgorithm):

    def __init__(self, problem: IFProblem, **kwargs):
        """
        Construct an instance of IFAlgorithm1 estimator
        The estimates as per [Len17]_  Sec. 5.5.4 https://eprint.iacr.org/2017/1087.pdf

        Args:
            problem (IFProblem): An instance of the IFProblem class containing the parameters for the problem.

        Examples:
            >>> from cryptographic_estimators.IFEstimator.IFAlgorithms import GNFS
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> GNFS(IFProblem(n=4096))
            General Number Field Sieve algorithm for Integer Factoring Problem with parameter n = 4096
        """
        self._name = "GNFS"
        super(GNFS, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, correctingfactor=True):
        """
        Return the time complexity of the General Number Field Sieve algorithm for a given set of parameters

        Args:
            parameters: dictionary including the parameters
            correcting factor: if true, adjust the runtime with the constant from [GuiSlides]_ https://people.rennes.inria.fr/Aurore.Guillevic/talks/2024-07-Douala/24-07-Douala-RSA.pdf

        Returns:
            tuple: (time complexity, memory complexity) of GNFS algorithm

        Examples:
            >>> from cryptographic_estimators.IFEstimator import GNFS
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> NF = GNFS(IFProblem(n=4096))
            >>> NF._time_and_memory_complexity({})
            (144.58695341792028, 85.48725232015862)

        """
        n = self.problem.parameters["n"]

        k = (64 / 9) ** (1 / 3)

        time_ln = Lfunction(1/3, k, n/lge)
        # the multiple lge converts the value to base-2
        time = time_ln * lge

        # memory = storing a matrix of relations size 2pi(B1) X 2pi(B1). Note that the matrix is sparse, with O(n) non-zero entries per row (p. 121 in [Cop93]_)
        B1 = Lfunction(1/3, 2/(3**(2./3)), n/lge)

        # log2(pi(B1)) = log2(B1)-log2(ln(B1)) = B1*lge - log2(B1); adding +1 to account for the factor 2 in 2pi(B1);
        memory = (B1*lge - log2(B1) + 1) + log2(n)

        if correctingfactor:
            time = time - correcting_factor

        return time, memory

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """
        Return the memory complexity of the algorithm for a given set of parameters

        Args:
            parameters: dictionary including the parameters

        Returns:
            tuple: (time complexity, memory complexity) of GNFS algorithm without considering the correctingfactor


        """
        return self._time_and_memory_complexity(parameters, correctingfactor=False)

    def __repr__(self):
        rep = "General Number Field Sieve algorithm for " + str(self.problem)
        return rep

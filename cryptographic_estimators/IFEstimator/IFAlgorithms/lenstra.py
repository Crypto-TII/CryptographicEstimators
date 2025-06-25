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
from ..if_helper import Lfunction
from math import log2, sqrt


class Lenstra(IFAlgorithm):
    def __init__(self, problem: IFProblem, **kwargs):
        """Construct an instance of Lenstra EC algorithm for Integer Factoring Estimator.

        Args:
            problem (IFProblem): An instance of the IFProblem class containing the parameters for the problem.

        Examples:
            >>> from cryptographic_estimators.IFEstimator.IFAlgorithms import Lenstra
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> Lenstra(IFProblem(n=4096))
            Lenstra Elliptic Curve factorization algorithm for Integer Factoring Problem with parameter n = 4096
        """
        self._name = "Lenstra"
        super(Lenstra, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, consider_arithmetic=True):
        """Realizes time complexity of Lenstra factorization algorithm [Len17]_ source: https://eprint.iacr.org/2017/1087.pdf (p.6)

        Args:
            parameters (dict): dictionary including the parameters
            consider_arithmetic (bool, optional): if true, consider the complexity of arithmetic on an elliptic curve over Z_{2**n}

        Returns:
            tuple: (time complexity, memory complexity) of Lenstra Elliptic Curve Factoring algorithm

        Examples:
            >>> from cryptographic_estimators.IFEstimator import Lenstra
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> L = Lenstra(IFProblem(n=4096))
            >>> L._time_and_memory_complexity({})
            (285.0347494832151, 14.584962500721156)


        """
        # bit size of the number to factor
        n = self.problem.parameters["n"]
        time = Lfunction(0.5, sqrt(2), n)
        if consider_arithmetic:
            time += 2*log2(n)
        # 4n to store the curve and a point on it + 2n to store one multiple of the point at a time
        memory = log2(4*n+2*n)

        return time, memory

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """Realizes time complexity of Lenstra factorization algorithm [Len] source: https://eprint.iacr.org/2017/1087.pdf (p.6) 
           DOES NOT CONSIDER THE COMPLEXITY OF ELLIPTIC CURVE ARITHMETIC   

         Args:
            parameters (dict): dictionary including the parameters

        Returns:
            tuple: (time complexity, memory complexity) of Lenstra Elliptic Curve Factoring algorithm without EC arithmetic complexity

        """
        time, memory = self._time_and_memory_complexity(
            parameters, consider_arithmetic=False)

        return time, memory

    def __repr__(self):
        rep = "Lenstra Elliptic Curve factorization algorithm for " + \
            str(self.problem)
        return rep

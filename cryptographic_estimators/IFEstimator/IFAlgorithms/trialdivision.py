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
from ..if_helper import primality_testing, D
from math import floor, log2


class TrialDivision(IFAlgorithm):
    def __init__(self, problem: IFProblem, **kwargs):
        """Construct an instance of Trial Division algorithm for Integer Factoring Estimator.

        Args:
            problem (IFProblem): An instance of the IFProblem class containing the parameters for the problem.

        Examples:
            >>> from cryptographic_estimators.IFEstimator.IFAlgorithms import TrialDivision
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> TrialDivision(IFProblem(n=4096))
            TrialDivision algorithm for Integer Factoring Problem with parameter n = 4096
        """

        self._name = "TrialDivision"
        super(TrialDivision, self).__init__(problem, **kwargs)

    def _time_and_memory_complexity(self, parameters: dict, consider_division=True):
        """ The function realizes the following algorithm:
        1. Build a list of prime numbers up to size 2**(floor(sqrt(n))), store this list. Time: pi(floor(sqrt(n)))*time_miller_rabin
        2. For each saved prime, check if it divides our number (complexity of gcd = complexity of division)

        In case memory is limited (< pi(floor(sqrt(n))) ), go over all numbers  < sqrt(n) and test for division (without primility testing)    

        Args:
            parameters (dict): dictionary including the parameters
            consider_division (bool, optional): flag indicating if the runtime of integer division is considered or not 

        Returns:
            tuple: (time complexity, memory complexity) of TrialDivision algorithm

        Examples:
            >>> from cryptographic_estimators.IFEstimator import TrialDivision
            >>> from cryptographic_estimators.IFEstimator import IFProblem
            >>> TD = TrialDivision(IFProblem(n=4096))
            >>> TD._time_and_memory_complexity({})
            (2070.0276629051027, 2037)

        """
        # bit size of the number to factor
        n = self.problem.parameters["n"]
        memory_bound = self.problem.memory_bound
        # log2 of pi(sqrt(n)) = numer of primes < 2^(sqrt(n))
        log_prime_factors_size = floor(n/2-log2(n/2 * 0.693147180559945))

        # naive brute force
        time = (n/2 - 1)
        if consider_division:
            time += log2(D(n))

        memory = log_prime_factors_size

        # if memory allows to store all primes < < 2^(sqrt(n)), store all primes
        if memory_bound >= log_prime_factors_size:
            tmp = log_prime_factors_size+log2(primality_testing(n))
            if consider_division:
                tmp = log_prime_factors_size+log2(primality_testing(n)+D(n))
            if tmp < time:
                time = tmp
                memory = log_prime_factors_size

        return time, memory

    def _tilde_o_time_and_memory_complexity(self, parameters: dict):
        """ The function realizes the following algorithm *WHITHOUT CONSIDERING THE RUNTIME OF DIVISION*
        1. Build a list of prime numbers up to size 2**(floor(sqrt(n))), store this list. Time: pi(floor(sqrt(n)))*time_miller_rabin
        2. For each saved prime, check if it divides our number (complexity of gcd = complexity of division = 1)

        In case memory is limited (<pi(floor(sqrt(n))) ), go over all numbers  < sqrt(n) and test for division (without primility testing)    

        Args:
            parameters (dict): dictionary including the parameters

        Returns:
            tuple: (time complexity, memory complexity) of TrialDivision algorithm without considering the runtime of division

        """
        time, memory = self._time_and_memory_complexity(
            parameters, consider_division=False)

        return time, memory

    def __repr__(self):
        rep = "TrialDivision algorithm for " + str(self.problem)
        return rep
